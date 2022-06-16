"""Console script for credentials_tool."""
import argparse
import sys
import credentials_tool.tool as tool


def main():
    """Console script for credentials_tool."""
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()

    print(args)
    print("hab ich gelesen")

    tool.do_something()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
