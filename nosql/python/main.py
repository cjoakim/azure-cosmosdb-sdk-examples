"""
Usage:
  python main.py <func> <params>
  python main.py display_azure_env_vars
  python main.py load_nosql_airports <dbname> <container-name>
  python main.py load_nosql_airports dev airports
  python main.py logical_partition_calc <avg_doc_size>
  python main.py logical_partition_calc 1024
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

# import the necessary python standard libraries
import base64
import json
import sys
import time
import os
import traceback

from docopt import docopt
from dotenv import load_dotenv

# import the custom python modules from within the pysrc directory
from pysrc.bytes import Bytes
from pysrc.cosmos import Cosmos
from pysrc.counter import Counter
from pysrc.env import Env
from pysrc.fs import FS
from pysrc.storage import Storage
from pysrc.system import System


def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version="1.0.0")
    print(arguments)


def display_azure_env_vars():
    for name in sorted(os.environ.keys()):
        if name.startswith("AZURE_"):
            print("{}: {}".format(name, os.environ[name]))


def load_nosql_airports(dbname, cname):
    print("load_nosql_airports dbname: {} cname: {}".format(dbname, cname))
    lines = FS.read_lines("../../data/openflights/json/airports.json")
    for line in lines:
        if len(line) > 0:
            print(line)


def logical_partition_calc(avg_doc_size):
    gb = Bytes.gigabyte()
    gb20 = float(gb * 20.0)
    docs_per_logical_partition = gb20 / avg_doc_size

    print("kilobyte:     {}".format(Bytes.kilobyte()))
    print("megabyte:     {}".format(Bytes.megabyte()))
    print("gigabyte:     {}".format(gb))
    print("20 gigabytes: {}".format(gb20))
    print("docs_per_logical_partition: {}".format(docs_per_logical_partition))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_options("Error: missing function argument")
        sys.exit(1)
    try:
        load_dotenv(override=True)
        func = sys.argv[1].lower()
        if func == "display_azure_env_vars":
            display_azure_env_vars()
        elif func == "load_nosql_airports":
            dbname, cname = sys.argv[2], sys.argv[3]
            load_nosql_airports(dbname, cname)
        elif func == "logical_partition_calc":
            avg_doc_size = float(sys.argv[2])
            logical_partition_calc(avg_doc_size)
        else:
            print_options("Error: invalid function: {}".format(func))
    except Exception as e:
        print(str(e))
        print(traceback.format_exc())
