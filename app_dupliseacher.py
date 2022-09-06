import logging

import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import QUERIES_DB
from src import Worker, Storage, RequestData
from src.utils import data_prepare

logger = logging.getLogger(__name__)


app = FastAPI(title="Duplicate searcher")


def get_db():
    engine = create_engine(QUERIES_DB, echo=True)
    with Session(engine) as session:
        yield session


def get_worker(db=Depends(get_db)) -> Worker:  # noqa
    storage = Storage(session=db)
    return Worker(storage=storage)


@app.post("/api")
def handle_collection(data: RequestData, worker: Worker = Depends(get_worker)):  # noqa
    """Service searches for duplicates, adds, deletes data in collection."""
    queries = data_prepare(data.data)
    match data.operation:
        case "add":
            worker.add(data=queries)
            return {"quantity": worker.quantity}
        case "update":
            worker.update(data=queries)
            return {"quantity": worker.quantity}
        case "search":
            search_results = worker.search(data=queries, score=data.score)
            return search_results
        case "delete":
            worker.delete(data=queries)
            return {"quantity": worker.quantity}
        case "delete_all":
            worker.delete_all()
            return {"quantity": worker.quantity}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
