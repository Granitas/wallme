import logging
from wallme.image_downloaders import finder
from wallme.image_downloaders.base import BaseImageDownloader

class BaseDownloader:
    def __init__(self):
        pass

    def download_image(self, url, meta=None):
        logging.debug('downloading {}'.format(url))
        dl_module = finder.get_dlmodule_bydomain(url)
        if not dl_module:
            # If no module found try to check maybe it's direct image
            logging.warning('No image parser for {}'.format(url))
            return BaseImageDownloader().download(url, meta)
        return dl_module.ImageDownloader().download(url, meta)