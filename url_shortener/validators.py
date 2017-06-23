from tools import *
from django.shortcuts import render

redis_handler = RedisHandler()

def transform_validator(request):

    if request.method == 'POST':
        large_url = request.POST.get("large_url")
        desired_url = request.POST.get("desired_url")

        if not large_url or not is_valid_url(large_url):
            return False, render(request, 'transform.html', {'error': {'message': 'No es una URL valida'}})

        is_valid, error = validate_desired_url(desired_url)

        if not is_valid:
            return False, render(request, 'transform.html', error)

        designated_url = redis_handler.key_in_cache(desired_url)
        if designated_url:
            return False, render(request, 'transform.html', {'error': {'message':'Error, ya se le designo una URL a ese short, intenta con otro'}})

    return True, {}

def redirect_validator(request):
    short_url = request.get_full_path().replace('/', '')
    large_url = redis_handler.key_in_cache(short_url)

    if large_url:
        return True, {}
    else:
        return False, render(request, 'index.html', {'error': {'message': 'No es una URL valida'}})