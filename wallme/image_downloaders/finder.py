import pkgutil
import importlib
import os
from wallme import image_downloaders
import tldextract

IMAGE_DOWNLOADERS = [n for _, n, _ in pkgutil.iter_modules([os.path.dirname(image_downloaders.__file__)])
                     if 'finder' not in n and 'base' not in n]

def get_dlmodule_bydomain(url):
    """
    Finds what image_downloader module to use for specific url by it's domain
    e.g.
    http://i.imgur.com/u6SmpU5.jpg
    -> <module 'wallme.image_downloaders.imgur' from ...>
    """

    domain = tldextract.extract(url).domain.lower()
    for downloader in IMAGE_DOWNLOADERS:
        if downloader == domain:
            matching_domain = domain
            dl_module = importlib.import_module('wallme.image_downloaders.{}'.format(matching_domain))
            return dl_module
