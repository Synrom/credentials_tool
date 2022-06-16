#!/usr/bin/env python

"""Tests for `credentials_format` """


import unittest
import os

from credentials_tool.sqlite_database import SqliteDatabase
from credentials_tool.credential_format import CredentialFormat, CredentialHolder


class TestCredentialsFormat(unittest.TestCase):
    """Tests for `sql_database package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):

        if os.path.isfile("data/test_database.db"):
            os.remove("data/test_database.db")

        with open("data/test_credentials1", "w") as f:
            f.write("max.leiwig@gmail.com:passwort123\n")
            f.write("max.leiwig@gmx.de:dieisteinpassswort\n")
            f.write("s6maleiw@uni-bonn.de:sehrsicherespasswort\n")

        with open("data/test_credentials2", "w") as f:
            f.write("password:max2.leiwig@gmail.com\n")
            f.write("diesisteinpassword:max2.leiwig@gmx.de\n")
            f.write("sehrsicherespasswort:s7maleiw@uni-bonn.de\n")

        with open("data/test_match", "w") as f:
            f.write("max.leiwig@gmail.com:passwort123\n")
            f.write("max2.leiwig@gmail.com:password\n")
            f.write("s6maleiw@uni-bonn.de:adsfasfsda\n")

        test_db = SqliteDatabase("data/test_database.db")

        test_format = CredentialFormat()

        test_format.add_table_to_database(test_db)

        credentials1 = test_format.read_data_from_file("data/test_credentials1")

        assert(credentials1 == [
            CredentialHolder(email='max.leiwig@gmail.com', password='passwort123'),
            CredentialHolder(email='max.leiwig@gmx.de', password='dieisteinpassswort'),
            CredentialHolder(email='s6maleiw@uni-bonn.de', password='sehrsicherespasswort')
            ])

        test_format.add_data_to_database(test_db, credentials1)

        credentials2 = test_format.read_data_from_file("data/test_credentials2")

        assert(credentials2 == [
            CredentialHolder(email='max2.leiwig@gmail.com', password='password'),
            CredentialHolder(email='max2.leiwig@gmx.de', password='diesisteinpassword'),
            CredentialHolder(email='s7maleiw@uni-bonn.de', password='sehrsicherespasswort')
            ])

        test_format.add_data_to_database(test_db, credentials2)

        matches = test_format.match_fields_with_database(test_db, ("email",), ("s6maleiw@uni-bonn.de",))

        assert(matches == [CredentialHolder(email='s6maleiw@uni-bonn.de', password='')])

        credentials_match = test_format.read_data_from_file("data/test_match")
        matches = test_format.match_data_with_database(test_db, credentials_match)

        assert(matches == [
            CredentialHolder(email='max.leiwig@gmail.com', password='passwort123'),
            CredentialHolder(email='max2.leiwig@gmail.com', password='password')
            ])
