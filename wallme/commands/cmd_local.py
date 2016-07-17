import click

from wallme.commands import base
from wallme.downloaders.local import LocalNonDownloader


@click.command('local', help='set an image from local history')
@click.pass_context
@click.option('--year_month', default=None, help='specify year and month; format %Y%m')
@click.option('--position', default=0, help='position of image')
def cli(context, **kwargs):
    """Downloader (not really) for local wallme history"""
    position = kwargs['position']
    year_month = kwargs['year_month']
    position_text = 'random' if position is None else position
    click.echo("setting {} image from local history".format(position_text))
    content = LocalNonDownloader.download(year_month, position)
    context.obj['no_log'] = True
    base.set_wallpaper(content, context)
