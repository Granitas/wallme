import pkgutil
import importlib
import os
import logging

import click
import math

from wallme import utils
from wallme.history import HISTORY
from wallme.imagedownloaders import get_dlmodule_bydomain, BaseImageDownloader
from wallme.settings import MAX_RETRIES

DOWNLOADERS = [n[1] for n in pkgutil.iter_modules([os.path.dirname(__file__)])]


class BaseDownloader:
    look_for_dl_module = True
    items_per_page = None

    def _retry(self, **kwargs):
        retries = kwargs.get('retries', 0)
        if retries < MAX_RETRIES:
            click.echo('got duplicate, retrying {}/{}...'.format(retries, MAX_RETRIES))
            kwargs['retries'] = retries + 1
            return self.download(**kwargs)
        else:
            click.secho('failed to find unique random wallpaper after {} tries'.format(MAX_RETRIES),
                        err=True, fg='red')

    @property
    def download(self):
        raise NotImplemented('Downloader must have "download" method')

    def process_url(self, image, download_kwargs):
        cli_ctx = download_kwargs['cli_ctx']
        if cli_ctx:
            ctx = cli_ctx.obj
            is_unique = any(i in ctx.keys() for i in ['unique', 'unique_month'])
            is_random = download_kwargs.get('position', 0) == 0
            cant_random = download_kwargs.get('cant_random', False)
            if (is_unique and is_random) or (is_unique and cant_random):
                history = []
                if ctx.get('unique_month', False):
                    history = HISTORY.all
                if ctx.get('unique', False):
                    history = HISTORY.this_month
                if image.url in [i[0]['url'] for i in history]:
                    if cant_random:
                        click.secho("Current wallpaper already in history, "
                                    "downloader doesn't support random retrieval", fg='yellow')
                        return
                    else:
                        return self._retry(**download_kwargs)
        return self.download_image(image)

    def download_image(self, image):
        """Downloads image and formats a response dictionary
        :param image - downloaders.Image object.
        :param meta - meta information to be included in response dictionary
        """
        url, meta = image.url, image.meta
        logging.debug('downloading {}'.format(url))
        dl_module = get_dlmodule_bydomain(url)
        if not dl_module:
            # If no module found try to check maybe it's direct image
            if self.look_for_dl_module:
                logging.warning('No image parser for {}'.format(url))
            return BaseImageDownloader().download(url, meta)
        return dl_module.ImageDownloader().download(url, meta)

    def _make_position(self, position):
        rand = True if not position else False
        page = 1
        if self.items_per_page:
            page = math.ceil((position + 1) / self.items_per_page)
            if position > self.items_per_page:
                position -= page * self.items_per_page
        return page, position, rand


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


def find_downloader_module(name):
    return importlib.import_module('wallme.downloaders.{}'.format(name))
