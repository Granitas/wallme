import logging
from wallme.image_downloaders import finder
from wallme.image_downloaders.base import BaseImageDownloader


class BaseDownloader:
    look_for_dl_module = True

    @property
    def download(self):
        raise NotImplemented('Downloader must have "download" method')

    def download_image(self, url, meta=None):
        """Downloads image and formats a response dictionary
        :param url - url where image is hosted
        :param meta - meta information to be included in response dictionary
        """
        logging.debug('downloading {}'.format(url))
        dl_module = finder.get_dlmodule_bydomain(url)
        if not dl_module:
            # If no module found try to check maybe it's direct image
            if self.look_for_dl_module:
                logging.warning('No image parser for {}'.format(url))
            return BaseImageDownloader().download(url, meta)
        return dl_module.ImageDownloader().download(url, meta)
