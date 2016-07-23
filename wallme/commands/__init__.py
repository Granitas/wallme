import subprocess
import click
import os

from wallme.history import log_wallpaper
from wallme.wallpapersetters import find_setter_module


def set_wallpaper(content, cli_ctx):
    """
    finds a setter module and uses it to set a wallpaper
    :param content: content dict for image
    :param cli_ctx: cli interface context
    """
    if not content:
        return
    home = os.path.expanduser('~')
    image_loc = os.path.join(home, '.wallme/wallpaper')
    with open(image_loc, 'wb') as wallme_file:
        wallme_file.write(content['content'])
    # set wallpaper
    setter_script = cli_ctx.obj['setter_script']
    if setter_script:
        subprocess.Popen(setter_script.format(file=image_loc), shell=True)
    else:
        setter = get_wallpaper_setter(cli_ctx.obj['setter'])
        setter(image_loc)
    click.echo('wallpaper set from {}'.format(content['url']))
    if not cli_ctx.obj['no_log']:
        click.echo('saving wallpaper to log')
        log_wallpaper(content)
    if cli_ctx.obj['notify']:
        click.echo("trying to send notify")
        subprocess.Popen(['notify-send', 'Wallme change to:', content['url']])


def get_wallpaper_setter(setter_name):
    """find wallpaper setter by name"""
    setter_module = find_setter_module(setter_name)
    setter_func = getattr(setter_module, 'set_wallpaper')
    return setter_func
