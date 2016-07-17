import click

from wallme.commands import base
from wallme.downloaders.natgeo import NatgeoDownloader


@click.command('natgeo', help='download image from nationalgeographic.com (low resolution)')
@click.pass_context
@click.option('--list', default=False, is_flag=True, help='list available categories')
@click.option('--category', default=None, help='category from which to download images, see --list')
@click.option('--position', default=None, type=click.INT, help='image position, default random')
def cli(cli_kwargs, category, position, list, *args):
    """Downloader for image of the day of nationalgeographic.com"""
    downloader = NatgeoDownloader()
    if list:
        click.echo("Available Categories:")
        for cat in downloader.get_categories():
            click.echo(cat)
        return
    position_text = 'random' if position is None else position
    click.echo('setting image {} from category {}'
               .format(position_text, category or downloader.default_cat))
    content = downloader.download(category, position)
    base.set_wallpaper(content, cli_kwargs)
