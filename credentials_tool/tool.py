"""Main module."""
from credentials_tool.sqlite_database import SqliteDatabase
from credentials_tool.credential_format import CredentialFormat


def do_something():
    db = SqliteDatabase("data/database.db")
    frmtMgr = CredentialFormat()
    print(db)
    print(frmtMgr)
