import logging
import random
import praw
from wallme.downloaders.base import BaseDownloader

from wallme.utils import fix_url_http


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
    def download(self, subreddit, tab, position=None):
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
        subreddit = self.downloader.get_subreddit(subreddit)
        # retrieve submissions
        submission_get_func = getattr(subreddit, 'get_{}'.format(tab), None)
        if not submission_get_func:
            logging.error('Incorrect tab {}'.format(tab))
        submissions = list(submission_get_func(limit=position or 0))  # download only as many we need; 0 == 25
        # choose a submission (either random or by position arg)
        if position is None:
            sub = random.choice(submissions)
        else:
            sub = submissions[position]
        # extract image url and meta data
        url = fix_url_http(sub.url)
        meta = {'score': sub.score,
                'title': sub.title,
                'url': sub.permalink}
        return self.download_image(url, meta)
