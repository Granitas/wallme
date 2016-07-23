import parsel
import requests
from wallme import utils
from wallme.imagedownloaders import make_content, BaseImageDownloader


class ImageDownloader(BaseImageDownloader):
    def find_images(self, response, meta=None):
        sel = parsel.Selector(text=response.text)
        url = sel.xpath("//div[@class='post-image']/a/img/@src").extract_first()
        if url:
            url = utils.fix_url_http(url)
            file_resp = requests.get(url)
            return make_content(file_resp, meta)
        return {}
