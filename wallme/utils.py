from urllib.parse import urljoin


def fix_url(url, parent=None):
    http = 'https:' if 'https' in url else 'http:'
    if url.startswith('//'):
        url = http + url
    if parent and url.startswith('/'):
        return urljoin(parent, url)
    return url
