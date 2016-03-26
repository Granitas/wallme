import sys
import random

import requests
from parsel import Selector
from wallme.downloaders.base import BaseDownloader


class MicrosoftDownloader(BaseDownloader):
    """
    Downloader for windows.microsoft.com/en-us/windows/wallpaper
    """
    url = "http://windows.microsoft.com/en-us/windows/wallpaper"
    # extend
    look_for_dl_module = False

    def get_categories(self, response=None):
        if not response:
            response = requests.get(self.url)
        sel = Selector(text=response.text)
        return sel.xpath("//div[@class='tabStripContainer']//a/@data-baseid").extract()

    # noinspection PyMethodOverriding
    def download(self, category=None, position=None):
        """
        :param category - category or defaults to featured
        :param position - position of image or defaults to random
        :return: dict{'content': <image_content>, <some meta data>...}
        """
        if not category:
            category = 'all'
        cat_url = '{}?T1={}'.format(self.url, category)
        response = requests.get(cat_url)
        sel = Selector(text=response.text)
        images = sel.xpath("//img[@class='blkImg']")
        # find the image by position
        if not position:
            image = random.choice(images)
        elif position <= len(images):
            image = images[position]
        else:
            e = IndexError('Position too big or wrong')
            sys.exit(e)
        image_url = image.xpath('../@href').extract_first()
        meta = {'title': image.xpath('@title').extract_first(),
                'url': image_url}
        return self.download_image(image_url, meta)
