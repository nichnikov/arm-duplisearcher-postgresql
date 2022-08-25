from typing import Literal, NamedTuple

from pydantic import BaseModel
from scipy.sparse import csc_matrix


class IdVector(NamedTuple):
    id: str
    vector: csc_matrix


class Data(NamedTuple):
    locale: str
    moduleId: int
    queryId: str
    answerId: int
    cluster: str
    pubIds: list[int]


class DataTransposed(NamedTuple):
    locales: list[str]
    moduleIds: list[int]
    queryIds: list[str]
    answerIds: list[int]
    clusters: list[str]
    pubIds: list[str]


class FastAnswer(BaseModel):
    id: int
    locale: Literal["ru", "ua", "kz", "uz"]
    moduleId: int
    clusters: list[str]
    pubIds: list[int | None]


class RequestData(BaseModel):
    score: float | None = 0.99
    data: list[FastAnswer] = []
    operation: Literal["add", "update", "delete", "delete_all", "search"]
