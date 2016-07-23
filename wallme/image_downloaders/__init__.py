import pkgutil
import importlib
import os
from urllib.parse import urlsplit

NON_MODULES = ['finder', 'base', 'content']
IMAGE_DOWNLOADERS = [n for _, n, _ in pkgutil.iter_modules([os.path.dirname(__file__)])
                     if not any(non in n for non in NON_MODULES)]


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
