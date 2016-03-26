import sys
import os
import random

from requests.models import Response
from wallme import settings
from wallme.downloaders.base import BaseDownloader
from wallme.image_downloaders.content import make_content


class LocalNonDownloader(BaseDownloader):
    """
    Downloader for local history files, doesn't actually
    download anything just wraps local files as responses
    """
    look_for_dl_module = False

    # noinspection PyMethodOverriding
    def download(self, year_month=None, position=None):
        """
        :param year_month - specify history month, default all of history
        :param position - position of image to ues, default random
        :return: dict{'content': <image_content>, <some meta data>...}
        """
        history = os.path.join(settings.WALLME_DIR, 'history')
        if year_month:
            history = os.path.join(history, year_month)
            if not os.path.exists(history):
                e = ValueError('No items for supplied '
                               'yearmonth "{}" value'.format(year_month))
                sys.exit(e)
        # Gather all images in history location
        images = []
        items = list(os.walk(history))
        items = [i for i in items if i != 'wallpaper' and '.json' not in i]
        for item in items:
            directory, dirs, files = item
            if not files:
                continue
            for file in files:
                abs_file = os.path.join(directory, file)
                images.append(abs_file)
        # choose image (either by position or random)
        if not position:
            image = random.choice(images)
        elif position >= len(images):
            image = images[position]
        else:
            e = ValueError('Position too high: pos:{}/images found:{}'.format(position, len(images)))
            sys.exit(e)
        # make fake requests response
        image_response = Response()
        image_response.url = image
        with open(image, 'rb') as image_file:
            image_response._content = image_file.read()
        return make_content(image_response)
