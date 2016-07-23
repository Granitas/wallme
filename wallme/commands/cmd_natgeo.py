import click

from wallme.commands import set_wallpaper
from wallme.downloaders.natgeo import NatgeoDownloader


@click.command('natgeo', help='download image from nationalgeographic.com (low resolution)')
@click.pass_context
@click.option('--list', 'list_categories', default=False, is_flag=True, help='list available categories')
@click.option('--category', default=None, help='category from which to download images, see --list')
@click.option('--position', default=0, help='image position +-[1..n]; (default=0 for random)')
def cli(cli_ctx, **kwargs):
    """Downloader for image of the day of nationalgeographic.com"""
    downloader = NatgeoDownloader()
    if kwargs['list_categories']:
        click.echo("Available Categories:")
        for cat in downloader.get_categories():
            click.echo(cat)
        return
    position = kwargs['position']
    position_text = 'random' if not position else position
    click.echo('setting image {} from category {}'
               .format(position_text, kwargs['category'] or downloader.default_cat))
    content = downloader.download(**kwargs, cli_ctx=cli_ctx)
    set_wallpaper(content, cli_ctx)
