import click
from wallme.commands import base
from wallme.downloaders.reddit import RedditDownloader


@click.command('reddit', help='download image from reddit.com')
@click.pass_context
@click.argument('subreddit')
@click.option('--position', default=0, help='result position; 0 == random')
@click.option('--list-tabs', is_flag=True, help='list available tabs')
@click.option('--tab', default='hot', help='tab name')
def cli(cli_kwargs, subreddit, tab, position, list_tabs, *args):
    """Downloader for reddit.com"""
    downloader = RedditDownloader()
    if list_tabs:
        click.echo('Available Tabs:')
        for tab in downloader.tabs:
            click.echo(tab)
        return
    if tab not in downloader.tabs:
        click.echo('Incorrect tab see --list-tabs for viable options', err=True)
        return
    click.echo('setting random wallpaper from /r/{} {} tab'.format(subreddit, tab))
    content = downloader.download(subreddit, tab=tab, position=position or None)
    base.set_wallpaper(content, cli_kwargs)

