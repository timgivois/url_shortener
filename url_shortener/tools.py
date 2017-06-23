# coding=utf-8
import string
import random
import redis
import re
import requests
import logging
import logging.config

from settings import RANDOM_DIGITS, POSSIBLE_CHARS_URL
from url_shortener.settings import REDIS_CONFIGURATION


def clean_url(large_url):
    return re.sub('(/)$', '', re.sub('(#.+)$', '', large_url))


def append_http_if_needed(large_url):
    if re.search('^127\.0\.0\.1', large_url) or re.search('^localhost', large_url):
        large_url = 'http://' + large_url

    return large_url


def get_real_url(large_url):

    if re.search('^http', large_url):
        try:
            large_url = requests.get(large_url).url
        except requests.RequestException:
            logging.exception('Error ocurred when trying to transform url')

    return large_url


def validate_desired_url(desired_url):

    if len(desired_url) != RANDOM_DIGITS and len(desired_url) > 0:
        return False, {"error": {"message": "El tamaño de la url es de {0} y debe ser de {1}".format(len(desired_url),
                                                                                                     RANDOM_DIGITS)}}

    for letter in desired_url:
        if letter not in POSSIBLE_CHARS_URL:
            return False, {"error": {"message": "El caracter {0} no es válido para formar una url".format(letter)}}

    return True, {}


def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return regex.match(url)

class RedisHandler:
    def __init__(self):
        self.redis_db = redis.StrictRedis(**REDIS_CONFIGURATION)

    def key_in_cache(self, key):
        key = clean_url(key)
        return self.redis_db.get(key)

    def compress_url(self, large_url, desired_url):
        large_url = clean_url(large_url)

        short_url = self.key_in_cache(large_url)
        if not short_url:
            short_url = self.generate_unique_random_token(desired_url)
            self.add_urls_to_cache(short_url, large_url)

        return short_url

    def generate_unique_random_token(self, token):
        while not token or self.key_in_cache(token):
            token = ''.join(random.choice(POSSIBLE_CHARS_URL) for x in range(RANDOM_DIGITS))

        return token

    def add_urls_to_cache(self, short_url, large_url):
        self.redis_db.set(short_url, large_url)
        self.redis_db.set(large_url, short_url)
