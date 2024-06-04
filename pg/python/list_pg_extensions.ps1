# PowerShell script to list the PostgreSQL extensions in a database.
# See the psql.ps1 script in this directory, which is invoked by this script.
# Chris Joakim, Microsoft

# Usage:
# > .\list_pg_extensions.ps1 local postgres > tmp\local_extensions.txt
# > .\list_pg_extensions.ps1 flex postgres > tmp\flex_extensions.txt
# > .\list_pg_extensions.ps1 cosmos citus > tmp\cosmos_extensions.txt

param(
    [Parameter()]
    [String]$env_name  = "<env>",
    [String]$db_name   = "<db>"
)

# Usage: .\extensions.ps1 cosmos citus > tmp\extensions.txt

Write-Output "extensions"
.\psql.ps1 $env_name $db_name psql\extensions.sql
