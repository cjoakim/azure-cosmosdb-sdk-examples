"""
Usage:
  python psycopg_example.py <func>
  -
  python psycopg_example.py check_environment_variables
  -
  python psycopg_example.py psycopg_example <envname> <dbname>
  python psycopg_example.py psycopg_example local postgres
  python psycopg_example.py psycopg_example flex postgres
  python psycopg_example.py psycopg_example cosmos citus
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import os
import sys
import time
import traceback

from docopt import docopt

from pysrc.util.counter import Counter
from pysrc.util.fs import FS 
from pysrc.util.pgclient import PGClient

def print_options(msg=None):
    if msg:
        print(msg)
    arguments = docopt(__doc__, version='1.0.0')
    print(arguments)

def check_environment_variables():
    home = os.environ['USERNAME']
    env_vars = [
        'USERNAME',
        'LOCAL_PG_USER',
        'LOCAL_PG_PASS',
        'AZURE_FLEX_PG_SERVER',
        'AZURE_FLEX_PG_USER',
        'AZURE_FLEX_PG_PASS',
        'AZURE_COSMOSDB_PG_USER',
        'AZURE_COSMOSDB_PG_PASS'
    ]
    for env_var in env_vars:
        print('check_env, {}: {}'.format(env_var, os.environ[env_var]))

def psycopg_example(envname, dbname):
    print('psycopg_example')
    client = PGClient(envname, dbname)
    cursor = client.get_cursor()

    # Drop previous table of same name if one exists
    cursor.execute("DROP TABLE IF EXISTS pharmacy;")
    print("Finished dropping table (if existed)")

    # Create a table
    cursor.execute("CREATE TABLE pharmacy (pharmacy_id integer, pharmacy_name text, city text, state text, zip_code integer);")
    print("Finished creating table")

    # Create a index
    cursor.execute("CREATE INDEX idx_pharmacy_id ON pharmacy(pharmacy_id);")
    print("Finished creating index")

    # Insert some data into the table
    cursor.execute("INSERT INTO pharmacy (pharmacy_id,pharmacy_name,city,state,zip_code) VALUES (%s, %s, %s, %s,%s);", (1,"Target","Sunnyvale","CA",94001))
    cursor.execute("INSERT INTO pharmacy (pharmacy_id,pharmacy_name,city,state,zip_code) VALUES (%s, %s, %s, %s,%s);", (2,"CVS","Davidson","NC",28036))
    print("Inserted 2 rows of data")

    client.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_options(None)
    else:
        func = sys.argv[1].lower()
        if func == 'check_environment_variables':
            check_environment_variables()
        elif func == 'psycopg_example':
            envname, dbname = sys.argv[2], sys.argv[3]
            psycopg_example(envname, dbname)
        else:
            print_options('Error: invalid function: {}'.format(func))
