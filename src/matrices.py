import logging
from itertools import chain
from multiprocessing import Pool

from scipy.sparse import hstack, vstack
from sklearn.metrics.pairwise import cosine_similarity

from config import VOCABULARY_SIZE
from src.texts_processing import TextsVectorsBoW, TextsTokenizer
from src.types import IdVector, Data
from src.utils import chunks, transpose

logger = logging.getLogger(__name__)


class IdsMatrix:
    """"""

    def __init__(self):
        self.ids = []
        self.matrix = None

    def delete(self, ids: list[str]) -> None:
        ids_vectors = [(i, v) for i, v in zip(self.ids, self.matrix) if i not in ids]
        if ids_vectors:
            self.ids, vectors = zip(*ids_vectors)
            self.matrix = vstack(vectors)
        else:
            self.ids = []
            self.matrix = None

    def add(self, ids_vectors: list[IdVector]) -> None:
        """tuples must be like (text_id, text_vector)"""
        ids, vectors = zip(*ids_vectors)
        self.ids += ids
        if self.matrix is None:
            self.matrix = hstack(vectors).T
        else:
            self.matrix = vstack((self.matrix, hstack(vectors).T))


class MatricesList:
    """"""

    def __init__(self, max_size: int):
        self.max_size = max_size
        self.tokenizer = TextsTokenizer()
        self.vectorizer = TextsVectorsBoW(max_dict_size=VOCABULARY_SIZE)
        self.ids_matrix_list = [IdsMatrix()]

    @property
    def quantity(self) -> int:
        _sum = sum([len(m.ids) for m in self.ids_matrix_list])
        logger.info(f"quantity: {_sum}")
        return _sum

    @staticmethod
    def search_func(searched_data: dict) -> list:
        """searched_vectors tuples must be like (query_id, query_vector)"""
        vectors_ids = searched_data["vectors_ids"]
        vectors = searched_data["vectors"]
        matrix = searched_data["matrix"]
        matrix_ids = searched_data["matrix_ids"]
        score = searched_data["score"]

        searched_matrix = hstack(vectors).T
        if matrix is None:
            return []
        try:
            matrix_scores = cosine_similarity(searched_matrix, matrix, dense_output=False)
            search_results = [
                [(v_id, matrix_ids[mrx_i], sc) for mrx_i, sc in zip(scores.indices, scores.data) if sc >= score]
                for v_id, scores in zip(vectors_ids, matrix_scores)
            ]
            logger.info("Searching successfully completed")
            return [x for x in chain(*search_results) if x]
        except Exception as e:
            logger.error("Failed queries search in MainSearcher.search: ", str(e))
            return []

    def vectors_maker(self, data: list[Data]) -> list[IdVector]:
        """"""
        data_t = transpose(data)
        tokens = self.tokenizer(texts=data_t.clusters)
        vectors = self.vectorizer(tokens=tokens)
        return [IdVector(id=_id, vector=_vec) for _id, _vec in zip(data_t.queryIds, vectors)]

    def add(self, data: list[Data]) -> None:
        """"""
        ids_vectors = self.vectors_maker(data)
        for chunk in chunks(ids_vectors, self.max_size):
            is_matrices_full = True
            for im in self.ids_matrix_list:
                if len(im.ids) < self.max_size:
                    im.add(chunk)
                    is_matrices_full = False
            if is_matrices_full:
                """adding new queries_matrix"""
                im = IdsMatrix()
                im.add(chunk)
                self.ids_matrix_list.append(im)

    def delete(self, ids: list[str]) -> None:
        """"""
        for ids_matrix in self.ids_matrix_list:
            if set(ids) & set(ids_matrix.ids):
                ids_matrix.delete(ids=ids)

    def search(self, data: list[Data], min_score: float) -> list[tuple]:
        ids_vectors = self.vectors_maker(data)
        vectors_ids, vectors = zip(*ids_vectors)
        searched_data = [
            {
                "vectors_ids": vectors_ids,
                "vectors": vectors,
                "matrix": mx.matrix,
                "matrix_ids": mx.ids,
                "score": min_score,
            }
            for mx in self.ids_matrix_list
        ]
        pool = Pool()
        search_result = pool.map(self.search_func, searched_data)
        pool.close()
        pool.join()
        return [x for x in chain(*search_result) if x]
