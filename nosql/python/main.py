"""
Usage:
  python main.py <func> <params>
  python main.py display_azure_env_vars
  python main.py list_databases_and_containers > tmp/list_databases_and_containers.txt
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
import uuid

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

def initialize_cosmos_object():
    opts = dict()
    opts['url'] = os.environ["AZURE_COSMOSDB_NOSQL_URI"]
    opts['key'] = os.environ["AZURE_COSMOSDB_NOSQL_RW_KEY1"]
    opts['enable_query_metrics'] = True
    return Cosmos(opts)

def list_databases_and_containers():
    cosmos = initialize_cosmos_object()

    for db in cosmos.list_databases():
        dbname = db['id']
        print("----- database: {}".format(dbname))
        print(json.dumps(db, sort_keys=False, indent=2))
        print("")

        print("----- listing containers in datbase: {}".format(dbname))
        cosmos.set_db(dbname)
        for c in cosmos.list_containers():
            print(json.dumps(c, sort_keys=False, indent=2))
            print("")

def load_nosql_airports(dbname, cname):
    print("load_nosql_airports dbname: {} cname: {}".format(dbname, cname))
    lines = FS.read_lines("../../data/openflights/json/airports.json")
    print("airport lines read: {}".format(len(lines)))

    cosmos = initialize_cosmos_object()
    cosmos.set_db(dbname)
    cosmos.set_container(cname)

    for idx, line in enumerate(lines):
        try:
            doc = json.loads(line)
            doc['id'] = str(uuid.uuid4())
            rdoc = cosmos.upsert_doc(doc)
            print("upserted doc idx, id: {} {}".format(idx, rdoc['id']))
        except Exception as e:
            print(str(e))

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
        elif func == "list_databases_and_containers":
            list_databases_and_containers()
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
