from threading import Thread
import numpy as np
import flask
import redis
import uuid
import time
import json
import cv2
import watch_finder_settings as settings
from common.vision import make_square, base64_encode_image

IMAGE_SIZE = settings.IMAGE_SIZE
IMAGE_QUEUE = settings.IMAGE_QUEUE
CLIENT_SLEEP = settings.CLIENT_SLEEP

app = flask.Flask(__name__)
db = redis.StrictRedis(host=settings.REDIS_HOST,
	port=settings.REDIS_PORT, db=settings.REDIS_DB)

def prepare_image(image_gray, size):
	image_gray = make_square(image_gray)
	return cv2.resize(image_gray, (size, size))

@app.route("/")
def homepage():
	return 'Welcome to watch-finder module!'

@app.route("/search", methods=['POST'])
def search():
	data = {'success': False}

	if flask.request.method == 'POST':
		if flask.request.files.get('image'):
			image = flask.request.files['image'].read()
			image = np.fromstring(image, np.uint8)
			image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)

			image = prepare_image(image, IMAGE_SIZE)
			shape = image.shape
			image = image.copy(order='C')

			k = str(uuid.uuid4())
			d = {'id': k, 'image': base64_encode_image(image), 'shape': shape}
			db.rpush(IMAGE_QUEUE, json.dumps(d))

			while True:
				output = db.get(k)

				if output is not None:
					output = output.decode('utf-8')
					data['predictions'] = json.loads(output)

					db.delete(k)
					break

				time.sleep(CLIENT_SLEEP)

			data['success'] = True

		return flask.jsonify(data)

if __name__ == '__main__':
	print('Starting web service...')
	app.run()
