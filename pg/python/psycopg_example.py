"""
Usage:
  python psycopg_example.py <func>
  -
  python psycopg_example.py check_environment_variables
  -
  python psycopg_example.py psycopg_example <envname> <dbname>
  python psycopg_example.py psycopg_example local postgres
  python psycopg_example.py psycopg_example cosmos citus
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import base64
import json
import os
import sys
import time
import traceback

from docopt import docopt

import psycopg

from pysrc.util.counter import Counter
from pysrc.util.fs import FS 
from pysrc.util.template import Template


class PGClient(object):

    def __init__(self, envname, dbname):
        self.envname = envname
        self.dbname  = dbname
        self.conn    = None
        self.cursor  = None

        # default to 'localhost'
        host     = "localhost"
        user     = os.environ['LOCAL_PG_USER']
        password = os.environ['LOCAL_PG_PASS']
        sslmode  = ""

        if envname == 'flex':
            host     = os.environ['AZURE_FLEX_PG_SERVER']
            user     = os.environ['AZURE_FLEX_PG_USER']
            password = os.environ['AZURE_FLEX_PG_PASS']
            sslmode  = "sslmode=require"
        elif envname == 'cosmos':
            host     = os.environ['AZURE_COSMOSDB_PG_FQNAME']
            user     = os.environ['AZURE_COSMOSDB_PG_USER']
            password = os.environ['AZURE_COSMOSDB_PG_PASS']
            sslmode  = "sslmode=require"

        print("PGClient#init - envname: {}, dbname: {}, host: {}".format(
            envname, dbname, host))

        # Build a connection string from the variables
        conn_string = "host={} user={} dbname={} password={} {}".format(
            host, user, dbname, password, sslmode)
        #print("PGClient#init - conn_string: {}".format(conn_string))
        
        self.conn = psycopg.connect(conninfo=conn_string)  # ("dbname=test user=postgres")
        if (self.conn != None):
            print("PGClient#init - connection created")
        else:
            print("PGClient#init - ERROR: connection NOT created")

    def get_cursor(self):
        self.cursor = self.conn.cursor()
        return self.cursor

    def close(self) -> None:
        """ commit the cursor and close the db connection, if they exist """
        if (self.cursor != None):
            self.cursor.close()
            print("PGClient#close - cursor closed")
        if (self.conn != None):
            self.conn.commit()
            self.conn.close()
            print("PGClient#close - connection closed")


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