import csv
import logging
import sys
import config
from tqdm import tqdm
from argparse import ArgumentParser
import redis

data_file = config.data_file
redis_client = None
jsonData = {}
vectorData = {}

def import_csv():
	logging.info("Import CSV file - ")
	logging.info(data_file)
	with open(data_file, encoding='utf-8') as csvFile:	
		reader = csv.DictReader(csvFile)
		for index, row in enumerate(reader, start=1):
			jsonData[index] = row
	logging.info("CSV imported, JSON created")

def push_redis_data():
	redis_client = redis.Redis(host=config.redis_host, port=config.redis_port, decode_responses=True)
	logging.info("push JSON data to Redis for cache hits")
	pipeline = redis_client.pipeline()
	for key, value in tqdm(jsonData.items()):
		redis_key = f"{{{config.redis_key}}}:{key:03}"
		pipeline.json().set(redis_key, "$", value)
		if key%50==0:
			pipeline.execute()

def set_logging(verbose):
	if verbose:
		logging.basicConfig(
			stream=sys.stdout, level=logging.INFO
		)
	else:
		logging.basicConfig(
			stream=sys.stdout, level=logging.ERROR
		)

def data_import():
	logging.info("Running data import.")
	import_csv()
	logging.info("push vectors to redis")
	push_redis_data()
	

if __name__ == '__main__':
	parser = ArgumentParser()
	parser.add_argument("-i", "--import-data", 
					    action="store_true", dest="data", default=False,
						help="import data from file into redis")
	parser.add_argument("-q", "--quiet",
						action="store_false", dest="verbose", default=True,
						help="don't print status messages to stdout")
	args = parser.parse_args()
	set_logging(args.verbose)
	if args.data:
		data_import()