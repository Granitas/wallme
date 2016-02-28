from datetime import datetime
import json
import logging
import subprocess

import click
import os
from wallme.downloaders import finder as download_finder
from wallme.downloaders.finder import DOWNLOADERS
from wallme.image_downloaders.finder import IMAGE_DOWNLOADERS
from wallme.wallpaper_setters.finder import WALL_SETTERS, get_dlmodule as get_setter_dlmodule

WALLME_DIR = os.path.join(os.path.expanduser('~'), '.wallme')

@click.group()
@click.version_option()
@click.option('--debug', 'debug', default=False, help='set verbosity', is_flag=True)
def cli(debug):
    """
    Modular wallpaper getter and setter.
    """
    if debug:
        log_stream = logging.StreamHandler()
        log_stream.setLevel(logging.DEBUG)
        logging.basicConfig(handlers=[log_stream])


@cli.command('reddit', help='download from reddit.com')
@click.argument('subreddit')
@click.option('-p', '--position', default=0, help='result position; 0 == random')
@click.option('--log/--no-log', default=True, help='log wallpaper')
@click.option('--tab', default='hot', help='tab name',
              type=click.Choice([
                  'controversial',
                  'controversial_from_all',
                  'controversial_from_day',
                  'controversial_from_hour',
                  'controversial_from_month',
                  'controversial_from_week',
                  'controversial_from_year',
                  'hot',
                  'new',
                  'rising',
                  'top',
                  'top_from_all',
                  'top_from_day',
                  'top_from_hour',
                  'top_from_month',
                  'top_from_week',
                  'top_from_year']))
@click.option('--setter', help='script that sets wallpaper',
              type=click.Choice([
                  'feh',
              ]),
              default='feh')
@click.option('-ss', '--setter_script', help='script to set wallpaper, {file} replaced with filename')
def reddit(subreddit, tab, position, setter, log, setter_script):
    """Downloader for reddit.com"""
    click.echo('setting random wallpaper from /r/{} {} tab'.format(subreddit, tab))
    downloader = get_downloader('reddit')
    content = downloader.download(subreddit, tab=tab, position=position or None)
    set_wallpaper(content, setter, log, setter_script)

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

def set_wallpaper(content, setter, to_log, setter_script=None):
    """finds a setter module and uses it to set a wallpaper"""
    home = os.path.expanduser('~')
    image_loc = os.path.join(home, '.wallme/wallpaper')
    with open(image_loc, 'wb') as wallme_file:
        wallme_file.write(content['content'])
    # set wallpaper
    if setter_script:
        subprocess.Popen(setter_script.format(file=image_loc), shell=True)
    else:
        setter = get_wallpaper_setter(setter)
        setter(image_loc)
    click.echo('wallpaper set from {}'.format(content['url']))
    if to_log:
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



def get_downloader(downloader_name):
    downloader_module = download_finder.get_dlmodule(downloader_name)
    downloader_cls = getattr(downloader_module, '{}Downloader'.format(downloader_name.title()))
    return downloader_cls()

def get_wallpaper_setter(setter_name):
    setter_module = get_setter_dlmodule(setter_name)
    setter_func = getattr(setter_module, 'set_wallpaper')
    return setter_func

if __name__ == '__main__':
    cli()
