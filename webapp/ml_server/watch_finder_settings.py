import os

# This is an updatable parameter
REDIS_HOST = 'localhost'

REDIS_PORT = 6379
REDIS_DB = 0

# Constants used for server queuing
IMAGE_DTYPE = 'uint8'
IMAGE_SIZE = 300
IMAGE_QUEUE = "image_queue"
BATCH_SIZE = 32
SERVER_SLEEP = 0.25
CLIENT_SLEEP = 0.25

# The next parameter is configurable, it has to be updated in the production mode
os.environ['WATCH_FINDER_HOME'] = '/mnt/linux_shared/shared/lwork/watch-finder/webapp'
SIFT_DB = '{}/data/watches_db'.format(os.environ['WATCH_FINDER_HOME'])