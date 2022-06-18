================
credentials_tool
================

A command-line interface tool for handling credentials. Currently implements storing and comparing with a database.


* Free software: GNU General Public License v3

Install
--------
1. Clone the repository::

   $ git clone https://github.com/Synrom/credentials_tool.git

1. Go to the root folder of the project and execute::

   $ python setup.py install

2. Now you can execute the tool using::

   $ credentials_tool -h

Features
--------
1. read data from a file and match it with a database::

   $ credentials_tool -mf file1 file2 -db database.db

2. read data from a command line arguments and match it with a database::

   $ credentials_tool -mi "example1.mail@mail.com:password1" "example2.mail@mail.com:password2" -db database.db

3. read data from a file and insert it into a database::

   $ credentials_tool -if file1 file2 -db database.db

4. the CLI is built in a way to support all functionalities at the same time::

   $ credentials_tool -if insertfile1 insertfile2 -mf matchfile1 matchfile2 -mi "example1.mail@mail.com:password1"  -db database.db


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
