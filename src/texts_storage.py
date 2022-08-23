import sqlite3

from src.types import Data


class TextsStorage:
    def __init__(self, db_path: str):
        self.con = sqlite3.connect(db_path, check_same_thread=False)
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
        # self.con.close()

    def add(self, input_data: list[Data]):
        """"""
        self.cur.executemany("insert into queries values(?, ?, ?, ?, ?, ?)", input_data)
        self.con.commit()

    def search_answers(self, ids: tuple[int]):
        """Возвращает текст вопроса с метаданными по входящему списку answer ids"""
        sql = f"select * from queries where answerId in ({','.join(['?'] * len(ids))})"
        self.cur.execute(sql, ids)
        return self.cur.fetchall()

    def search_queries(self, ids: tuple[int]):
        """Возвращает текст вопроса с метаданными по входящему списку query ids"""
        sql = f"select * from queries where queryId in ({','.join(['?'] * len(ids))})"
        self.cur.execute(sql, ids)
        return self.cur.fetchall()
