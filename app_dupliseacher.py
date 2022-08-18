import os
import json
import logging
from typing import Literal
from uuid import uuid4

import pydantic
import uvicorn
from fastapi import FastAPI

from src.utils import Worker


logger = logging.getLogger("app_duplisearcher")
logger.setLevel(logging.INFO)


app = FastAPI(title="app_duplisearcher")

with open(os.path.join("data", "config.json")) as json_config_file:
    config = json.load(json_config_file)

db_path = os.path.join("data", "queries.db")
main = Worker(config["shard_size"], config["dictionary_size"], db_path)


def data_prepare(json_data):
    """Преобразует входящие словари в список кортежей"""
    queries_in = []
    for d in json_data:
        queries_in += [(d.locale, d.moduleId, str(uuid4()), d.id, tx, d.pubIds) for tx in d.clusters]
    return [(str(x[0]), int(x[1]), str(x[2]), int(x[3]), str(x[4]), str(x[5])) for x in queries_in]


class Query(pydantic.BaseModel):
    id: int
    locale: Literal["ru", "ua", "kz", "uz"]
    moduleId: int
    clusters: list[str]
    pubIds: list[int]


class FastAnswer(pydantic.BaseModel):
    score: float = pydantic.Field(description="The similarity coefficient")
    data: list[Query]
    operation: Literal["add", "update", "delete", "delete_all", "search"]


@app.post("/api")
def handle_collection(data: FastAnswer):
    """Service searches for duplicates, adds and deletes data in collection."""

    queries = data_prepare(data.data)
    lc, m_i, q_i, a_i, txs, p_ids = zip(*queries)
    match data.operation:
        case "add":
            main.add(queries)
            logger.info(f"quantity: {main.matrix_list.quantity}")
            return {"quantity": main.matrix_list.quantity}
        case "delete":
            main.delete(list(set(a_i)))
            logger.info(f"quantity: {main.matrix_list.quantity}")
            return {"quantity": main.matrix_list.quantity}
        case "update":
            main.update(queries)
            logger.info("data were updated")
            return {"quantity": main.matrix_list.quantity}
        case "search":
            search_results = main.search(queries, data.score)
            return search_results
        case "delete_all":
            main.delete_all()
            logger.info(f"quantity: {main.matrix_list.quantity}")
            return {"quantity": main.matrix_list.quantity}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
