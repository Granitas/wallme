import logging
import os
import click
import sys

from wallme.wallpaper_setters.finder import WALL_SETTERS

cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'commands'))


class ComplexCLI(click.MultiCommand):
    """Adjust click.Group to detect commands properly from wallme.commands location"""
    def list_commands(self, ctx):
        """list all commands from wallme.commands sub-package"""
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and \
                    filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        """return a command from wallme.commands sub-package"""
        if sys.version_info[0] == 2:
            name = name.encode('ascii', 'replace')
        mod = __import__('wallme.commands.cmd_{}'.format(name),
                         None, None, ['cli'])
        return mod.cli


@click.command(cls=ComplexCLI)
@click.version_option()
@click.option('--verbose', help='set verbosity', is_flag=True)
@click.option('--notify', help='send notify-send to the system', is_flag=True)
@click.option('--no-log', help='log wallpaper', is_flag=True)
@click.option('--setter_script', help='script to set wallpaper, {file} replaced with filename')
@click.option('--setter', help='script that sets wallpaper',
              type=click.Choice(WALL_SETTERS),
              default='feh')
@click.pass_context
def cli(context, **kwargs):
    """
    Modular wallpaper getter and setter.
    """
    context.obj = kwargs
    if kwargs['verbose']:
        log_stream = logging.StreamHandler()
        log_stream.setLevel(logging.DEBUG)
        logging.basicConfig(handlers=[log_stream])

