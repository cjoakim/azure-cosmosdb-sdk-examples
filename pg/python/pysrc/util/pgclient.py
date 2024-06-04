import os
import sys
import traceback


import psycopg
from psycopg import connect, ClientCursor

# This class is used to interact with a PostgreSQL database, such as
# Azure Cosmos DB for PostgreSQL or Azure Database for PostgreSQL.
# Chris Joakim, Microsoft

class PGClient(object):

    def __init__(self, opts: dict = {}):
        """
        Establish a connection to a PostgreSQL database per the
        environment variables associated with the given environment name
        and database name.  These self-explanatory keys may be in the opts:
        - envname    (logical name of the environment - local, flex, or cosmos)
        - dbname
        - host
        - user
        - pass       (password)
        - sslmode    (a value such as either an empty string "" or "sslmode=require")
        - port       (default is 5432, specify a value such as 6432 for pgbouncer)

        If 'envname' is provided, then the host, user, pass, and sslmode
        will be derived given that value. 
        """
        envname  = self._opt("envname", opts)
        dbname   = self._opt("dbname", opts)
        host     = self._opt("host", opts)
        user     = self._opt("user", opts)
        password = self._opt("pass", opts)
        sslmode  = self._opt("sslmode", opts)
        port     = self._opt("port", opts)
        autocommit = False
        if "autocommit" in opts:
            autocommit = opts["autocommit"]

        try:
            if envname is not None:
                if envname == 'flex':
                    host     = os.environ['AZURE_FLEX_PG_SERVER']
                    user     = os.environ['AZURE_FLEX_PG_USER']
                    password = os.environ['AZURE_FLEX_PG_PASS']
                    sslmode  = "sslmode=require"
                elif envname == 'cosmos':
                    host     = os.environ['AZURE_COSMOSDB_PG_SERVER']
                    user     = os.environ['AZURE_COSMOSDB_PG_USER']
                    password = os.environ['AZURE_COSMOSDB_PG_PASS']
                    sslmode  = "sslmode=require"
                else:
                    # default to 'localhost'
                    host     = "localhost"
                    user     = os.environ['LOCAL_PG_USER']
                    password = os.environ['LOCAL_PG_PASS']
                    sslmode  = ""

            print("PGClient#init - envname: {}, dbname: {}, host: {}".format(
                envname, dbname, host))

            if port is not None:
                conn_string = "host={} port={} user={} dbname={} password={} {}".format(
                    host, port, user, dbname, password, sslmode)
            else:
                conn_string = "host={} user={} dbname={} password={} {}".format(
                    host, user, dbname, password, sslmode)
            print("PGClient#init - conn_string: {}".format(conn_string))
            
            self.conn = psycopg.connect(
                conninfo=conn_string,
                cursor_factory=ClientCursor,
                autocommit=autocommit)
            
            if (self.conn != None):
                print("PGClient#init - connection created")
            else:
                print("PGClient#init - ERROR: connection NOT created")
        except Exception as e:
            print("PGClient#init - Exception: {}".format(e))
            traceback.print_exc()

    def get_cursor(self):
        self.cursor = self.conn.cursor()
        return self.cursor

    def commit(self):
        if self.cursor != None:
            self.cursor.close()
        if self.conn != None:
            self.conn.commit()
    
    def close(self) -> None:
        """ close the cursor and commit/close the db connection, if they exist """
        if self.cursor != None:
            self.cursor.close()
            print("PGClient#close - cursor closed")
        if self.conn != None:
            self.conn.commit()
            self.conn.close()
            print("PGClient#close - connection closed")

    def _opt(self, name, opts):
        if name in opts:
            return opts[name]
        else:
            return None
        