import math
from urllib.parse import urljoin
import random

import requests
from parsel import Selector
from wallme import utils
from wallme.downloaders import Image, BaseDownloader


class NatgeoDownloader(BaseDownloader):
    """
    Downloader for National Geopgraphy galery
    "http://photography.nationalgeographic.com/photography/photo-of-the-day/archive"
    """
    url = "http://photography.nationalgeographic.com/" \
          "photography/photo-of-the-day/archive"
    url_tpl = "http://photography.nationalgeographic.com/photography" \
              "/photo-of-the-day/{category}/".format
    default_cat = 'archive'
    # extend
    look_for_dl_module = False

    def get_categories(self, response=None):
        if not response:
            response = requests.get(self.url)
        sel = Selector(text=response.text)
        categories = sel.xpath("//select[@id='search_category']"
                               "/option/text()").extract()
        categories = [c.split(' by ')[0].replace(' & ', '-')
                      for c in categories]
        return categories

    # noinspection PyMethodOverriding
    def download(self, **kwargs):
        """
        :param position - position of image or defaults to random
        :param category - archive category, see get_categories for the list
        :return: dict{'content': <image_content>, <some meta data>...}
        """
        category = kwargs.get('category', None)
        position = kwargs.get('position', 0)
        rand = False
        if position == 0:
            rand = True
        if position > 1:
            position -= 1  # since 0 is reserved reduce position
        if not category:
            category = self.default_cat
        category = category.lower()
        url = self.url_tpl(category=category)
        response = requests.get(url)
        sel = Selector(text=response.text)
        # get position
        total_items = int(sel.xpath("//p[@class='count']").re('\d+')[0])
        items = sel.xpath("//div[@id='search_results']//a[img]/@href").extract()
        items_per_page = len(items)
        # find the right image by position
        if rand:
            position = random.randrange(0, total_items)
        if position < items_per_page:
            image = items[position]
        else:
            page = int(math.ceil(position / items_per_page))
            position -= items_per_page * (page - 1)
            url = "{}?page={}".format(url, page)
            response = requests.get(url)
            pos_sel = Selector(text=response.text)
            items = pos_sel.xpath("//div[@id='search_results']//a[img]/@href").extract()
            image = items[position]
        # retrieve image
        response = requests.get(urljoin(url, image))
        sel = Selector(text=response.text)
        image_url = sel.xpath("//div[@class='primary_photo']/a/img/@src").extract_first()
        image_url = utils.fix_url_http(image_url)
        meta = {
            'url': image_url,
            'title': sel.xpath("//div[@class='primary_photo']/a/img/@alt").extract_first(),
            'desc_title': sel.xpath("//div[@id='caption']/h2/text()").extract_first(),
            'desc': sel.xpath("//div[@id='caption']/p[not(@class)]/text()").extract_first(),
            'author': sel.xpath("//div[@id='caption']/p[@class='credit']/a/text()").extract_first(),
            'publication_date': sel.xpath("//div[@id='caption']/p[@class='publication_time']"
                                          "/text()").extract_first(),
        }
        image = Image(image_url, meta)
        return self.process_url(image, kwargs)

if __name__ == '__main__':
    ng = NatgeoDownloader()
    print(ng.download(category='animals', position=0))
