import cv2
import numpy as np
import os
import argparse
import glob

def to_grayscale(in_directory, out_directory):

	if not os.path.exists(out_directory):
		os.makedirs(out_directory)

	images = glob.glob("{:s}/*".format(in_directory))

	for im in images:
		new_im = "{:s}/{:s}".format(out_directory, im.split("/")[-1])
		print("{:s} -> {:s}".format(im, new_im))
		im_gray = cv2.imread(im, cv2.IMREAD_GRAYSCALE)
		im_resized = cv2.resize(im_gray, (100, 100))
		cv2.imwrite(new_im, im_resized)

parser = argparse.ArgumentParser(description="Grayscale images")
parser.add_argument("in_directory", type=str)
parser.add_argument("out_directory", type=str)

args = parser.parse_args()
in_directory = args.in_directory
out_directory = args.out_directory

to_grayscale(in_directory, out_directory)


