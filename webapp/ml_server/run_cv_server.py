import redis
import time
import json
import watch_finder_settings as settings
from common.vision import SIFTDescriptor, Searcher, base64_decode_image1

IMAGE_DTYPE = settings.IMAGE_DTYPE
IMAGE_QUEUE = settings.IMAGE_QUEUE
BATCH_SIZE = settings.BATCH_SIZE
SERVER_SLEEP = settings.SERVER_SLEEP
SIFT_DB = settings.SIFT_DB

db = redis.StrictRedis(host=settings.REDIS_HOST,
	port=settings.REDIS_PORT, db=settings.REDIS_DB)

def search_process(db_path):
	descriptor = SIFTDescriptor(32)
	searcher = Searcher(db_path)

	# continues polling images to search
	while True:
		queue = db.lrange(IMAGE_QUEUE, 0, BATCH_SIZE - 1)
		results = {}

		for q in queue:
			q = json.loads(q.decode('utf-8'))
			image = base64_decode_image1(q['image'], IMAGE_DTYPE, q['shape'])
			features = descriptor.describe(image)
			query_results = searcher.search(features)
			results[q["id"]] = query_results

		if len(results) > 0:
			for (imageID, result) in results.items():
				output = []

				five_results = result[:5]
				alikes = []
				for r in five_results:
					alikes.append(r[-1].split('/')[-1])

				output.append({'imageID': imageID, 'results': alikes})

				db.set(imageID, json.dumps(output))

			db.ltrim(IMAGE_QUEUE, len(results), -1)

		time.sleep(SERVER_SLEEP)

if __name__ == '__main__':
	# print('Starting cv model...')
	# t = Thread(target=search_process, args=(db_path,))
	# t.daemon = True
	# t.start()
	search_process(SIFT_DB)
