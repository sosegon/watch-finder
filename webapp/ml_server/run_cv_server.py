from threading import Thread
import numpy as np
import base64
import flask
import redis
import uuid
import time
import json
import sys
import io
import cv2
import pickle

IMAGE_DTYPE = "uint8"
IMAGE_SIZE = 300

# initialize constants used for server queuing
IMAGE_QUEUE = "image_queue"
BATCH_SIZE = 32
SERVER_SLEEP = 0.25
CLIENT_SLEEP = 0.25

app = flask.Flask(__name__)
db = redis.StrictRedis(host='localhost', port=6379, db=0)

def base64_encode_image(a):
	return base64.b64encode(a).decode('utf-8')

def base64_decode_image(a, dtype, shape):
	if sys.version_info.major == 3:
		a = bytes(a, encoding='utf-8')

	a = np.frombuffer(base64.decodestring(a), dtype=dtype)
	a = a.reshape(shape)

	return a

def prepare_image(image_gray, size):

	image_gray = make_square(image_gray)
	return cv2.resize(image_gray, (size, size))

def make_square(img):
	h, w = img.shape
	if h == w:
		return img
	elif w < h:
		n_img = np.ones((h, h)) * 255
		dif = h - w
		left = 0
		right = 0
		if dif % 2 == 0:
			left = int(dif / 2)
			right = left
		else:
			left = int(math.ceil(dif/2))
			right = left - 1
		# print("left {:d}, right {:d}".format(left, right))
		n_img[:, left:-right] = img

	elif w > h:
		n_img = np.ones((w, w)) * 255
		dif = w - h
		top = 0
		bottom = 0
		if dif % 2 == 0:
			top = int(dif / 2)
			bottom = top
		else:
			top = int(math.ceil(dif/2))
			bottom = top - 1
		# print("top {:d}, bottom {:d}".format(top, bottom))
		n_img[top:-bottom, :] = img

	return n_img

def search_process():
	descriptor = SIFTDescriptor(32)
	searcher = Searcher()

	# continues polling images to search
	while True:
		queue = db.lrange(IMAGE_QUEUE, 0, BATCH_SIZE - 1)
		results = {}

		for q in queue:
			q = json.loads(q.decode('utf-8'))
			image = base64_decode_image(q['image'], IMAGE_DTYPE, q['shape'])
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

class Searcher:
    def __init__(self, index_path="./features.pck"):
        self.index = pickle.loads(open(index_path, "rb").read())

    def search(self, query_features):
        results = {}

        for (k, features) in self.index.items():

            d = self.euclidean_distance(features, query_features)
            results[k] = d

        results = sorted([(v, k) for (k, v) in results.items()])

        return results

    def euclidean_distance(self, featuresA, featuresB):
        return np.linalg.norm(featuresA - featuresB)

class SIFTDescriptor:
    def __init__(self, vector_size):
        self.vector_size = vector_size
        self.sift = cv2.xfeatures2d.SIFT_create()

    def describe(self, image_gray):
        image = image_gray
        try:
            kps = self.sift.detect(image, None)
            kps = sorted(kps, key=lambda x: -x.response)[:self.vector_size]
            kps, dsc = self.sift.compute(image, kps)
            dsc = dsc.flatten()

            needed_size = (self.vector_size * 128) # 128 is the size of a SIFT descriptor
            if dsc.size < needed_size:
                dsc = np.concatenate([dsc, np.zeros(needed_size - dsc.size)])
        except cv2.error as e:
            print('Error: ', e)
            return None

        return dsc


if __name__ == '__main__':
	print('Starting cv model...')
	t = Thread(target=search_process, args=())
	t.daemon = True
	t.start()

	print('Starting web service...')
	app.run()
