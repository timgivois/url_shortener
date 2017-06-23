# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Count
from django.db.models import Max, Min
from django.shortcuts import redirect
from django.shortcuts import render
from models import Url_Transformations

from tools import RedisHandler, get_real_url

redis_handler = RedisHandler()


def index(request):
    return render(request, 'index.html')


def view(request):
    results_clicks = Url_Transformations.objects.values('short_url', 'large_url')\
        .annotate(count = Count('short_url')-1,
                  created_at = Min('retrieved_at'),
                  last_retrieved_at = Max('retrieved_at'))\
        .order_by('-count')

    context = {'results_clicks': results_clicks, 'host': request.get_host()}

    return render(request, 'view.html', context)


def transform(request):
    context = {}

    if request.method == 'POST':
        large_url = request.POST.get("large_url")
        
        if not large_url:
            return render(request, 'transform.html', {})

        large_url = get_real_url(large_url)
        short_url = redis_handler.key_in_cache(large_url)
        
        if not short_url:
            short_url = redis_handler.compress_url(large_url)
            Url_Transformations.objects.create(large_url=large_url, short_url=short_url).save()

        context = {'short_url': short_url, 'host': request.get_host()}

    return render(request, 'transform.html', context)


def redirect_short_url(request):
    short_url = request.get_full_path().replace('/', '')
    large_url = redis_handler.key_in_cache(short_url)
    
    if large_url:
        Url_Transformations.objects.create(short_url=short_url, large_url=large_url).save()

        return redirect(large_url)
    else:
        return render(request, 'index.html')
