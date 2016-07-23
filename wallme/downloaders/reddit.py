import logging
import random

import click
import praw

from wallme.downloaders import Image
from wallme.downloaders.base import BaseDownloader


class RedditDownloader(BaseDownloader):
    """
    Downloader for reddit.com
    """
    tabs = [
        'controversial',
        'controversial_from_all',
        'controversial_from_day',
        'controversial_from_hour',
        'controversial_from_month',
        'controversial_from_week',
        'controversial_from_year',
        'hot',
        'new',
        'rising',
        'top',
        'top_from_all',
        'top_from_day',
        'top_from_hour',
        'top_from_month',
        'top_from_week',
        'top_from_year']

    def __init__(self):
        super().__init__()
        self.downloader = praw.Reddit(user_agent='random_wallpaper')

    # noinspection PyMethodOverriding
    def download(self, **kwargs):
        """
        :param subreddit: subreddit to crawl; i.e. wallpapers for reddit.com/r/wallpapers
        :param position: position of post, None will download random
        :param tab: <Taken from `Praw` api wrapper>
        controversial,
        controversial_from_all,
        controversial_from_day,
        controversial_from_hour,
        controversial_from_month,
        controversial_from_week,
        controversial_from_year,
        hot,
        new,
        rising,
        top,
        top_from_all,
        top_from_day,
        top_from_hour,
        top_from_month,
        top_from_week,
        top_from_year
        :return: dict{'content': <image_content>, <some meta data>...}
        """
        subreddit = kwargs['subreddit']
        position = kwargs.get('position', 0)
        tab = kwargs.get('tab', None)
        rand = False
        if position == 0:
            rand = True
        if position > 1:
            position -= 1  # since 0 is reserved reduce position
        # retrieve submissions
        submission_get_func = getattr(self.downloader.get_subreddit(subreddit),
                                      'get_{}'.format(tab), None)
        if not submission_get_func:
            logging.error('Incorrect tab {}'.format(tab))
        submissions = list(submission_get_func())
        submissions = [s for s in submissions if '/comments/' not in s.url]
        if position + 1 > len(submissions):
            click.echo('position setting is incorrect, should be +-[1..25]')
            return
        # choose a submission (either random or by position arg)
        if rand:
            sub = random.choice(submissions)
        else:
            sub = submissions[position]
        # extract image url and meta data
        meta = {'score': sub.score,
                'title': sub.title,
                'url': sub.permalink}
        return self.process_url(Image(sub.url, meta), kwargs)
