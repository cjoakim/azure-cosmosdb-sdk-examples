import os
import sys
import traceback

import psycopg

# This class is used to interact with a PostgreSQL database, such as
# Azure Cosmos DB for PostgreSQL or Azure Database for PostgreSQL.
# Chris Joakim, Microsoft

class PGClient(object):

    def __init__(self, envname, dbname, override_opts: dict = None):
        """
        Establish a connection to a PostgreSQL database per the
        environment variables associated with the given environment name
        and database name.
        
        However, the optional 'override_opts' parameter may be used to pass
        in the connection options directly.  The required keys are:
        host, user, dbname, password, and sslmode.
        """
        self.envname = envname
        self.dbname  = dbname
        self.conn    = None
        self.cursor  = None

        try:
            if override_opts is not None:
                host = override_opts['host']
                user = override_opts['user']
                dbname = override_opts['dbname']
                password = override_opts['password']
                sslmode = override_opts['sslmode']
            else:
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

            conn_string = "host={} user={} dbname={} password={} {}".format(
                host, user, dbname, password, sslmode)
            #print("PGClient#init - conn_string: {}".format(conn_string))
            
            self.conn = psycopg.connect(conninfo=conn_string)  # ("dbname=test user=postgres")
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

    def close(self) -> None:
        """ close the cursor and commit/close the db connection, if they exist """
        if (self.cursor != None):
            self.cursor.close()
            print("PGClient#close - cursor closed")
        if (self.conn != None):
            self.conn.commit()
            self.conn.close()
            print("PGClient#close - connection closed")
