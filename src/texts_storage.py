from sqlalchemy import Column, Integer, String, ARRAY, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

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
    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def row2dict(row: Base) -> dict:
        _dict = {}
        for column in row.__table__.columns:
            _dict[column.name] = getattr(row, column.name)

        return _dict

    def add(self, data: list[Data]) -> None:
        queries = [Query(**item._asdict()) for item in data]
        self.session.bulk_save_objects(queries)
        self.session.commit()

    def search_by_answers(self, ids: list[int]) -> list[Data]:
        queries = self.session.query(Query).filter(Query.answer_id.in_(ids)).all()
        return [Data(**self.row2dict(item)) for item in queries]

    def search_by_queries(self, ids: list[int]) -> list[Data]:
        queries = self.session.query(Query).filter(Query.query_id.in_(ids)).all()
        return [Data(**self.row2dict(item)) for item in queries]

    def delete_by_queries(self, ids: list[str]) -> None:
        self.session.query(Query).filter(Query.query_id.in_(ids)).delete()
        self.session.commit()

    def delete_all(self) -> None:
        self.session.query(Query).delete()
        self.session.commit()

    def get_all(self) -> list[Data]:
        queries = self.session.query(Query).all()
        return [Data(**self.row2dict(item)) for item in queries]
