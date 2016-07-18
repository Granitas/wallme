import json

import click

from wallme.history import get_history


@click.command('history', help='display history')
@click.option('-c', '--count', 'count', default=1, help='amount of items to display')
@click.option('-p', '--position', 'position', default=None, help='amount of items to display')
@click.option('--year_month', help='filter specific month of the year, format %Y%m')
@click.option('--raw', is_flag=True, help='return raw json for parsing')
def cli(count, year_month, raw, position, **kwargs):

    def print_item(item):
        click.echo(json.dumps(item, sort_keys=True, indent=2))

    all_items = list(get_history(year_month))
    if position is not None:
        print_item(all_items[int(position)][0])
        return
    items = all_items[::-1][:count][::-1]
    if raw:
        print_item(items)
        return
    for item in items:
        print_item(item[0])
