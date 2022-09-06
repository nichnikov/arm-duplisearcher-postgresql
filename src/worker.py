import logging
from collections import namedtuple
from itertools import groupby

from config import SHARD_SIZE
from src.matrices import MatricesList
from src.schemas import Data
from src.texts_storage import Storage
from src.utils import transpose

logger = logging.getLogger(__name__)


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


def grouping(similarity_items, searched_queries, searched_answers_moduls, locale: str):
    """"""
    return [
        {
            "id": k1,
            "locale": locale,
            "moduleId": searched_answers_moduls[k1],
            "clustersWithDuplicate": [
                {
                    "cluster": searched_queries[k2].cluster,
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
        for k1, v1 in groupby(sorted(similarity_items, key=lambda a: a.SearchedAnswerId), lambda b: b.SearchedAnswerId)
    ]


def resulting_report(searched_data, result_tuples, found_data_l: list[Data], locale: str):
    """"""
    searched_dict = {item.query_id: item for item in searched_data}
    found_dict = {d.query_id: d for d in found_data_l}
    searched_answers_moduls = {item.answer_id: item.module_id for item in searched_data}

    similarity_items = [
        ResultItem(
            searched_dict[sq_i].answer_id,
            searched_dict[sq_i].cluster,
            searched_dict[sq_i].query_id,
            searched_dict[sq_i].module_id,
            searched_dict[sq_i].pub_ids,
            found_dict[fq_i].answer_id,
            found_dict[fq_i].cluster,
            found_dict[fq_i].query_id,
            found_dict[fq_i].module_id,
            found_dict[fq_i].pub_ids,
        )
        for sq_i, fq_i, _ in result_tuples
    ]

    return grouping(similarity_items, searched_dict, searched_answers_moduls, locale)


class Worker:
    """Объект для оперирования MatricesList и TextsStorage"""

    def __init__(self, storage: Storage):
        self.text_storage = storage
        self.matrix_list = MatricesList(max_size=SHARD_SIZE)
        if len(existing_data := self.text_storage.get_all()) > 0:
            self.matrix_list.add(data=existing_data)

    @property
    def quantity(self) -> int:
        return self.matrix_list.quantity

    def add(self, data: list[Data]) -> None:
        """"""
        self.matrix_list.add(data)
        self.text_storage.add(data)

    def delete(self, data: list[Data]) -> None:
        """"""
        data_t = transpose(data)
        searched_data = self.text_storage.search_by_answers(ids=list(set(data_t.answer_ids)))
        q_ids = [x.query_id for x in searched_data]
        q_ids = list(set(q_ids))
        self.matrix_list.delete(ids=q_ids)
        self.text_storage.delete_by_queries(ids=q_ids)

    def delete_all(self) -> None:
        """"""
        self.text_storage.delete_all()
        self.matrix_list = MatricesList(max_size=SHARD_SIZE)

    def update(self, data: list[Data]) -> None:
        data_t = transpose(data)
        searched_data = self.text_storage.search_by_answers(ids=data_t.answer_ids)
        self.delete(searched_data)
        self.add(data)

    def search(self, data: list[Data], score: float) -> list[dict]:
        """grouped searched_data by locale:"""
        it = groupby(sorted(data, key=lambda x: x.locale), key=lambda x: x.locale)
        data_by_locale = {k: list(v) for k, v in it}
        results = []
        for lc in data_by_locale:
            result_tuples = self.matrix_list.search(data=data_by_locale[lc], min_score=score)
            searched_ids, found_ids, scores = zip(*result_tuples)
            found_data = self.text_storage.search_by_queries(ids=found_ids)
            results += resulting_report(data, result_tuples, found_data, locale=lc)
        return results
