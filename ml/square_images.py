import cv2
import numpy as np
import os
import argparse
import glob
import math
from common.vision import make_square

def do_square(in_directory, out_directory):

	if not os.path.exists(out_directory):
		os.makedirs(out_directory)

	images = glob.glob("{:s}/*.jpg".format(in_directory))
	img_num = 1

	for image_name in images:
		try:
			new_image_name = "{:s}/{:s}".format(out_directory, image_name.split("/")[-1])
			print("{:d} | {:s} -> {:s}".format(img_num, image_name, new_image_name))
			image = cv2.imread(image_name)
			image = make_square(image)
			cv2.imwrite(new_image_name, image)
			img_num += 1
		except Exception as e:
			print(str(e))

parser = argparse.ArgumentParser(description="Grayscale images")
parser.add_argument("in_directory", type=str)
parser.add_argument("out_directory", type=str)

args = parser.parse_args()
in_directory = args.in_directory
out_directory = args.out_directory

do_square(in_directory, out_directory)


