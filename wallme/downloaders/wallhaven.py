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
    look_for_dl_module = False

    items_per_page = 24.0
    logger = logging.getLogger(__name__)
    sorting_types = ['favorites', 'views', 'relevance', 'date_added', 'random']

    def download(self, **kwargs):
        """
        Download and set image from wallhaven.cc
        :param query - query of search
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
        q = kwargs.get('query', '')  # search query
        page, position, rand = self._make_position(kwargs.get('position', 0))
        url = self.base_url
        for arg in ['categories', 'purity', 'sorting', 'order', 'page', 'q']:
            value = locals()[arg]
            if value:
                url = add_or_replace_parameter(url, arg, locals()[arg])
        # Download and parse items
        resp = requests.get(url)
        if resp.status_code != 200:
            self.logger.error('Failed to download image list {}'.format(resp.url))
            return
        list_sel = Selector(text=resp.text)
        items = list_sel.xpath("//section[@class='thumb-listing-page']//figure/a/@href").extract()
        item = random.choice(items) if rand else items[position - 1]
        resp = requests.get(item)
        if resp.status_code != 200:
            self.logger.error('Failed to download image page {}'.format(resp.url))
            return
        sel = Selector(text=resp.text)
        image_url = sel.xpath("//img[@id='wallpaper']/@src").extract_first()
        meta = {
            'id': sel.xpath("//img[@id='wallpaper']/@data-wallpaper-id").extract_first(),
            'tags': sel.xpath("//ul[@id='tags']//li/a/text()").extract(),
            'views': sel.xpath("//dt[contains(text(),'Views')]/following-sibling::dd[1]/text()").extract_first(),
            'favorites': sel.xpath("//dt[contains(text(),'Favorites')]"
                                   "/following-sibling::dd[1]//text()").extract_first(),
            'res': sel.xpath("//h3/text()").extract_first(),
        }
        image = Image(image_url, meta)
        return self.process_url(image, kwargs)

