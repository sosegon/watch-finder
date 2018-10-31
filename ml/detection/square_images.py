import cv2
import numpy as np
import os
import argparse
import glob
import math

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

def make_square(img):
	h, w, c = img.shape
	if h == w:
		return img
	elif w < h:
		n_img = np.ones((h, h, c)) * 255
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
		n_img[:, left:-right, :] = img

	elif w > h:
		n_img = np.ones((w, w, c)) * 255
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
		n_img[top:-bottom, :, :] = img

	return n_img

args = parser.parse_args()
in_directory = args.in_directory
out_directory = args.out_directory

do_square(in_directory, out_directory)


