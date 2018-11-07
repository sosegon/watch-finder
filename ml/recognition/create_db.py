import argparse
import glob
import pickle
import cv2
from common.vision import SIFTDescriptor

def create_db(images_folder, db_name, log_file):
	descriptor = SIFTDescriptor(32)
	result = {}
	invalid_images = []
	# TODO: regex have to include other image formats
	for file in glob.glob("{}/*.jpg".format(images_folder)):
		image = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
		try:
			dsc = descriptor.describe(image)
		except ValueError as e:
			print("Not valid image: {}".format(file))
			invalid_images.append(file)
			continue

		result[file] = dsc

	f = open(db_name, 'wb')
	f.write(pickle.dumps(result))
	f.close()

	with open(log_file, 'wb') as f:
		for item in invalid_images:
			f.write("{}\n".format(item).encode())


parser = argparse.ArgumentParser(description="Create database of images")
parser.add_argument("images_directory", type=str)
parser.add_argument("db_file", type=str)
parser.add_argument("-l", dest='log_file', type=str, default='create_db.log')

args = parser.parse_args()
images_directory = args.images_directory
db_file = args.db_file
log_file = args.log_file

create_db(images_directory, db_file, log_file)