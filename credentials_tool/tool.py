"""Main module."""
from credentials_tool.abstract_classes import AbstractDatabase, AbstractFormat
from credentials_tool.errors import InterpreterNotFoundError, DatabaseInsertionError, DatabaseMatchingError, InterpreterFormatError


def read_data_from_file(credentials_format: AbstractFormat, filename: str) -> list:
    """
    This function reads data from a file and returns it

    credentials_format: AbstractFormat
        the format in which the file will be interpreted
    filename: str
        the file name
    """

    try:

        data = credentials_format.read_data_from_file(filename)

    except InterpreterNotFoundError:
        print("Couldnt find a valid interpreter for the file")
        return []

    except InterpreterFormatError:
        print("file "+filename+" is not in a valid format")
        return []

    except FileNotFoundError:
        print("File "+filename+" doesnt exist")
        return []

    except PermissionError:
        print("Permission Denied for "+filename)
        return []

    print("Read "+str(len(data))+" credentials from "+filename)
    print(*data, sep="\n")

    return data


def read_data_from_file_to_database(credentials_format: AbstractFormat, database: AbstractDatabase, filename: str):
    """
    This function reads data from a file and inserts it into a database

    credentials_format: AbstractFormat
        the format in which the file will be interpreted and the data will be inserted
    database: AbstractDatabase
        the database in which the data will be inserted
    filename: str
        the file name
    """

    data = read_data_from_file(credentials_format, filename)

    if len(data) == 0:
        return

    try:

        credentials_format.add_table_to_database(database)  # adds the format table, if it doesnt already exists
        credentials_format.add_data_to_database(database, data)

    except DatabaseInsertionError:

        print("Error occured while writing data into the database")
        print("Probably because a table "+credentials_format.table_name+" already exists with a different datastructure then:")

        for column, ctype in zip(credentials_format.table_columns, credentials_format.table_types):
            print(column+" "+ctype)


def match_data_from_file_with_database(credentials_format: AbstractFormat, database: AbstractDatabase, filename: str):
    """
    This function reades data from a file and matches it with a database

    credentials_format: AbstractFormat
        the format in which the file will be interpreted and the data will be matched
    database: AbstractDatabase
        the database to which the data will be matched
    filename: str
        the file name
    """

    data = credentials_format.read_data_from_file(filename)

    print("match file "+filename+" with database:")

    if len(data) == 0:
        return

    matches = []

    try:
        matches = credentials_format.match_data_with_database(database, data)

    except DatabaseMatchingError:

        print("Error occured while matching data with database")
        print("Probably because a table "+credentials_format.table_name+" already exists with a different datastructure then:")

        for column, ctype in zip(credentials_format.table_columns, credentials_format.table_types):
            print(column+" "+ctype)

    print("found "+str(len(matches))+" matches:")
    for match in matches:
        print(match)


def match_data_from_itemlist_with_database(credentials_format: AbstractFormat, database: AbstractDatabase, itemlist: list):
    """
    This function reades data from a itemlist and matches it with a database

    credentials_format: AbstractFormat
        the format in which the itemlist will be interpreted and the data will be matched
    database: AbstractDatabase
        the database to which the data will be matched
    itemlist: str
        the itemlist, which will be matched with the database
    """

    try:
        data = credentials_format.read_data_from_itemlist(itemlist)

    except InterpreterNotFoundError:
        print("Couldnt find a valid interpreter for the file")
        return

    except InterpreterFormatError:
        print("The given item are not in a valid format")
        return

    print("match itemlist with database:")

    if len(data) == 0:
        return

    matches = []

    try:
        matches = credentials_format.match_data_with_database(database, data)

    except DatabaseMatchingError:

        print("Error occured while matching data with database")
        print("Probably because a table "+credentials_format.table_name+" already exists with a different datastructure then:")

        for column, ctype in zip(credentials_format.table_columns, credentials_format.table_types):
            print(column+" "+ctype)

    print("found "+str(len(matches))+" matches:")
    for match in matches:
        print(match)
