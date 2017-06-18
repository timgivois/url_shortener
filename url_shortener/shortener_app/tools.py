import string
import random
import redis
import re

def clean_url(large_url):
    return re.sub('(#.+)$', '', large_url)

class RedisCompresser:
    def __init__(self, host='localhost', port=6379, db=0, **kwargs):
        self.redis_db = redis.StrictRedis(host=host, port=port, db=db, **kwargs)

    def key_in_cache(self, key):
        return self.redis_db.get(key)

    def compress_url(self, large_url):
        large_url = clean_url(large_url)

        short_url = self.key_in_cache(large_url)
        if not short_url:
            short_url = self.generate_unique_random_token()
            self.redis_db.set(short_url, large_url)
            self.redis_db.set(large_url, short_url)

        return short_url

    def generate_unique_random_token(self):
        token = False
        while not token and self.key_in_cache(token):
            token = ''.join(random.choice(string.ascii_letters) for x in range(10))

        return token
