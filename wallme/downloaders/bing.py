from datetime import datetime
import json
from urllib.parse import urljoin
import sys

import requests
from wallme.downloaders import BaseDownloader


class BingDownloader(BaseDownloader):
    """
    Downloader for daily image of bing.com
    """
    api_tpl = "http://www.bing.com/HPImageArchive.aspx?" \
              "format=js&idx={days}&n=1&nc={timestamp}&pid=hp".format
    date_format = '%Y-%m-%d'
    # extend
    look_for_dl_module = False

    # noinspection PyMethodOverriding
    def download(self, date=None):
        """
        :param date - date of picture in %Y-%m-%d format
        :return: dict{'content': <image_content>, <some meta data>...}
        """
        # Generate timestamp for wanted day
        if date:
            date = date.strip()
            date_obj = datetime.strptime(date, self.date_format)
        else:
            date_obj = datetime.now()
        timestamp = int(date_obj.timestamp() * 1000)
        # count how many days between now and date
        days = (datetime.now() - date_obj).days
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
        return self.download_image(image_url, meta)
