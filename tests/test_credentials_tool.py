#!/usr/bin/env python

"""Tests for `credentials_format` """


import unittest
import os

from credentials_tool.sqlite_database import SqliteDatabase
from credentials_tool.credential_format import CredentialFormat
from credentials_tool.tool import match_data_from_file_with_database, match_data_from_itemlist_with_database
from credentials_tool.tool import read_data_from_file_to_database


class TestCredentialsFormat(unittest.TestCase):
    """Tests for `sql_database package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):

        if os.path.isfile("tests/data/temporary_test_database.db"):
            os.remove("tests/data/temporary_test_database.db")

        # with open("tests/data/test_credentials1", "w") as f:
        #     f.write("max.leiwig@gmail.com:passwort123\n")
        #     f.write("max.leiwig@gmx.de:dieisteinpassswort\n")
        #     f.write("s6maleiw@uni-bonn.de:sehrsicherespasswort\n")

        # with open("tests/data/test_credentials2", "w") as f:
        #     f.write("password:max2.leiwig@gmail.com\n")
        #     f.write("diesisteinpassword:max2.leiwig@gmx.de\n")
        #     f.write("sehrsicherespasswort:s7maleiw@uni-bonn.de\n")

        # with open("tests/data/test_match", "w") as f:
        #     f.write("max.leiwig@gmail.com:passwort123\n")
        #     f.write("max2.leiwig@gmail.com:password\n")
        #     f.write("s6maleiw@uni-bonn.de:adsfasfsda\n")

        test_db = SqliteDatabase("tests/data/temporary_test_database.db")

        test_format = CredentialFormat()

        read_data_from_file_to_database(test_format, test_db, "tests/data/test_credentials1")
        read_data_from_file_to_database(test_format, test_db, "tests/data/test_credentials2")

        itemlist = [
                "s6maleiw@uni-bonn.de:sehrsicherespasswort",
                "max.leiwig@gmx.de:dieisteinpassswort",
                "max.leiwig@gmail.com:falschespasswort"
                ]

        match_data_from_itemlist_with_database(test_format, test_db, itemlist)

        match_data_from_file_with_database(test_format, test_db, "tests/data/test_match")

        test_db.close()
