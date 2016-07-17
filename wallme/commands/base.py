import subprocess
from datetime import datetime
import json
import click
import os
from wallme.settings import WALLME_DIR
from wallme.wallpaper_setters.finder import find_setter_module


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
    if not os.path.exists(file_dir):
        with open(file_dir, 'wb') as image_file:
            image_file.write(content['content'])
    # save history file
    del content['content']  # we don't want content in history so del it
    try:
        with open(history_dir, 'r') as history_json:
            jcontent = history_json.read()
    except FileNotFoundError:
        jcontent = None
    if not jcontent:
        jcontent = json.dumps({'items': []})
    j = json.loads(jcontent)
    j['items'].append(content)
    with open(history_dir, 'w') as history_json:
        history_json.write(json.dumps(j, indent=2))


def set_wallpaper(content, context):
    """
    finds a setter module and uses it to set a wallpaper
    :param content: content dict for image
    :param context: cli interface context
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
    if context.obj['notify']:
        click.echo("trying to send notify")
        subprocess.Popen(['notify-send', 'Wallme change to:', content['url']])


def get_wallpaper_setter(setter_name):
    """find wallpaper setter by name"""
    setter_module = find_setter_module(setter_name)
    setter_func = getattr(setter_module, 'set_wallpaper')
    return setter_func
