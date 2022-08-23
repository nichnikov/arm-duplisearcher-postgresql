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
    pubIds: str


# TODO: Proper naming
class DataT(NamedTuple):
    locales: tuple[str]
    moduleIds: tuple[int]
    queryIds: tuple[str]
    answerIds: tuple[int]
    clusters: tuple[str]
    pubIds: tuple[str]


class FastAnswerData(BaseModel):
    id: int
    locale: Literal["ru", "ua", "kz", "uz"]
    moduleId: int
    clusters: list[str]
    pubIds: list[int | None]


class FastAnswer(BaseModel):
    score: float | None = 0.99
    data: list[FastAnswerData] = []
    operation: Literal["add", "update", "delete", "delete_all", "search"]
