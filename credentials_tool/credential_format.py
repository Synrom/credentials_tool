from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod
import hashlib
import base64
import re
import os

from credentials_tool.abstract_classes import AbstractFormat, AbstractDatabase
from credentials_tool.errors import InterpreterNotFoundError


@dataclass
class CredentialHolder():
    email: str
    password: str = ""

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


class AbstractLineInterpreterCredential(ABC):

    @abstractmethod
    def check_line(self, line: str) -> bool:
        pass

    @abstractmethod
    def interpret_item(self, line: str) -> CredentialHolder:
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

    def interpret_item(self, item: str) -> CredentialHolder:

        item_splited = item.split(":")

        password = item_splited[0].strip()
        mail = item_splited[1].strip()

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

    def interpret_item(self, item: str) -> CredentialHolder:

        item_splited = item.split(":")

        mail = item_splited[0].strip()
        password = item_splited[1].strip()

        return CredentialHolder(email=mail, password=password)


class CredentialFormat(AbstractFormat):

    def table_name(self):
        return "credentials_email_and_password"

    def table_columns(self):
        return ("email", "password", "salt")

    def table_types(self):
        return ("varchar(320)", "varchar(172)", "varchar(44)")

    def __init__(self, email_regex: str = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"):

        self.line_interpreters = [LineInterpreterMailPassword(email_regex), LineInterpreterPasswordMail(email_regex)]
        self.table_columns_for_search = ("email",)
        self.table_salt_position = 2
        self.table_password_position = 1

    def read_data_from_file(self, filename: str) -> list[CredentialHolder]:

        f = open(filename, "r")
        interpreter = self.establich_interpreter_for_itemlist(f.readlines())

        f.seek(0)

        credentials = []

        for line in f.readlines():

            credentials.append(interpreter.interpret_item(line))

        f.close()

        return credentials

    def read_data_from_itemlist(self, itemlist: list) -> list[CredentialHolder]:

        interpreter = self.establich_interpreter_for_itemlist(itemlist)

        credentials = []

        for item in itemlist:

            credentials.append(interpreter.interpret_item(item))

        return credentials

    def add_data_to_database(self, database: AbstractDatabase, credentials: list[CredentialHolder]) -> None:

        for credential in credentials:

            database.insert(self.table_name(), credential.as_tuple_with_hashed_password())

    def match_data_with_database(self, database: AbstractDatabase, credentials: list[CredentialHolder]) -> list:

        matches = []

        for credential in credentials:

            search = {}
            credential_dict = asdict(credential)

            for column in self.table_columns_for_search:
                search.update({column: credential_dict[column]})

            matches_of_credential = database.match(self.table_name(), search, return_columns=self.table_columns())

            for match_of_credential in matches_of_credential:

                raw_salt = base64.b64decode(match_of_credential[self.table_salt_position])

                if credential.get_hashed_password(raw_salt) == match_of_credential[self.table_password_position]:
                    matches.append(credential)

        return matches

    def add_table_to_database(self, database: AbstractDatabase) -> None:
        database.create_table_if_non_existent(self.table_name(), dict(zip(self.table_columns(), self.table_types())))

    def establich_interpreter_for_itemlist(self, items: list) -> AbstractLineInterpreterCredential:

        for item in items:

            valid_interpreters = []

            for interpreter in self.line_interpreters:

                if interpreter.check_line(item):
                    valid_interpreters.append(interpreter)

            if len(valid_interpreters) == 1:
                interpreter = valid_interpreters[0]
                return interpreter

        raise InterpreterNotFoundError("No valid interpreter was found")
