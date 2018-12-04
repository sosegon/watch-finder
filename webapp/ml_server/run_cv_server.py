#!/mnt/linux_shared/shared/lwork/watch-finder/webapp/python
############################################################################
# This script run as a service, it works with the full path to the symlink #
############################################################################

import redis
import time
import json
import logging
import sys
import logging.handlers
import watch_finder_settings as settings
from common.vision import SIFTDescriptor, Searcher, base64_decode_image_server

IMAGE_DTYPE = settings.IMAGE_DTYPE
IMAGE_QUEUE = settings.IMAGE_QUEUE
BATCH_SIZE = settings.BATCH_SIZE
SERVER_SLEEP = settings.SERVER_SLEEP
SIFT_DB = settings.SIFT_DB

LOG_FILENAME = "/tmp/cv_server.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

db = redis.StrictRedis(host=settings.REDIS_HOST,
	port=settings.REDIS_PORT, db=settings.REDIS_DB)

def search_process(db_path):
	descriptor = SIFTDescriptor(32)
	searcher = Searcher(db_path)

	# continues polling images to search
	while True:
		logger.info("Runnig cv server")
		queue = db.lrange(IMAGE_QUEUE, 0, BATCH_SIZE - 1)
		results = {}

		for q in queue:
			q = json.loads(q.decode('utf-8'))
			image = base64_decode_image_server(q['image'], IMAGE_DTYPE, q['shape'])
			features = descriptor.describe(image)
			query_results = searcher.search(features)
			results[q["id"]] = query_results

		if len(results) > 0:
			for (imageID, result) in results.items():
				output = []

				five_results = result[:5]
				alikes = {}
				for r in five_results:
					watch_name = r[-1].split('/')[-1]
					# alikes[watch_name] = get_encoded_image(watch_name)
					alikes[watch_name] = r[-1]

				output.append({'imageID': imageID, 'results': alikes})

				db.set(imageID, json.dumps(output))

			db.ltrim(IMAGE_QUEUE, len(results), -1)

		time.sleep(SERVER_SLEEP)

# Logger from http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/
# Make a class we can use to capture stdout and sterr in the log
class MyLogger(object):
    def __init__(self, logger, level):
        """Needs a logger and a logger level."""
        self.logger = logger
        self.level = level

    def write(self, message):
        # Only log if there is a message (not just a new line)
        if message.rstrip() != "":
            self.logger.log(self.level, message.rstrip())

if __name__ == '__main__':
	# Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
	# Give the logger a unique name (good practice)
	logger = logging.getLogger(__name__)
	# Set the log level to LOG_LEVEL
	logger.setLevel(LOG_LEVEL)
	# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
	handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
	# Format each log message like this
	formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
	# Attach the formatter to the handler
	handler.setFormatter(formatter)
	# Attach the handler to the logger
	logger.addHandler(handler)

	# Replace stdout with logging to file at INFO level
	sys.stdout = MyLogger(logger, logging.INFO)
	# Replace stderr with logging to file at ERROR level
	sys.stderr = MyLogger(logger, logging.ERROR)

	search_process(SIFT_DB)
	# while True:
	# 	logger.info("Testing this logger in cv")
