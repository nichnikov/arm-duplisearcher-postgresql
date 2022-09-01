from sqlalchemy import Column, Integer, String, ARRAY, MetaData
from sqlalchemy.ext.declarative import declarative_base

from src.schemas import Data

Base = declarative_base(metadata=MetaData())


class Query(Base):
    __tablename__ = "queries"

    locale = Column(String)
    module_id = Column(Integer)
    query_id = Column(String, primary_key=True)
    answer_id = Column(Integer)
    cluster = Column(String)
    pub_ids = Column(ARRAY(Integer))


class Storage:
    def __init__(self, db):
        self.db = db

    @staticmethod
    def row2dict(row: Base):
        _dict = {}
        for column in row.__table__.columns:
            _dict[column.name] = str(getattr(row, column.name))

        return _dict

    def add(self, data: list[Data]) -> None:
        queries = [Query(**item._asdict()) for item in data]
        self.db.bulk_save_objects(queries)
        self.db.commit()

    def search_answers(self, ids: list[int]) -> list[Data]:
        queries = self.db.query(Query).filter(Query.answer_id.in_(ids)).all()
        return [Data(**self.row2dict(item)) for item in queries]

    def search_queries(self, ids: list[int]) -> list[Data]:
        queries = self.db.query(Query).filter(Query.query_id.in_(ids)).all()
        return [Data(**self.row2dict(item)) for item in queries]

    def delete_queries(self, ids: list[int]) -> None:
        self.db.query(Query).filter(Query.query_id.in_(ids)).delete()
        self.db.commit()

    def delete_all(self) -> None:
        self.db.query(Query).delete()
        self.db.commit()

    def get_all(self) -> list[Data]:
        queries = self.db.query(Query).all()
        return [Data(**self.row2dict(item)) for item in queries]
