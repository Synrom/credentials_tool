from abc import ABC, abstractmethod


class AbstractDatabase(ABC):
    """
    This class represents an abstract database.
    """

    @abstractmethod
    def insert(self, table: str, values: tuple) -> None:
        """
        This function inserts a row into a table of the database

        table: str
            The name of the table, the row will be inserted to
        values: tuple
            The values to the elements of the row, that will be inserted

        """
        pass

    @abstractmethod
    def match(self, table: str, search: dict, return_columns: tuple = ("*",)) -> list:
        """
        This function matches values with a table and returns the matching rows

        table: str
            The name of the table, the values will be matchd with
        search: dict
            The values the table will be matched with. Specified in a {"<column_name>": <value>,...} dictonary
        return_columns: tuple
            The values of the columns specified by return_columns will be returned. (default ("*",))

        """
        pass

    @abstractmethod
    def create_table_if_non_existent(self, tablename: str, tablestructure: dict) -> None:
        """
        This function creates a table if it doesnt already exists.

        table: str
            The name of the table, that will be created
        tablestructure: dict
            This represents the tablestructure. Specified in a {"<column_name>": "<column_type>",...} dictonary

        """
        pass

    @abstractmethod
    def commit(self):
        """
        This function commits all the changes to the database
        """
        pass

    @abstractmethod
    def close(self):
        """
        This function closes the database
        """
        pass


class AbstractFormat(ABC):
    """
    This class represents an abstract format.
    That includes the way data is stored in and matched with databases and the way data is interpreted and read from files or strings.
    """

    @abstractmethod
    def read_data_from_file(self, filename: str) -> list:
        """
        This function reades data from a file and returns it.

        filename: str
            The filename of the datafile

        """
        pass

    @abstractmethod
    def read_data_from_itemlist(self, itemlist: list[str]) -> list:
        """
        This function reades data from an itemlist and returns it.

        itemlist: list[str]
            itemlist is a list of the items, that will be read

        """
        pass

    @abstractmethod
    def add_data_to_database(self, database: AbstractDatabase, data: list) -> None:
        """
        This function adds data to a database.

        database: AbstractDatabase
            This is the database, to which the data will be added
        data: list
            This is the data, that will be added to the database

        """
        pass

    @abstractmethod
    def match_data_with_database(self, database: AbstractDatabase, data: list) -> list:
        """
        This function matches data with a database and returns the matches.

        database: AbstractDatabase
            This is the database, with which the data will be matched
        data: list
            This is the data, that will be matched with the database

        """
        pass

    @abstractmethod
    def add_table_to_database(self, database: AbstractDatabase) -> None:
        """
        This function adds its own table to a database, if the table doesnt already exists.

        database: AbstractDatabase
            This is the database, to which the table will be added

        """
        pass

    # table_name should be unique for every format
    @property
    def table_name(self) -> str:
        """ This is the tablename in databases of this format. """
        raise NotImplementedError()

    @property
    def table_columns(self) -> tuple:
        """ These are the tablecolumns in databases of this format. """
        raise NotImplementedError()

    @property
    def table_types(self) -> tuple:
        """ These are the types of the tablecolumns in databases of this format. """
        raise NotImplementedError()
