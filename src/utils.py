import pathlib
from uuid import uuid4

from src.types import Data, DataTransposed, FastAnswer


def data_prepare(data: list[FastAnswer]) -> list[Data]:
    queries_in = []
    for item in data:
        queries_in += [
            Data(
                locale=item.locale,
                moduleId=item.moduleId,
                queryId=str(uuid4()),
                answerId=item.id,
                cluster=cluster,
                pubIds=item.pubIds,
            )
            for cluster in item.clusters
        ]
    return queries_in


def transpose(data: list[Data]) -> DataTransposed:
    transposed = DataTransposed(*zip(*data))
    return transposed


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def fix_path_to_tests(path: str) -> str:
    path_cwd = pathlib.Path.cwd()
    if "tests" not in path_cwd.parts:
        path_cwd = path_cwd.joinpath("tests")
    else:
        path_cwd = pathlib.Path(*path_cwd.parts[: (path_cwd.parts.index("tests") + 1)])
    return str(path_cwd.joinpath(path))
