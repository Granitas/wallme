import logging
import os
import requests


def make_content(response, meta=None):
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


class BaseImageDownloader:
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
        raise NotImplementedError
