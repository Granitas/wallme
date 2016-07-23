from wallme import utils
import pkgutil
import importlib
import os


class Image:
    def __init__(self, url, meta):
        self.meta = meta
        self._url = None
        self.url = url

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = utils.fix_url_http(value)


DOWNLOADERS = [n for _, n, _ in pkgutil.iter_modules([os.path.dirname(__file__)])
               if 'finder' not in n and 'base' not in n]


def find_downloader_module(name):
    return importlib.import_module('wallme.downloaders.{}'.format(name))
