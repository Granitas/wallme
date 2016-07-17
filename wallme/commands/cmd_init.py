import os

import click

from wallme.settings import WALLME_DIR


@click.command('init', help='create ~/.wallme/')
def cli():
    if not os.path.exists(WALLME_DIR):
        click.echo('creating {}'.format(WALLME_DIR))
        os.makedirs(WALLME_DIR)
        history_dir = os.path.join(WALLME_DIR, 'history')
        click.echo('creating {}'.format(history_dir))
        os.makedirs(history_dir)
    else:
        click.echo('{} already exists'.format(WALLME_DIR), err=True)
