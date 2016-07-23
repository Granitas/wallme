import click
from wallme.commands import set_wallpaper
from wallme.downloaders.reddit import RedditDownloader


@click.command('reddit', help='download image from reddit.com')
@click.pass_context
@click.argument('subreddit')
@click.option('--position', '-p', default=0, help='choose position +-[1..25]; (default=0 for random)')
@click.option('--list-tabs', is_flag=True, help='list available tabs')
@click.option('--tab', '-t', default='hot', help='tab name')
def cli(cli_ctx, **kwargs):
    """Downloader for reddit.com"""
    tab, position, list_tabs, subreddit = [kwargs.get(x, None) for x in ['tab', 'position', 'list_tabs', 'subreddit']]
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
    content = downloader.download(**kwargs, cli_ctx=cli_ctx)
    set_wallpaper(content, cli_ctx)

