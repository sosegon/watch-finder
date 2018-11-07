import urllib.request
import cv2
import numpy as np
import os
import argparse

def store_raw_images(directory, url):
    neg_images_link = url
    neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()
    pic_num = 1

    if not os.path.exists(directory):
        os.makedirs(directory)

    for i in neg_image_urls.split('\n'):
        try:
            print(i)
            im_name = "{:s}/{:d}.jpg".format(directory, pic_num)
            urllib.request.urlretrieve(i, im_name)
            img = cv2.imread(im_name, cv2.IMREAD_GRAYSCALE)
            # should be larger than samples / pos pic (so we can place our image on it)
            resized_image = cv2.resize(img, (100, 100))
            cv2.imwrite(im_name, resized_image)
            pic_num += 1

        except Exception as e:
            print(str(e))

parser = argparse.ArgumentParser(description="Download images")
parser.add_argument('directory', type=str)
parser.add_argument('url', type=str)

args = parser.parse_args()
directory = args.directory
url = args.url

store_raw_images(directory, url)