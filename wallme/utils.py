from urllib.parse import urljoin


def fix_url_http(url, parent=None):
    """
    Fix urls missing http prefix
    :param url - url to fix
    :param parent - if url is relative parent will be used
                    to generate absolute url
    """
    http = 'https:' if 'https' in url else 'http:'
    if url.startswith('//'):
        url = http + url
    if parent and url.startswith('/'):
        return urljoin(parent, url)
    return url
