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

def store_raw_images(directory, list_file, log_file='watches.log'):
	logs = []
	image_urls = open(list_file, 'r')
	unique_urls = {}
	unique_names = {}

	images_in_folder = glob.glob("{:s}/*".format(directory))

	if not os.path.exists(directory):
		os.makedirs(directory)

	for url in image_urls.read().split('\n'):
		# No image
		if '.' not in url.split('/')[-1]:
			new_log = 'NO IMAGE URL: {}'.format(url)
			print(new_log)
			logs.append(new_log)
			continue

		# Url repeated
		if url not in unique_urls:
			unique_urls[url] = url
		else:
			new_log = 'REPEATED URL: {}'.format(url)
			# print(new_log)
			logs.append(new_log)
			continue

		# Name repeated
		image_name = url.split('/')[-1]
		if image_name not in unique_names:
			unique_names[image_name] = image_name
		else:
			new_log = 'REPEATED NAME: {}'.format(url)
			# print(new_log)
			logs.append(new_log)
			continue

		# Image in source folder
		image_path = '{}/{}'.format(directory, image_name)
		if image_path in images_in_folder:
			new_log = 'DOWNLOADED: {}'.format(url)
			# print(new_log)
			logs.append(new_log)
			unique_names[image_name] = image_name
			continue

		try:
			urllib.request.urlretrieve(url, image_path)
			unique_urls[url] = url
			new_log = 'NEW IMAGE: {}'.format(url)
			print(new_log)
			logs.append(new_log)
			unique_names[image_name] = image_name
		except Exception as e:
			new_log = 'ERROR: {}'.format(url)
			print(new_log)
			logs.append(new_log)

	# Just assume the image name are uniques
	for image_path in images_in_folder:
		image_name = image_path.split('/')[-1]
		print("{}".format(image_name))
		if image_name not in unique_names:
			os.remove(image_path)
			new_log = 'REMOVED: {}'.format(image_path)
			print(new_log)
			logs.append(new_log)

	with open(log_file, 'wb') as f:
		for item in logs:
			f.write("{}\n".format(item).encode())



parser = argparse.ArgumentParser(description="Download images")
parser.add_argument('directory', type=str)
parser.add_argument('list_file', type=str)

args = parser.parse_args()
directory = args.directory
list_file = args.list_file

store_raw_images(directory, list_file)