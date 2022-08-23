import logging
from collections import namedtuple
from itertools import groupby

from config import SHARD_SIZE, VOCABULARY_SIZE, DB_PATH
from src.matrices import MatricesList
from src.texts_processing import TextsVectorsBoW, TextsTokenizer
from src.texts_storage import TextsStorage
from src.types import Data, DataTransposed, IdVector

logger = logging.getLogger(__name__)


def resulting_report(searched_data, result_tuples, found_data_l: list[Data], locale: str):
    """"""
    # TODO: refactor
    def grouping(similarity_items, searched_queries, searched_answers_moduls, locale: str):
        """"""
        return [
            {
                "id": k1,
                "locale": locale,
                "moduleId": searched_answers_moduls[k1],
                "clustersWithDuplicate": [
                    {
                        "cluster": searched_queries[k2]["cluster"],
                        "duplicates": [
                            {
                                "cluster": x2.FoundText,
                                "id": x2.FoundAnswerId,
                                "moduleId": x2.FoundModuleId,
                                "pubId": x2.FoundPubIds,
                            }
                            for x2 in v2
                        ],
                    }
                    for k2, v2 in groupby(sorted(v1, key=lambda c: c.SearchedQueryId), lambda d: d.SearchedQueryId)
                ],
            }
            for k1, v1 in groupby(
                sorted(similarity_items, key=lambda a: a.SearchedAnswerId), lambda b: b.SearchedAnswerId
            )
        ]

    ResultItem = namedtuple(
        "ResultItem",
        "SearchedAnswerId, "
        "SearchedText, "
        "SearchedQueryId, "
        "SearchedModuleId, "
        "SearchedPubIds, "
        "FoundAnswerId, "
        "FoundText, "
        "FoundQueryId, "
        "FoundModuleId, "
        "FoundPubIds",
    )

    searched_dict = {
        q_i: {"answerId": a_i, "moduleId": m_i, "cluster": cl, "pubIds": p_i}
        for lc, m_i, q_i, a_i, cl, p_i in searched_data
    }

    searched_answers_moduls = {a_i: m_i for lc, m_i, q_i, a_i, cl, p_i in searched_data}

    found_dict = {d.queryId: d for d in found_data_l}

    similarity_items = [
        ResultItem(
            searched_dict[sq_i]["answerId"],
            searched_dict[sq_i]["cluster"],
            sq_i,
            searched_dict[sq_i]["moduleId"],
            searched_dict[sq_i]["pubIds"],
            found_dict[fq_i].answerId,
            found_dict[fq_i].cluster,
            found_dict[fq_i].queryId,
            found_dict[fq_i].moduleId,
            found_dict[fq_i].pubIds,
        )
        for sq_i, fq_i, sc in result_tuples
    ]

    return grouping(similarity_items, searched_dict, searched_answers_moduls, locale)


class Worker:
    """Объект для оперирования MatricesList и TextsStorage"""

    def __init__(self):
        # TODO: init from db
        self.text_storage = TextsStorage(db_path=DB_PATH)
        self.matrix_list = MatricesList(max_size=SHARD_SIZE)
        self.tokenizer = TextsTokenizer()
        self.vectorizer = TextsVectorsBoW(max_dict_size=VOCABULARY_SIZE)

    @property
    def quantity(self) -> int:
        return self.matrix_list.quantity

    @staticmethod
    def transpose(data: list[Data]) -> DataTransposed:
        transposed = DataTransposed(*zip(*data))
        return transposed

    def vectors_maker(self, data: list[Data]) -> list[IdVector]:
        """"""
        data_t = self.transpose(data)
        tokens = self.tokenizer(data_t.clusters)
        vectors = self.vectorizer(tokens)
        return [IdVector(id=_id, vector=_vec) for _id, _vec in zip(data_t.queryIds, vectors)]

    def add(self, data: list[Data]) -> None:
        """"""
        ids_vectors = self.vectors_maker(data)
        self.matrix_list.add(ids_vectors)
        self.text_storage.add(data)

    def delete(self, data: list[Data]) -> None:
        """"""
        data_t = self.transpose(data)
        searched_data = self.text_storage.search_answers(ids=tuple(set(data_t.answerIds)))
        q_ids = [x[2] for x in searched_data]
        q_ids = list(set(q_ids))
        self.matrix_list.delete(q_ids)
        self.text_storage.delete(q_ids)

    def delete_all(self) -> None:
        """"""
        self.text_storage.delete_all()
        self.matrix_list = MatricesList(max_size=SHARD_SIZE)

    def update(self, data: list[Data]) -> None:
        data_t = self.transpose(data)
        searched_data = self.text_storage.search_answers(ids=data_t.answerIds)
        self.delete(searched_data)
        self.add(data)

    def search(self, data: list[Data], score: float) -> list[tuple]:
        """grouped searched_data by locale:"""
        it = groupby(sorted(data, key=lambda x: x[0]), key=lambda x: x[0])
        data_by_locale = {k: list(v) for k, v in it}
        results = []
        for lc in data_by_locale:
            ids_vectors = self.vectors_maker(data_by_locale[lc])
            result_tuples = self.matrix_list.search(ids_vectors, score)
            searched_ids, found_ids, scores = zip(*result_tuples)
            found_data = self.text_storage.search_queries(ids=found_ids)
            found_data_l = [Data(*x) for x in found_data]
            results += resulting_report(data, result_tuples, found_data_l, locale=lc)
        return results
