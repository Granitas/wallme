import logging
import random
import praw
from wallme.downloaders.base import BaseDownloader

from wallme.utils import fix_url

_POSSIBLE_TABS = ['top', 'new', 'rising', 'hot', 'controversial']  # todo remove


class RedditDownloader(BaseDownloader):
    """"""

    def __init__(self):
        super().__init__()
        self.downloader = praw.Reddit(user_agent='random_wallpaper')

    def download(self, subreddit, tab, position=None):
        """
        :param position: position of post, None will download random
        :param tab:
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
        subreddit = self.downloader.get_subreddit(subreddit)
        # retrieve submissions
        submission_get_func = getattr(subreddit, 'get_{}'.format(tab), None)
        if not submission_get_func:
            logging.error('Incorrect tab {}'.format(tab))
        submissions = list(submission_get_func(limit=position or 0))  # download only as many we need; 0 == 25
        # choose a submision (either random or by position arg)
        if position is None:
            sub = random.choice(submissions)
        else:
            sub = submissions[position]
        # extract image url and meta data
        url = fix_url(sub.url)
        meta = {'score': sub.score,
                'title': sub.title,
                'url': sub.permalink}
        return self.download_image(url, meta)

