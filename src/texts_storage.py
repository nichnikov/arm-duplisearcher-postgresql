import ast
import sqlite3

from src.types import Data


class TextsStorage:
    def __init__(self, db_path: str):
        self.con = sqlite3.connect(db_path, check_same_thread=False)
        self.con.execute(
            "create table if not exists "
            "queries(locale text, moduleId integer, queryId text primary key, "
            "answerId integer, cluster text, pubIds text)"
        )
        self.con.execute("VACUUM")
        self.cur = self.con.cursor()

    def delete(self, query_ids: list[int]):
        """dictionary must include all attributes"""
        sql = f"delete from queries where queryId in ({','.join(['?'] * len(query_ids))})"
        self.cur.execute(sql, query_ids)
        self.con.commit()

    def delete_all(self):
        """"""
        self.cur.execute("delete from queries")
        self.con.commit()

    def add(self, input_data: list[Data]) -> None:
        """"""
        transformed_data = [Data(*x[:-1], str(x[-1])) for x in input_data]
        self.cur.executemany("insert into queries values(?, ?, ?, ?, ?, ?)", transformed_data)
        self.con.commit()

    def search_answers(self, ids: list[int]) -> list[Data]:
        """Возвращает текст вопроса с метаданными по входящему списку answer ids"""
        sql = f"select * from queries where answerId in ({','.join(['?'] * len(ids))})"
        self.cur.execute(sql, ids)
        result = self.cur.fetchall()
        found_data = [Data(*x[:-1], ast.literal_eval(x[-1])) for x in result]
        return found_data

    def search_queries(self, ids: list[int]) -> list[Data]:
        """Возвращает текст вопроса с метаданными по входящему списку query ids"""
        sql = f"select * from queries where queryId in ({','.join(['?'] * len(ids))})"
        self.cur.execute(sql, ids)
        result = self.cur.fetchall()
        found_data = [Data(*x[:-1], ast.literal_eval(x[-1])) for x in result]
        return found_data

    def get_all(self):
        self.cur.execute(f"select * from queries")
        return self.cur.fetchall()
