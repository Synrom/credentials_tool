from abc import ABC, abstractmethod


class AbstractDatabase(ABC):

    @abstractmethod
    def insert(self, table: str, values: tuple):
        pass

    @abstractmethod
    def match(self, table: str, search: dict, return_columns: tuple = ("*",)) -> list:
        pass

    @abstractmethod
    def create_table_if_non_existent(self, tablename: str, tablestructure: dict) -> None:
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
    def match_fields_with_database(self, database: AbstractDatabase, search: dict) -> list:
        pass

    # table_name should be unique for every format
    @property
    def table_name(self) -> str:
        raise NotImplementedError()

    @property
    def table_columns(self) -> tuple:
        raise NotImplementedError()

    @property
    def table_types(self) -> tuple:
        raise NotImplementedError()
