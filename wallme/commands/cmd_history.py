import json

import click

from wallme.history import get_history


@click.command('history', help='display history')
@click.option('-n', '--count', 'count', default=1, help='amount of items to display')
@click.option('--year_month', help='filter specific month of the year, format %Y%m')
@click.option('--raw', is_flag=True, help='return raw json for parsing')
def cli(**kwargs):
    count = kwargs['count']
    year_month = kwargs['year_month']
    raw = kwargs['raw']
    items = list(get_history(year_month))
    items = items[::-1][:count][::-1]
    if raw:
        click.echo(json.dumps(items, sort_keys=True, indent=2))
        return
    for item in items:
        click.echo(json.dumps(item[0], sort_keys=True, indent=2))


