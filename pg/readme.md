## Azure Cosmos DB PostgreSQL API, and PostgreSQL Flex

This directory contains examples for PostgreSQL, including:
- PostgreSQL on localhost
- Azure Database for PostgreSQL
- Azure Cosmos DB for PostgreSQL

## Documentation

### Flex

- https://learn.microsoft.com/en-us/azure/postgresql/



### Cosmos DB PostgreSQL

- https://learn.microsoft.com/en-us/azure/cosmos-db/postgresql/introduction

- https://docs.citusdata.com/en/v11.3/develop/integrations.html#differences-from-single-node-postgresql

- https://learn.microsoft.com/en-us/azure/cosmos-db/postgresql/quickstart-app-stacks-python

- https://devblogs.microsoft.com/cosmosdb/auto-scaling-azure-cosmos-db-for-postgresql-with-citus-grafana-azure-functions/


### Cosmos DB PostgreSQL - Best Practices


#### Scaling


#### CDC

- Fabric Mirroring 

- FLEX: https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/concepts-logical
  via https://github.com/2ndQuadrant/pglogical

- FLEX/STD: CREATE PUBLICATION newpub FOR TABLE public.users;

https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/concepts-logical


#### PgBouncer

- "Managed PgBouncer"
  - https://learn.microsoft.com/en-us/azure/cosmos-db/postgresql/concepts-connection-pool
  - It supports up to 2,000 simultaneous client connections.
  - https://learn.microsoft.com/en-us/azure/cosmos-db/postgresql/reference-parameters#managed-pgbouncer-parameters

  


### Python and psycopg (aka - psycopg3)

- psycopg is the replacement for psycopg2
- https://pypi.org/project/psycopg/
- https://www.psycopg.org/psycopg3/docs/api/

---

### Environment Variables

The following environment variables are used by the scripts and code
in this project.  Set these with your appropriate values.

```
Name                       Example Value
-----------------------    --------------
LOCAL_PG_USER              postgres
LOCAL_PG_PASS              <secret>

AZURE_FLEX_PG_SERVER       gbbchris.postgres.database.azure.com
AZURE_FLEX_PG_USER         chjoakim
AZURE_FLEX_PG_PASS         <secret>

AZURE_COSMOSDB_PG_SERVER   c-gbbchris.5rmXl6v48ge55r.postgres.cosmos.azure.com
AZURE_COSMOSDB_PG_USER     citus
AZURE_COSMOSDB_PG_PASS     <secret>
```

---

## Command-Line Client:

Install PostgreSQL 16 locally and add C:\Program Files\PostgreSQL\16\bin
to your PATH environment variable.  This directory is where the **psql**
command-line client is located.

### Helper Script - .\psql.ps1 local postgres

PowerShell script **psql.ps1** exists in this directory and can
be used as follows to connect to one of several PostgreSQL databases
per your command line arguments and environment variables.

```
> .\psql.ps1 local postgres
> .\psql.ps1 local dev
```

### Example psql terminal use 

```
> psql --help

> psql -d movies -f load_sample.sql    # to load a datafile
```

```
insert into customers (customer_id, customer_name, phone, birth_date, balance) values (5, 'sam', '867-5309', '1988-01-01', 0.0);

command          description
---------------  ------------------------------------
\q               quit the client program
\l               list databases
\c   dbname      use the given database
\connect dbname  use the given database
\d               list tables, or "List of relations"
\d               show tables
\d customers     describe the customers table
\du              list roles
\dt              show all the tables in db
\dt *.*          show all the tables in system & db
\di              list indexes
\dv              list views
\i filename      to run (include) a script file of SQL commands
\?               show the list of \postgres commands
\h               show the list of SQL commands
\h command       show syntax on this SQL command
\x on            Turn on mysql-like \G output
\x off           Turn off mysql-like \G output

(END) simply use ‘q’ to quit the viewing and came back to the prompt.
```

---

## Azure Cosmos DB for PostgreSQL 

Show the PG version.

```
citus=> SHOW server_version;
          server_version
----------------------------------
 16.3 (Ubuntu 16.3-1.pgdg20.04+1)
(1 row)
```

Initially there are no distributed tables.

```
citus=> SELECT * FROM citus_tables;
 table_name | citus_table_type | distribution_column | colocation_id | table_size | shard_count | table_owner | access_method
------------+------------------+---------------------+---------------+------------+-------------+-------------+---------------
(0 rows)
```
