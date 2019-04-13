import os
import datetime
BASE_DIR = "/home/cgboal/.ardent/" + datetime.datetime.now().isoformat() + "/"

RESOURCES_DIR = os.path.join(os.path.dirname(__file__), 'resources')

CONCURRENT_HOSTS = 2

CONCURRENT_TASKS = 6

OUTPUT_MODE = "print"
