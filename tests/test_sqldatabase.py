#!/usr/bin/env python

"""Tests for `sql_database` """


import unittest
import os

from credentials_tool.sqlite_database import SqliteDatabase


class TestSqlDatabase(unittest.TestCase):
    """Tests for `sql_database package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):

        if os.path.isfile("data/test_database.db"):
            os.remove("data/test_database.db")

        test_db = SqliteDatabase("data/test_database.db")

        test_db.create_table_if_non_existent("credentials", ("password", "email"), ("varchar(50)", "varchar(200)"))

        test_db.insert("credentials", ("hallo123", "max.leiwig@gmail.com"))
        test_db.insert("credentials", ("password", "max.leiwig@gmx.de"))
        test_db.insert("credentials", ("drowssap", "s6maleiw@uni-bonn.de"))
        test_db.insert("credentials", ("drowssap", "s6maleiw2@uni-bonn.de"))

        matches = test_db.match("credentials", ("password",), ("hallo123",))
        assert(matches == [('hallo123', 'max.leiwig@gmail.com')])
        matches = test_db.match("credentials", ("password",), ("drowssap",))
        assert(matches == [('drowssap', 's6maleiw@uni-bonn.de'), ('drowssap', 's6maleiw2@uni-bonn.de')])
