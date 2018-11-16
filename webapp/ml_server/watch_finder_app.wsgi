import sys
sys.path.insert(0, '/var/www/html/watch-finder')

# The next parameter is configurable, it has to be updated in the production mode
import os
os.environ['WATCH_FINDER_HOME'] = '/mnt/linux_shared/shared/lwork/watch-finder'

from run_web_server import app as application