import logging
import random

import math
import requests
from parsel import Selector

from wallme.downloaders import Image, BaseDownloader
from wallme.utils import add_or_replace_parameter


class WallhavenDownloader(BaseDownloader):
    """
    Downloader for wallhaven.cc
    """
    base_url = 'https://alpha.wallhaven.cc/search'
    wallpaper_url = 'https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-{}.{}'.format
    look_for_dl_module = False

    items_per_page = 24.0
    logger = logging.getLogger(__name__)
    sorting_types = ['favorites', 'views', 'relevance', 'date_added', 'random']

    def download(self, **kwargs):
        """
        Download and set image from wallhaven.cc
        :param position - position of image to choose from listed from 1 to 24,
        default is 0 = random.
        :param categories - categories to download from in 000 format, where every number
        represents binary for [general, anime, people] list.
        :param purity - purity of content in 000 format, where every number
        represents binary for [sfw, sketchy, _].
        :param sorting - sorting type from available see WallhavenDownloader.sorting_types .
        """
        # Make url from arguments
        order = 'desc'
        categories = kwargs.get('categories', '')
        purity = kwargs.get('purity', '')
        sorting = kwargs.get('sorting', '')
        page, position, rand = self._make_position(kwargs.get('position', 0))
        url = self.base_url
        for arg in ['categories', 'purity', 'sorting', 'order', 'page']:
            value = locals()[arg]
            if value:
                url = add_or_replace_parameter(url, arg, locals()[arg])
        # Download and parse items
        resp = requests.get(url)
        sel = Selector(text=resp.text)
        items = sel.xpath("//section[@class='thumb-listing-page']//figure")
        item = random.choice(items) if rand else items[position - 1]
        image_ext = item.xpath('img/@data-src').extract_first().rsplit('.')[-1]
        image_id = item.xpath('@data-wallpaper-id').extract_first()
        image_url = self.wallpaper_url(image_id, image_ext)
        meta = {
            'id': image_id,
            'res': item.xpath(".//span[@class='wall-res']/text()").extract_first(),
            'favorites': item.xpath(".//a[contains(@class,'wall-favs')]/text()").extract_first(),
        }
        image = Image(image_url, meta)
        return self.process_url(image, kwargs)
