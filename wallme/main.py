from datetime import datetime
import json
import logging
import subprocess

import sys

import click
import os
from wallme.downloaders.bing import BingDownloader
from wallme.downloaders.finder import DOWNLOADERS
from wallme.downloaders.local import LocalNonDownloader
from wallme.downloaders.microsoft import MicrosoftDownloader
from wallme.downloaders.natgeo import NatgeoDownloader
from wallme.downloaders.reddit import RedditDownloader
from wallme.image_downloaders.finder import IMAGE_DOWNLOADERS
from wallme.wallpaper_setters.finder import WALL_SETTERS, get_dlmodule as get_setter_dlmodule
from wallme.settings import WALLME_DIR


@click.group()
@click.version_option()
@click.option('--debug', default=False, help='set verbosity', is_flag=True)
@click.option('--no-log', is_flag=True, default=False, help='log wallpaper')
@click.option('--setter', help='script that sets wallpaper',
              type=click.Choice(['feh', ]),
              default='feh')
@click.option('--setter_script', help='script to set wallpaper, {file} replaced with filename')
@click.pass_context
def cli(context, **kwargs):
    """
    Modular wallpaper getter and setter.
    """
    context.obj = kwargs
    if kwargs['debug']:
        log_stream = logging.StreamHandler()
        log_stream.setLevel(logging.DEBUG)
        logging.basicConfig(handlers=[log_stream])


@cli.command('reddit', help='download image from reddit.com')
@click.pass_context
@click.argument('subreddit')
@click.option('--position', default=0, help='result position; 0 == random')
@click.option('--list-tabs', default=False, is_flag=True, help='list available tabs')
@click.option('--tab', default='hot', help='tab name')
@click.option('-ss', '--setter_script', help='script to set wallpaper, {file} replaced with filename')
def reddit(cli_kwargs, subreddit, tab, position, list_tabs):
    """Downloader for reddit.com"""
    downloader = RedditDownloader()
    if list_tabs:
        click.echo('Available Tabs:')
        for tab in downloader.tabs:
            click.echo(tab)
        return
    if tab not in downloader.tabs:
        e = ValueError('Incorrect tab see --list-tabs for viable options')
        sys.exit(e)
    click.echo('setting random wallpaper from /r/{} {} tab'.format(subreddit, tab))
    content = downloader.download(subreddit, tab=tab, position=position or None)
    set_wallpaper(content, cli_kwargs)


@cli.command('bing', help='download image of the day from bing.com')
@click.pass_context
@click.option('--date', default=None, help='date of daily image in Y-m-d format')
def bing(cli_kwargs, date):
    """Downloader for image of the day of bing.com"""
    click.echo('setting daily image from bing for {} as wallpaper'.format(date or 'Today'))
    downloader = BingDownloader()
    content = downloader.download(date)
    set_wallpaper(content, cli_kwargs)


@cli.command('local', help='set an image from local history')
@click.pass_context
@click.option('--list', default=False, is_flag=True, help='list available categories')
@click.option('--year_month', default=None, help='specify year and month; format %Y%m')
def local(cli_kwargs, position, year_month):
    """Downloader (not really) for local wallme history"""
    position_text = 'random' if position is None else position
    click.echo("setting {} image from local history".format(position_text))
    downloader = LocalNonDownloader()
    content = downloader.download(year_month, position)
    cli_kwargs.obj['no_log'] = True
    set_wallpaper(content, cli_kwargs)


@cli.command('microsoft', help='download image from microsoft wallpapers')
@click.pass_context
@click.option('--list', default=False, is_flag=True, help='list available categories')
@click.option('--category', default='all', help='category from which to download images, see --list')
@click.option('--position', default=None, type=click.INT, help='image position, default random')
def microsoft(cli_kwargs, category, position, list):
    """Downloader for windows wallpapers from microsoft"""
    downloader = MicrosoftDownloader()
    if list:
        click.echo("Available Categories:")
        for cat in downloader.get_categories():
            click.echo(cat)
        return
    position_text = 'random' if position is None else position
    click.echo('setting image {} from category {}'.format(position_text, category))
    content = downloader.download(category, position)
    set_wallpaper(content, cli_kwargs)


@cli.command('natgeo', help='download image from microsoft wallpapers')
@click.pass_context
@click.option('--list', default=False, is_flag=True, help='list available categories')
@click.option('--category', default='all', help='category from which to download images, see --list')
@click.option('--position', default=None, type=click.INT, help='image position, default random')
def natgeo(cli_kwargs, category, position, list):
    """Downloader for image of the day of nationalgeographic.com"""
    downloader = NatgeoDownloader()
    if list:
        click.echo("Available Categories:")
        for cat in downloader.get_categories():
            click.echo(cat)
        return
    position_text = 'random' if position is None else position
    click.echo('setting image {} from category {}'.format(position_text, category))
    content = downloader.download(category, position)
    set_wallpaper(content, cli_kwargs)


@cli.command('list', help='list modules')
@click.option('-a', '--all', 'list_all', is_flag=True, help='list all modules')
def list_modules(list_all):
    click.echo('Downloaders:')
    for el in DOWNLOADERS:
        click.echo('\t{}'.format(el))
    if list_all:
        click.echo('Image Downloaders:')
        for el in IMAGE_DOWNLOADERS:
            click.echo('\t{}'.format(el))
        click.echo('Image Setters:')
        for el in WALL_SETTERS:
            click.echo('\t{}'.format(el))


# def set_wallpaper(content, setter, to_log, setter_script=None):
def set_wallpaper(content, context):
    """
    finds a setter module and uses it to set a wallpaper
    :param content: content dict for image
    :param setter_script - script for setting
    :param setter
    :param to_log
    """
    home = os.path.expanduser('~')
    image_loc = os.path.join(home, '.wallme/wallpaper')
    with open(image_loc, 'wb') as wallme_file:
        wallme_file.write(content['content'])
    # set wallpaper
    setter_script = context.obj['setter_script']
    if setter_script:
        subprocess.Popen(setter_script.format(file=image_loc), shell=True)
    else:
        setter = get_wallpaper_setter(context.obj['setter'])
        setter(image_loc)
    click.echo('wallpaper set from {}'.format(content['url']))
    if not context.obj['no_log']:
        click.echo('saving wallpaper to log')
        log_wallpaper(content)


def log_wallpaper(content):
    """Saves wallpaper content and meta info to .wallme/history"""
    year_month = datetime.now().strftime('%Y%m')
    ym_dir = os.path.join(WALLME_DIR, 'history', year_month)
    if not os.path.exists(ym_dir):
        os.makedirs(ym_dir)
    history_dir = os.path.join(ym_dir, 'history.json')
    # save image file
    filename = content.get('name', 'unknown{}'.format(datetime.now().strftime('%Y%m%d%M%S')))
    file_dir = os.path.join(ym_dir, filename)
    with open(file_dir, 'wb') as image_file:
        image_file.write(content['content'])
        del content['content']  # we don't want content in history so del it
    # save history file
    try:
        with open(history_dir, 'r') as history_json:
            jcontent = history_json.read()
    except FileNotFoundError:
        jcontent = None
    if not jcontent:
        jcontent = '{"items": []}'
    j = json.loads(jcontent)
    j['items'].append(content)
    with open(history_dir, 'w') as history_json:
        history_json.write(json.dumps(j, indent=2))


@cli.command('init', help='create ~/.wallme/')
def init():
    if not os.path.exists(WALLME_DIR):
        click.echo('creating {}'.format(WALLME_DIR))
        os.makedirs(WALLME_DIR)
        history_dir = os.path.join(WALLME_DIR, 'history')
        click.echo('creating {}'.format(history_dir))
        os.makedirs(history_dir)
    else:
        click.echo('{} already exists'.format(WALLME_DIR))


def get_wallpaper_setter(setter_name):
    setter_module = get_setter_dlmodule(setter_name)
    setter_func = getattr(setter_module, 'set_wallpaper')
    return setter_func


if __name__ == '__main__':
    cli()
