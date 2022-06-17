"""Main module."""
from credentials_tool.abstract_classes import AbstractDatabase, AbstractFormat
from credentials_tool.errors import InterpreterNotFoundError, DatabaseInsertionError, DatabaseMatchingError


def read_data_from_file(credentials_format: AbstractFormat, filename: str):

    try:

        data = credentials_format.read_data_from_file(filename)

    except InterpreterNotFoundError:
        print("Couldnt find a valid interpreter for the file")
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

    data = read_data_from_file(credentials_format, filename)

    if len(data) == 0:
        return

    try:

        credentials_format.add_table_to_database(database)
        credentials_format.add_data_to_database(database, data)

    except DatabaseInsertionError:

        print("Error occured while writing data into the database")
        print("Probably because a table "+credentials_format.table_name+" already exists with a different datastructure then:")

        for column, ctype in zip(credentials_format.table_columns, credentials_format.table_types):
            print(column+" "+ctype)


def match_data_from_file_with_database(credentials_format: AbstractFormat, database: AbstractDatabase, filename: str):

    data = credentials_format.read_data_from_file(filename)

    print("match "+filename+" with database:")

    if len(data) == 0:
        return

    try:
        credentials_format.match_data_with_database(database, data)

    except DatabaseMatchingError:

        print("Error occured while matching data with database")
        print("Probably because a table "+credentials_format.table_name+" already exists with a different datastructure then:")

        for column, ctype in zip(credentials_format.table_columns, credentials_format.table_types):
            print(column+" "+ctype)


def match_data_from_itemlist_with_database(credentials_format: AbstractFormat, database: AbstractDatabase, itemlist: list):

    data = credentials_format.read_data_from_itemlist(itemlist)

    print("match itemlist with database:")

    if len(data) == 0:
        return

    try:
        credentials_format.match_data_with_database(database, data)

    except DatabaseMatchingError:

        print("Error occured while matching data with database")
        print("Probably because a table "+credentials_format.table_name+" already exists with a different datastructure then:")

        for column, ctype in zip(credentials_format.table_columns, credentials_format.table_types):
            print(column+" "+ctype)
