def fix_url(url):
    if url.startswith('//'):
        url = 'http:' + url
    return url
