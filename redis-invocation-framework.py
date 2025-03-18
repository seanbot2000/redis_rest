import json
import requests
import argparse
import urllib3
import config

class RedisInvocationFramework:
    def __init__(self, config_file):
        urllib3.disable_warnings()
        with open(config_file, 'r') as file:
            self.config = json.load(file)
            self.auth = (config.redis_user, config.redis_password)
            self.url = config.redis_host
            self.port = config.redis_port
    
    def invoke(self, dry_run):
        final_data = dict()
        for api_call in self.config['api']:
            url = f"https://{self.url}:{self.port}{api_call['endpoint']}"
            name = api_call.get('name')
            method = api_call['method']
            headers = api_call.get('headers', {})
            params = api_call.get('params', {})
            json_data = api_call.get('json', {})
            #need to add dry_run when exists to query string
            if(dry_run == 'True'):
               params['dry_run'].update(True)

            if method == 'GET':
                response = requests.get(url=url, headers=headers, verify=False, auth=self.auth)
            
            if method == 'POST':
                response = requests.post(method, url, headers=headers, params=params, auth=self.auth, json=json_data, verify=False)

            # need to add loads and dumps to append data for coherent JSON
            final_data[name] = response.json()
            
        return json.dumps(final_data, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a config file to call Redis API.")
    parser.add_argument("infile", type=str, help="The name of the file to process")
    parser.add_argument("outfile", type=str, help="The name of the file in which to store results")
    parser.add_argument("--dry_run", type=bool, required=False, help="Add dry_run=True to validate the post data without executing the command")
    args = parser.parse_args()

    infile = args.infile
    outfile = args.outfile
    dry_run = args.dry_run
    
    framework = RedisInvocationFramework(infile)
    json = framework.invoke(dry_run)

    with open(outfile, "w") as f:
        f.write(json)


    