import logging

import click
from wallme.downloaders.wallhaven import WallhavenDownloader
from wallme.commands import set_wallpaper


@click.command('wallhaven', help='download image from wallhaven.cc')
@click.pass_context
@click.option('-p', '--position', default=0, help='position, +-[1..n] (default=0 random)')
@click.option('--sorting', help='sorting of results (default:random)', default='random',
              type=click.Choice(['favorites', 'views', 'relevance', 'date_added', 'random']))
@click.option('--nsfw', is_flag=True, help='enable nsfw images')
@click.option('--nsfw-only', is_flag=True, help='only nsfw images')
@click.option('--categories', default='general,anime,people',
              help='categories to scrape; comma separated list from [general,anime,people] (default all)')
def cli(cli_ctx, **kwargs):
    """Downloader for wallhaven.cc"""
    logger = logging.getLogger(__name__)
    logger.debug('Got cli arguments {}'.format(kwargs))
    purity = '100'
    if kwargs.get('nsfw', False):
        purity = '110'
    if kwargs.get('nsfw_only', False):
        purity = '010'
    categories = extract_categories(kwargs.get('categories', '').lower())
    kwargs['categories'] = categories
    kwargs['purity'] = purity
    logger.debug('Downloading content using {}'.format(kwargs))
    content = WallhavenDownloader().download(**kwargs, cli_ctx=cli_ctx)
    set_wallpaper(content, cli_ctx)


def extract_categories(text):
    categories = ['0', '0', '0']
    if 'general' in text:
        categories[0] = '1'
    if 'anime' in text:
        categories[1] = '1'
    if 'people' in text:
        categories[2] = '1'
    return ''.join(categories)
