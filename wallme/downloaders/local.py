import sys
import os
import random

from requests.models import Response

from wallme.downloaders.base import BaseDownloader
from wallme.history import get_history
from wallme.image_downloaders.content import make_content


class LocalNonDownloader(BaseDownloader):
    """
    Downloader for local history files, doesn't actually
    download anything just wraps local files as responses
    """
    look_for_dl_module = False

    # noinspection PyMethodOverriding
    @staticmethod
    def download(year_month=None, position=None):
        """
        :param year_month - specify history month, default all of history
        :param position - position of image to ues, default random
        :return: dict{'content': <image_content>, <some meta data>...}
        """
        images = [os.path.join(loc, i['name']) for i, loc in get_history(year_month)]
        if position is None:
            image = random.choice(images)
        elif position <= len(images) or position < 0:
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
