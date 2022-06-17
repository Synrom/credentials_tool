import sqlite3
from credentials_tool.abstract_classes import AbstractDatabase
from credentials_tool.errors import DatabaseInsertionError, DatabaseMatchingError, DatabaseOpeningError


class SqliteDatabase(AbstractDatabase):

    def __init__(self, filename: str):

        try:

            self.connection = sqlite3.connect(filename)

        except sqlite3.OperationalError:
            raise DatabaseOpeningError("Cant open "+filename)

        self.cursor = self.connection.cursor()

    def insert(self, tablename: str, values: tuple) -> None:

        sql_cmd = "INSERT INTO "+tablename+" VALUES ("
        sql_cmd += ", ".join(["?"] * len(values))
        sql_cmd += ")"

        try:

            self.cursor.execute(sql_cmd, values)

        except sqlite3.OperationalError:
            raise DatabaseInsertionError("Insertion Error while trying to execute: "+sql_cmd)

    def match(self, tablename: str, search: dict, return_columns: tuple = ("*",)) -> list:

        self.cursor.fetchall()

        sql_cmd = "SELECT "
        sql_cmd += ", ".join(return_columns)
        sql_cmd += " FROM "+tablename+" WHERE "

        search_values = ()
        search_columns = ()
        for column, value in search.items():
            search_columns += (column,)
            search_values += (value,)

        sql_cmd += " AND ".join(column+"=?" for column in search_columns)

        try:
            self.cursor.execute(sql_cmd, search_values)

        except sqlite3.OperationalError:
            raise DatabaseMatchingError("Matching Error while trying to execute: "+sql_cmd)

        return self.cursor.fetchall()

    def exist_table(self, tablename: str):

        self.cursor.fetchall()

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tablename,))

        if self.cursor.fetchone():
            return True
        return False

    def create_table(self, tablename: str, tablestructure: dict) -> None:

        sql_cmd = "CREATE TABLE "+tablename+" ("
        sql_cmd += ",".join(str(column)+" "+str(typename) for column, typename in tablestructure.items())
        sql_cmd += ")"

        try:

            self.cursor.execute(sql_cmd)

        except sqlite3.OperationalError:
            raise DatabaseInsertionError("Insertion Error while trying to execute: "+sql_cmd)

    def create_table_if_non_existent(self, tablename: str, tablestructure: dict) -> None:

        if not self.exist_table(tablename):
            self.create_table(tablename, tablestructure)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
