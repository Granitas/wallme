import click

from wallme.wallpaper_setters.finder import WALL_SETTERS
from wallme.image_downloaders.finder import IMAGE_DOWNLOADERS
from wallme.downloaders import DOWNLOADERS


@click.command('list', help='list modules')
@click.option('--all', 'list_all', is_flag=True, help='list all modules')
def cli(list_all):
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
