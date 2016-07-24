import urllib
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


def add_or_replace_parameter(url, name, new_value):
    """
    Add or remove a parameter to a given url
    """
    parsed = urllib.parse.urlsplit(url)
    args = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)

    new_args = []
    found = False
    for name_, value_ in args:
        if name_ == name:
            new_args.append((name_, new_value))
            found = True
        else:
            new_args.append((name_, value_))

    if not found:
        new_args.append((name, new_value))

    query = urllib.parse.urlencode(new_args)
    return urllib.parse.urlunsplit(parsed._replace(query=query))

