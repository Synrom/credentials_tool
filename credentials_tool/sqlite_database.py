import sqlite3
from credentials_tool.abstract_classes import AbstractDatabase


class SqliteDatabase(AbstractDatabase):

    def __init__(self, filename: str):
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()

    def insert(self, tablename: str, values: tuple) -> None:

        sql_cmd = "INSERT INTO "+tablename+" VALUES ("
        sql_cmd += ", ".join(["?"] * len(values))
        sql_cmd += ")"

        self.cursor.execute(sql_cmd, values)

    def match(self, tablename: str, search_columns: tuple, values: tuple, return_columns: tuple = ("*",)) -> list:

        self.cursor.fetchall()

        sql_cmd = "SELECT "
        sql_cmd += ", ".join(return_columns)
        sql_cmd += " FROM "+tablename+" WHERE "
        sql_cmd += " AND ".join(column+"=?" for column in search_columns)

        self.cursor.execute(sql_cmd, values)

        return self.cursor.fetchall()

    def exist_table(self, tablename: str):

        self.cursor.fetchall()

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tablename,))

        if self.cursor.fetchone():
            return True
        return False

    def create_table(self, tablename: str, columns: tuple, types: tuple) -> None:

        sql_cmd = "CREATE TABLE "+tablename+" ("
        sql_cmd += ",".join(column+" "+typename for column, typename in zip(columns, types))
        sql_cmd += ")"

        self.cursor.execute(sql_cmd)

    def create_table_if_non_existent(self, tablename: str, columns: tuple, types: tuple) -> None:

        if not self.exist_table(tablename):
            self.create_table(tablename, columns, types)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
