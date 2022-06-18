=====
Usage
=====

To use credentials_tool in a project::

    import credentials_tool

To use the credentials_tool programm::

    $ credentials_tool -h
    usage: credentials_tool [-h] [-if [filename ...]] [-db database] [-mf [filename ...]] [-mi [item ...]]

    A command-line interface tool for handling credentials. Currently implements storing and comparing with a database.

    optional arguments:
      -h, --help            show this help message and exit
      -if [filename ...], --input-files [filename ...]
                            read data from files
      -db database, --database database
                            use this file as database (default: credentials.db)
      -mf [filename ...], --match-files [filename ...]
                            match database with these files (after inserting the files specified by -in)
      -mi [item ...], --match-items [item ...]
                            match database with these items (after inserting the files specified by -in).The items are given either in the format <email>:<password> or <password>:<email>, but not both

