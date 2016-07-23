import click
from wallme.downloaders.bing import BingDownloader
from wallme.commands import set_wallpaper


@click.command('bing', help='download image of the day from bing.com')
@click.pass_context
@click.option('--date', default=None, help='date of daily image in Y-m-d format')
@click.option('-p', '--position', default=0, help='position, -[1..n] days from today')
def cli(cli_ctx, **kwargs):
    """Downloader for image of the day of bing.com"""
    content = BingDownloader().download(**kwargs, cli_ctx=cli_ctx)
    set_wallpaper(content, cli_ctx)
