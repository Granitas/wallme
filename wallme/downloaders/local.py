import json
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
    @staticmethod
    def download(year_month=None, position=None):
        """
        :param year_month - specify history month, default all of history
        :param position - position of image to ues, default random
        :return: dict{'content': <image_content>, <some meta data>...}
        """
        history_loc = os.path.join(settings.WALLME_DIR, 'history')

        def get_images(ym):
            with open(os.path.join(history_loc, ym, 'history.json'), 'r') as f:
                history_json = json.loads(f.read())
            return [os.path.join(history_loc, ym, i['name']) for i in history_json['items']]

        images = []
        if not year_month:
            yms = sorted(os.listdir(history_loc), key=int)
            for ym in yms:
                images.extend(get_images(ym))
        else:
            images = get_images(year_month)
        if not position:
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
