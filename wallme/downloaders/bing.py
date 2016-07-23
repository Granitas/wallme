import random
from datetime import datetime, timedelta
import json
from urllib.parse import urljoin
import sys

import click
import requests
from wallme.downloaders import BaseDownloader, Image


class BingDownloader(BaseDownloader):
    """
    Downloader for daily image of bing.com
    """
    api_tpl = "http://www.bing.com/HPImageArchive.aspx?" \
              "format=js&idx={days}&n=1&nc={timestamp}&pid=hp".format
    date_format = '%Y-%m-%d'
    # extend
    look_for_dl_module = False
    max_position = 10  # amount of days back of wallpapers bing keeps, is very unpredictable

    # noinspection PyMethodOverriding
    def download(self, **kwargs):
        """
        :param date - date of picture in %Y-%m-%d format
        :return: dict{'content': <image_content>, <some meta data>...}
        """
        # Generate timestamp for wanted day
        rand = True if kwargs['position'] is 0 else False
        position = abs(kwargs['position']) - 1
        date = (kwargs.get('date', '') or '').strip()
        date_obj = datetime.strptime(date, self.date_format) if date else datetime.now()
        if rand:
            date_obj -= timedelta(days=random.randint(0, self.max_position))
            click.echo('setting random daily image from bing as wallpaper')
        else:
            date_obj -= timedelta(days=position)
            click.echo('setting daily image from bing for {} as wallpaper'.format(date or 'Today'))
        timestamp = int(date_obj.timestamp() * 1000)
        days = (datetime.now() - date_obj).days  # count how many days between now and date

        # retrieve image json via api
        url = self.api_tpl(days=days, timestamp=timestamp)
        response = requests.get(url)
        if response.text == 'null':
            e = ValueError("No image for this date :(\nTry an earlier date")
            sys.exit(e)
        data = json.loads(response.text)['images'][0]
        image_url = urljoin(url, data['url'])
        meta = {'date': date_obj.strftime(self.date_format),
                'copyright': data.get('copyright'),
                'url': image_url}
        image = Image(image_url, meta)
        return self.process_url(image, kwargs)
