import cv2
import pickle
import numpy as np

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
            if dsc is not None:
                dsc = dsc.flatten()
            else:
                raise ValueError("No descriptor found for image")

            needed_size = (self.vector_size * 128) # 128 is the size of a SIFT descriptor
            if dsc.size < needed_size:
                dsc = np.concatenate([dsc, np.zeros(needed_size - dsc.size)])
        except cv2.error as e:
            print('Error: ', e)
            return None

        return dsc

class Searcher:
    def __init__(self, index_path):
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

def make_square(img):
    shape = img.shape

    if len(shape) == 2:
        h, w = shape
        c = 1
    elif len(shape) == 3:
        h, w, c = shape
    else:
        raise ValueError('Not valid image shape: {}'.format(shape))

    if h == w:
        return img
    elif w < h:
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
        if c == 1:
            n_img = np.ones((h, h)) * 255
            n_img[:, left:-right,] = img
        else:
            n_img = np.ones((h, h, c)) * 255
            n_img[:, left:-right, :] = img

    elif w > h:
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
        if c == 1:
            n_img = np.ones((w, w)) * 255
            n_img[top:-bottom, :] = img
        else:
            n_img = np.ones((w, w, c)) * 255
            n_img[top:-bottom, :, :] = img

    return n_img

def base64_encode_image(a):
    return base64.b64encode(a).decode('utf-8')

def base64_decode_image(a, dtype, shape):
    if sys.version_info.major == 3:
        a = bytes(a, encoding='utf-8')

    a = np.frombuffer(base64.decodestring(a), dtype=dtype)
    a = a.reshape(shape)

    return a