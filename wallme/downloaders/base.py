import logging

import click

from wallme.history import HISTORY
from wallme.image_downloaders import get_dlmodule_bydomain
from wallme.image_downloaders.base import BaseImageDownloader
from wallme.settings import MAX_RETRIES


class BaseDownloader:
    look_for_dl_module = True

    def _retry(self, **kwargs):
        retries = kwargs.get('retries', 0)
        if retries < MAX_RETRIES:
            click.echo('got duplicate, retrying {}/{}...'.format(retries, MAX_RETRIES))
            kwargs['retries'] = retries + 1
            self.download(**kwargs)
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
            is_random = ctx.get('position', 0) == 0
            if is_unique and is_random:
                history = []
                if ctx.get('unique_month', False):
                    history = HISTORY.all
                if ctx.get('unique', False):
                    history = HISTORY.this_month
                if image.url in [i[0]['url'] for i in history]:
                    self._retry(**download_kwargs)
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
