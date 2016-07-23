import pkgutil
import importlib
import logging
import os
from urllib.parse import urlsplit

import parsel
import requests

from wallme import utils
from wallme.imagedownloaders import make_content

IMAGE_DOWNLOADERS = [n[1] for n in pkgutil.iter_modules([os.path.dirname(__file__)])]


def get_dlmodule_bydomain(url):
    """
    Finds what image_downloader module to use for specific url by it's domain
    e.g.
    http://i.imgur.com/u6SmpU5.jpg
    -> <module 'wallme.image_downloaders.imgur' from ...>
    """

    domain = urlsplit(url).netloc.split('.')[-2]
    for downloader in IMAGE_DOWNLOADERS:
        if downloader == domain:
            matching_domain = domain
            dl_module = importlib.import_module('wallme.image_downloaders.{}'.format(matching_domain))
            return dl_module


# todo turn this into a proper class
def make_content(response, meta=None):
    """
    Converts requests.response to content dictionary
    :param response: requests response object
    :param meta[None]: extra data used in generating content
    :return:
    return {'content': image_content in bytes,
           'name': filename,
           'extension': file extension,
           'meta': meta data from :param meta,
           'url': url of file image}
    """
    if not meta:
        meta = {}
    name = os.path.basename(response.url)
    extension = response.headers.get('Content-Type', '').split('/')[-1]
    if not extension:
        extension = name.rsplit('.', 1)[-1]
    return {'content': response.content,
            'name': name,
            'extension': extension,
            'meta': meta,
            'url': response.url}


BIGGEST_IMAGE = 'find_biggest_image'


class BaseImageDownloader:
    def __init__(self, default_behaviour=BIGGEST_IMAGE):
        self.default_behaviour = default_behaviour
        # Set up logging
        self.logging = logging.getLogger(self.__class__.__name__)
        self.logging.setLevel(logging.DEBUG)

    def download(self, url, meta=None):
        """Download image from url
        :returns dict with content:
        content - content of the file
        name - filename
        extension - file extension if there is one
        url - url from where the image was downloaded
        """
        logging.debug('Downloading {}'.format(url))
        response = requests.get(url)
        content_type = response.headers.get('Content-Type', '')
        if 'image' in content_type:
            return make_content(response, meta)
        return self.find_images(response, meta)

    def find_images(self, response, meta=None):
        """
        Base method for retrieving images from response
        Should return dictionary from
        """
        if self.default_behaviour:
            return getattr(self, self.default_behaviour)(response, meta)
        raise NotImplementedError

    def find_biggest_image(self, response, meta=None):
        """
        Finds all images on the website and returns the biggest one by resolution
        NOTE:
        This method should ONLY be used as last resort when source
        is not an image and there's no downloader for the domain
        because it's slow and inaccurate
        """
        sel = parsel.Selector(text=response.text)
        urls = sel.xpath("//*[self::div or self::span]/img/@src").extract()
        for image in sel.xpath("//*[self::div or self::span]/a[img]/@href").extract():
            if '.' in os.path.basename(image):
                print(image)
                urls.append(image)
        urls = [utils.fix_url_http(u, parent=response.url) for u in urls]

        images = []
        for i, url in enumerate(urls):
            self.logging.debug('downloading {}/{}: {}'.format(i, len(urls), url))
            try:
                images.append(requests.get(url))
            except Exception as e:
                logging.debug('Failed to download image: {}\n{}'.format(url, e))
        images = [i for i in images if 'image' in i.headers['Content-Type']]
        images = sorted(images, key=lambda v: int(v.headers['Content-Length']), reverse=True)
        return make_content(images[0], meta=meta)
