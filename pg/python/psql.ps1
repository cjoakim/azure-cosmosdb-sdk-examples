# PowerShell script to easily connect to a PostgreSQL database
# using the psql command line tool and simple CLI arguments.
# Chris Joakim, Microsoft

param(
    [Parameter()]
    [String]$env_name  = "",
    [String]$db_name   = "",
    [String]$psql_file = ""
)

$h=""
$p="5432"
$user="<user>"
$pass="<pass>"
$ssl=""

if ('local' -eq $env_name) {
    $h="localhost"
    $user=$env:LOCAL_PG_USER
    $pass=$env:LOCAL_PG_PASS
}
elseif ('flex' -eq $env_name) {
    $h=$env:AZURE_FLEX_PG_SERVER
    $user=$env:AZURE_FLEX_PG_USER
    $pass=$env:AZURE_FLEX_PG_PASS
    $ssl="sslmode=require"
}
elseif ('cosmos' -eq $env_name) {
    if ('citus' -ne $db_name) {
        Write-Output "WARNING: 'citus' is the only allowed database name for Azure Cosmos DB / PostgreSQL"
    }
    $h=$env:AZURE_COSMOSDB_PG_SERVER
    $user=$env:AZURE_COSMOSDB_PG_USER
    $pass=$env:AZURE_COSMOSDB_PG_PASS
    $ssl="sslmode=require"
}
else {
    Write-Output "unknown env_name $env_name, terminating"
    Write-Output ""
    Write-Output "Usage:"
    Write-Output ".\psql.ps1 <env> <db> - where env is local, flex, or cosmos"
    Write-Output ".\psql.ps1 local postgres"
    Write-Output ".\psql.ps1 local dev"
    Write-Output ".\psql.ps1 flex postgres"
    Write-Output ".\psql.ps1 cosmos citus"
    Write-Output ""
    Exit
}

if ("" -eq $psql_file) {
    # This path is for opening a psql terminal session
    Write-Output "connecting to host: $h, db: $db_name, user: $user"
    $psql_args="host=$h port=$p dbname=$db_name user=$user password=$pass $ssl"
    Write-Output $psql_args
    psql "$psql_args"
}
else {
    # This path is for executing a batch file of SQL commands using psql
    Write-Output "connecting to host: $h, db: $db_name, user: $user, using file: $psql_file"
    $psql_args="host=$h port=$p dbname=$db_name user=$user password=$pass $ssl"
    psql -f $psql_file "$psql_args"
}
