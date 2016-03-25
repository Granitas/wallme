import os


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
