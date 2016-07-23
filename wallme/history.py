import json
import os
from datetime import datetime

from wallme.settings import WALLME_HISTORY_DIR, WALLME_DIR

WALLME_HISTORY_JSON_LOCS = [os.path.join(WALLME_HISTORY_DIR, year_month, 'history.json')
                            for year_month in sorted(os.listdir(WALLME_HISTORY_DIR), key=int)]


class History:
    def __init__(self):
        self.__all = None
        self.__this_month = None

    @property
    def this_month(self):
        if not self.__this_month:
            this_month = datetime.now().strftime('%Y%m')
            self.__this_month = get_history(this_month)
        return self.__this_month

    @property
    def all(self):
        if not self.__all:
            self.__all = get_history()
        return self.__all


def get_history(year_month=None):
    locs = WALLME_HISTORY_JSON_LOCS
    if year_month:
        locs = [l for l in locs if year_month in l]
        if not locs:
            return
    results = []
    for loc in locs:
        with open(loc, 'r') as f:
            history_json = json.loads(f.read())
            for item in history_json['items']:
                results.append((item, os.path.dirname(loc)))
    return results


HISTORY = History()


def log_wallpaper(content):
    """Saves wallpaper content and meta info to .wallme/history"""
    year_month = datetime.now().strftime('%Y%m')
    ym_dir = os.path.join(WALLME_DIR, 'history', year_month)
    if not os.path.exists(ym_dir):
        os.makedirs(ym_dir)
    history_dir = os.path.join(ym_dir, 'history.json')
    # save image file
    filename = content.get('name', 'unknown{}'.format(datetime.now().strftime('%Y%m%d%M%S')))
    file_dir = os.path.join(ym_dir, filename)
    if not os.path.exists(file_dir):
        with open(file_dir, 'wb') as image_file:
            image_file.write(content['content'])
    # save history file
    del content['content']  # we don't want content in history so del it
    try:
        with open(history_dir, 'r') as history_json:
            jcontent = history_json.read()
    except FileNotFoundError:
        jcontent = None
    if not jcontent:
        jcontent = json.dumps({'items': []})
    j = json.loads(jcontent)
    j['items'].append(content)
    with open(history_dir, 'w') as history_json:
        history_json.write(json.dumps(j, indent=2))

