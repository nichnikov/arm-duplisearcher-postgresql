import logging

import uvicorn
from fastapi import FastAPI

from src import Worker, FastAnswer
from src.utils import data_prepare

logger = logging.getLogger(__name__)


app = FastAPI(title="App duplisearcher")
worker = Worker()


@app.post("/api")
def handle_collection(data: FastAnswer):
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
