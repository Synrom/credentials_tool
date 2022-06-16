from abc import ABC, abstractmethod


class AbstractDatabase(ABC):

    @abstractmethod
    def insert(self, table: str, values: tuple):
        pass

    @abstractmethod
    def match(self, table: str, search_columns: tuple, values: tuple, return_columns: tuple = ("*",)) -> list:
        pass

    @abstractmethod
    def create_table_if_non_existent(self, tablename: str, columns: tuple, types: tuple) -> None:
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def close(self):
        pass


class AbstractFormat(ABC):

    @abstractmethod
    def read_data_from_file(self, filename: str) -> list:
        pass

    @abstractmethod
    def add_data_to_database(self, database: AbstractDatabase, data: list) -> None:
        pass

    @abstractmethod
    def match_data_with_database(self, database: AbstractDatabase, data: list) -> list:
        pass

    @abstractmethod
    def match_fields_with_database(self, database: AbstractDatabase, fields: tuple, values: tuple) -> list:
        pass
