import click
from wallme.downloaders.bing import BingDownloader
from wallme.commands import set_wallpaper


@click.command('bing', help='download image of the day from bing.com')
@click.pass_context
@click.option('--date', default=None, help='date of daily image in Y-m-d format')
def cli(context, **kwargs):
    """Downloader for image of the day of bing.com"""
    date = kwargs['date']
    click.echo('setting daily image from bing for {} as wallpaper'.format(date or 'Today'))
    content = BingDownloader().download(date)
    set_wallpaper(content, context)
