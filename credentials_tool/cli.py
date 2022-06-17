"""Console script for credentials_tool."""
import argparse
import sys
import credentials_tool.tool
import credentials_tool.sqlite_database
import credentials_tool.credential_format
import credentials_tool.errors


def main():
    """Console script for credentials_tool."""
    description = "A command-line interface tool for handling credentials. Currently implements storing and comparing with a database."
    parser = argparse.ArgumentParser(description=description)

    help_file = "read data from file"
    parser.add_argument("-in", metavar="filename", type=str, nargs="*", dest="insert_filenames", help=help_file)

    help_db = "use this file as database (default: credentials.db)"
    parser.add_argument("-db", metavar="database", type=str, default="credentials.db", dest="db", help=help_db)

    help_match = "match database with this file (after inserting the files specified by -in)"
    parser.add_argument("-match", metavar="filename", type=str, nargs="*", dest="match_filenames", help=help_match)

    args = parser.parse_args()

    try:
        database = credentials_tool.sqlite_database.SqliteDatabase(args.db)

    except credentials_tool.errors.DatabaseOpeningError:
        print("Cant open "+args.db)
        return

    print("using "+args.db+" as database")

    credential_format = credentials_tool.credential_format.CredentialFormat()

    for insert_filename in args.insert_filenames:
        credentials_tool.tool.read_data_from_file_to_database(credential_format, database, insert_filename)

    for match_filename in args.match_filenames:
        credentials_tool.tool.match_data_from_file_with_database(credential_format, database, match_filename)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
