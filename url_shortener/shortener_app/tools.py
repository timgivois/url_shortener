import string
import random

def compress_url(large_url):
    # TODO
    # clean url
    # compress url
    return 'localhost:8000/' + ''.join(random.choice(string.ascii_letters) for x in range(10))