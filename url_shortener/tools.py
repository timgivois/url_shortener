import string
import random
import redis
import re
import requests

from settings import RANDOM_DIGITS
from url_shortener.settings import REDIS_CONFIGURATION


def clean_url(large_url):
    return re.sub('(/)$', '', re.sub('(#.+)$', '', large_url))


def get_real_url(large_url):
    if not large_url.startswith('http'):
        large_url = 'http://' + large_url
    return requests.get(large_url).url


class RedisHandler:
    def __init__(self):
        self.redis_db = redis.StrictRedis(**REDIS_CONFIGURATION)

    def key_in_cache(self, key):
        key = clean_url(key)
        return self.redis_db.get(key)

    def compress_url(self, large_url):
        large_url = clean_url(large_url)

        short_url = self.key_in_cache(large_url)
        if not short_url:
            short_url = self.generate_unique_random_token()
            self.add_urls_to_cache(short_url, large_url)

        return short_url

    def generate_unique_random_token(self):
        token = False
        while not token or self.key_in_cache(token):
            token = ''.join(random.choice(string.ascii_letters) for x in range(RANDOM_DIGITS))

        return token

    def add_urls_to_cache(self, short_url, large_url):
        self.redis_db.set(short_url, large_url)
        self.redis_db.set(large_url, short_url)
