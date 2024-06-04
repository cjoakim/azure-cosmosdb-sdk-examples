# PowerShell script to delete/define the PostgreSQL baseball database.
# See the psql.ps1 script in this directory, which is invoked by this script.
# Chris Joakim, Microsoft

# Usage:
# > .\baseball_deldef.ps1 local postgres
# > .\baseball_deldef.ps1 flex postgres > tmp\flex_baseball_deldef.txt
# > .\baseball_deldef.ps1 cosmos citus > tmp\cosmos_baseball_deldef.txt

param(
    [Parameter()]
    [String]$env_name  = "<env>",
    [String]$db_name   = "<db>"
)

Write-Output "baseball_deldef"
.\psql.ps1 $env_name $db_name psql\baseball_deldef.sql
