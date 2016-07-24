import os

WALLME_DIR = os.path.join(os.path.expanduser('~'), '.wallme')
WALLME_HISTORY_DIR = os.path.join(WALLME_DIR, 'history')
MAX_RETRIES = 5
FILE_LOG_FORMAT = '[%(name)s]%(levelname)s:%(message)s'
CONSOLE_LOG_FORMAT = '%(levelname)s:%(message)s'
LOG_DIR = os.path.join(os.path.expanduser('~'), '.wallme', 'wallme.log')
