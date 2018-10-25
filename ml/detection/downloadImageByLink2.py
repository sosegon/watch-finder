import urllib.request
import cv2
import numpy as np
import os
import argparse
import glob

def store_raw_images(directory, list_file):
    neg_image_urls = open(list_file, "r");

    if not os.path.exists(directory):
        os.makedirs(directory)

    existing = glob.glob("{:s}/*".format(directory))

    for i in neg_image_urls.read().split('\n'):
        try:
            print(i)
            im_name = "{:s}/{:s}".format(directory, i.split("/")[-1])
            if im_name in existing:
                print("Existing")
                continue
            urllib.request.urlretrieve(i, im_name)

        except Exception as e:
            print(str(e))

parser = argparse.ArgumentParser(description="Download images")
parser.add_argument('directory', type=str)
parser.add_argument('list_file', type=str)

args = parser.parse_args()
directory = args.directory
list_file = args.list_file

store_raw_images(directory, list_file)