class InterpreterNotFoundError(Exception):
    """
    This Class represents the Error, thats occurs if no Interpreter for a file or an itemlist was found.
    """
    pass


class InterpreterFormatError(Exception):
    """
    This Class represents an Error, that occurs while interpreting a file or an itemlist.
    """
    pass


class DatabaseInsertionError(Exception):
    """
    This Class represents an Error, that occurs while inserting into a database.
    """
    pass


class DatabaseMatchingError(Exception):
    """
    This Class represents an Error, that occurs while matching with a database.
    """
    pass


class DatabaseOpeningError(Exception):
    """
    This Class represents an Error, that occurs while opening a database.
    """
    pass
