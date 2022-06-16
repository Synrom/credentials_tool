from dataclasses import dataclass
from abc import ABC, abstractmethod
import hashlib
import base64
import re
import os

from credentials_tool.abstract_classes import AbstractFormat, AbstractDatabase


@dataclass
class CredentialHolder():
    email: str
    password: str = ""

    def as_tuple(self):
        return (self.email, self.password)

    def as_seacharble_tuple(self):
        return (self.email, )

    def generate_salt(self):
        return os.urandom(32)

    def get_hashed_password(self, salt):
        hashed_pwd = hashlib.pbkdf2_hmac("sha256", self.password.encode("utf-8"), salt, 100000, dklen=128)
        b64_hashed_pwd = base64.b64encode(hashed_pwd).decode("utf-8")
        return b64_hashed_pwd

    def as_tuple_with_hashed_password(self):
        raw_salt = self.generate_salt()
        hashed_pwd = self.get_hashed_password(raw_salt)
        salt = base64.b64encode(raw_salt).decode("utf-8")

        return (self.email, hashed_pwd, salt)


class InterpreterNotFoundError(Exception):
    pass


class AbstractLineInterpreterCredential(ABC):

    @abstractmethod
    def check_line(self, line: str) -> bool:
        pass

    @abstractmethod
    def interpret_line(self, line: str) -> CredentialHolder:
        pass


class LineInterpreterPasswordMail(AbstractLineInterpreterCredential):

    def __init__(self, email_regex: str):
        self.email_regex = email_regex

    def check_line(self, line: str) -> bool:

        line_splited = line.split(":")

        if len(line_splited) != 2:
            return False

        mail = line_splited[1].strip()
        if re.match(self.email_regex, mail):
            return True

        return False

    def interpret_line(self, line: str) -> CredentialHolder:

        line_splited = line.split(":")

        password = line_splited[0].strip()
        mail = line_splited[1].strip()

        return CredentialHolder(email=mail, password=password)


class LineInterpreterMailPassword(AbstractLineInterpreterCredential):

    def __init__(self, email_regex: str):
        self.email_regex = email_regex

    def check_line(self, line: str) -> bool:

        line_splited = line.split(":")

        if len(line_splited) != 2:
            return False

        mail = line_splited[0].strip()
        if re.match(self.email_regex, mail):
            return True

        return False

    def interpret_line(self, line: str) -> CredentialHolder:

        line_splited = line.split(":")

        mail = line_splited[0].strip()
        password = line_splited[1].strip()

        return CredentialHolder(email=mail, password=password)


class CredentialFormat(AbstractFormat):

    def __init__(self, tablename: str = "credentials", email_regex: str = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"):

        self.line_interpreters = [LineInterpreterMailPassword(email_regex), LineInterpreterPasswordMail(email_regex)]

        self.tablename = tablename
        self.tablecolumns = ("email", "password", "salt")
        self.tablecolumns_for_search = ("email",)
        self.tabletypes = ("varchar(320)", "varchar(172)", "varchar(44)")

    def read_data_from_file(self, filename: str) -> list[CredentialHolder]:

        try:
            f = open(filename, "r")
        except FileNotFoundError:
            print(filename+" doesnt exist")
            return []

        try:

            file_interpreter = self.establich_interpreter_for_file(f)

        except InterpreterNotFoundError:
            print("Error: couldnt find any valid interpreter for "+filename)
            f.close()
            return []

        credentials = []

        for line in f.readlines():

            credentials.append(file_interpreter.interpret_line(line))

        f.close()

        return credentials

    def add_data_to_database(self, database: AbstractDatabase, credentials: list[CredentialHolder]) -> None:

        for credential in credentials:

            database.insert(self.tablename, credential.as_tuple_with_hashed_password())

    def match_data_with_database(self, database: AbstractDatabase, credentials: list[CredentialHolder]) -> list:

        matches = []

        for credential in credentials:

            search_credential = credential.as_seacharble_tuple()
            matches_of_credential = database.match(self.tablename, self.tablecolumns_for_search, search_credential)

            for match_of_credential in matches_of_credential:

                raw_salt = base64.b64decode(match_of_credential[2])

                if credential.get_hashed_password(raw_salt) == match_of_credential[1]:
                    matches.append(credential)

        return matches

    def match_fields_with_database(self, database: AbstractDatabase, fields: tuple, values: tuple) -> list:

        if len(fields) != len(values) or "password" in fields:
            return []

        matches_as_tuples = database.match(self.tablename, fields, values, return_columns=self.tablecolumns_for_search)
        matches_as_credentials = [CredentialHolder(email=match[0]) for match in matches_as_tuples]

        return matches_as_credentials

    def add_table_to_database(self, database: AbstractDatabase) -> None:
        database.create_table_if_non_existent(self.tablename, self.tablecolumns, self.tabletypes)

    def establich_interpreter_for_file(self, file) -> AbstractLineInterpreterCredential:

        for line in file.readlines():

            valid_interpreters = []

            for interpreter in self.line_interpreters:

                if interpreter.check_line(line):
                    valid_interpreters.append(interpreter)

            if len(valid_interpreters) == 1:
                interpreter = valid_interpreters[0]
                file.seek(0)
                return interpreter

        raise InterpreterNotFoundError("No valid interpreter was found")
