import parsel
import requests
from wallme import utils
from wallme.image_downloaders.base import BaseImageDownloader, make_content


class ImageDownloader(BaseImageDownloader):
    def find_images(self, response, meta=None):
        sel = parsel.Selector(text=response.text)
        url = sel.xpath("//div[@class='post-image']/a/img/@src").extract_first()
        if url:
            url = utils.fix_url(url)
            file_resp = requests.get(url)
            return make_content(file_resp, meta)
        return {}
