"""Console script for credentials_tool."""
import argparse
import sys
import credentials_tool.tool
import credentials_tool.sqlite_database
import credentials_tool.credential_format
import credentials_tool.errors


def main(command=sys.argv[1:]):
    """Console script for credentials_tool."""
    description = "A command-line interface tool for handling credentials. Currently implements storing and comparing with a database."
    parser = argparse.ArgumentParser(description=description)

    help_file = "read data from files"
    parser.add_argument("-in", metavar="filename", type=str, nargs="*", dest="insert_filenames", help=help_file)

    help_db = "use this file as database (default: credentials.db)"
    parser.add_argument("-db", metavar="database", type=str, default="credentials.db", dest="db", help=help_db)

    help_match = "match database with these files (after inserting the files specified by -in)"
    parser.add_argument("-matchfiles", metavar="filename", type=str, nargs="*", dest="match_filenames", help=help_match)

    help_match = "match database with these items (after inserting the files specified by -in)."
    help_match += "The items are given either in the format <email>:<password> or <password>:<email>, but not both"
    parser.add_argument("-matchitems", metavar="item", type=str, nargs="*", dest="match_items", help=help_match)

    args = parser.parse_args(command)

    try:
        database = credentials_tool.sqlite_database.SqliteDatabase(args.db)

    except credentials_tool.errors.DatabaseOpeningError:
        print("Cant open "+args.db)
        return

    print("using "+args.db+" as database")

    credential_format = credentials_tool.credential_format.CredentialFormat()

    if args.insert_filenames:
        for insert_filename in args.insert_filenames:
            credentials_tool.tool.read_data_from_file_to_database(credential_format, database, insert_filename)

    if args.match_filenames:
        for match_filename in args.match_filenames:
            credentials_tool.tool.match_data_from_file_with_database(credential_format, database, match_filename)

    if args.match_items:
        credentials_tool.tool.match_data_from_itemlist_with_database(credential_format, database, args.match_items)

    database.commit()
    database.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
