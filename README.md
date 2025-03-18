# REDIS-API

This Python and JSON code utilizes a custom framework to digest a JSON-based configuration file (located in ./json) to execute commands via the Redis REST API. 

## Usage
Currently, the Python script requires environment variables to exist. Copy the .env.template file to .env and fill in the variable values for connecting to Redis then execute the .env file:

```
$source .env
```

Invoke the framework with the following parameters:
- Config input file - the json file path containing the configuration for the API call. 
- JSON output file - this file will contain the output from the Redis server
- Dry-run flag set to True - used with PUT or POST operations, thus flag will toggle the execution OR dry-run of the command

Examples:
```
$python3 redis-invocation-framework.py json/cluster_summary.json out/cluster_output.json
$python3 redis-invocation-framework.py json/create_database.json out/create_db_output.json True