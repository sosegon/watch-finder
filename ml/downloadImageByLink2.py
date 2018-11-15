#!../python
#####################################################################
# MAKE SURE THE SYMLINK IN THE ROOT FOLDE OF THE APPLICATION EXISTS #
#####################################################################

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
    pic_num = 1

    for i in neg_image_urls.read().split('\n'):
        try:
            print("{:d} | {:s}".format(pic_num, i))
            im_name = "{:s}/{:s}".format(directory, i.split("/")[-1])
            if im_name.split(".")[-1] != "jpg":
                continue
            if im_name in existing:
                print("Existing")
                pic_num += 1
                continue
            urllib.request.urlretrieve(i, im_name)
            pic_num += 1

        except Exception as e:
            print(str(e))

parser = argparse.ArgumentParser(description="Download images")
parser.add_argument('directory', type=str)
parser.add_argument('list_file', type=str)

args = parser.parse_args()
directory = args.directory
list_file = args.list_file

store_raw_images(directory, list_file)