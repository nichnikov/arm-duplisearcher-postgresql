from typing import Literal, NamedTuple

from pydantic import BaseModel, Field
from scipy.sparse import csc_matrix


class IdVector(NamedTuple):
    id: str
    vector: csc_matrix


class Data(NamedTuple):
    locale: str
    module_id: int
    query_id: str
    answer_id: int
    cluster: str
    pub_ids: list[int]


class DataTransposed(NamedTuple):
    locales: list[Data.locale]
    module_ids: list[Data.module_id]
    query_ids: list[Data.query_id]
    answer_ids: list[Data.answer_id]
    clusters: list[Data.cluster]
    pub_ids: list[Data.pub_ids]


class FastAnswer(BaseModel):
    answer_id: int = Field(alias="id")
    locale: Literal["ru", "ua", "kz", "uz"]
    module_id: int = Field(alias="moduleId")
    clusters: list[str]
    pub_ids: list[int | None] = Field(alias="pubIds")


class RequestData(BaseModel):
    score: float | None = 0.99
    data: list[FastAnswer] = []
    operation: Literal["add", "update", "delete", "delete_all", "search"]


# class Duplicate(BaseModel):
#     id: int
#     moduleId: int
#     cluster: str
#     pubId: list[int]  # -> pubIds
#
#
# class ClusterWithDuplicates(BaseModel):
#     cluster: str
#     duplicates: list[Duplicate]
#
#
# class ResponseData(BaseModel):
#     id: int
#     locale: Literal["ru", "ua", "kz", "uz"]
#     moduleId: int
#     clustersWithDuplicate: list[ClusterWithDuplicates]
