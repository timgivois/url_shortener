# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import F
from django.shortcuts import redirect
from django.shortcuts import render
from models import Url_Transformations

from tools import RedisCompresser

compreser = RedisCompresser()

def index(request):
    return render(request, 'index.html')

def view(request):
    all_urls = Url_Transformations.objects.all()
    context = {'all_urls': all_urls, 'host': request.get_host()}

    return render(request, 'view.html', context)

def transform(request):
    context = {}

    if request.method == 'POST':
        print request.POST.items()
        large_url = request.POST.get("large_url")

        if not large_url:
            return render(request, 'transform.html', {})

        short_url = compreser.key_in_cache(large_url)
        if short_url:
            context = {'short_url': short_url, 'host': request.get_host()}
        else:
            url_transformation = Url_Transformations.objects.create(large_url=large_url,
                                                                    short_url=compreser.compress_url(large_url))
            url_transformation.save()
            context = {'short_url': url_transformation.short_url, 'host': request.get_host()}

    return render(request, 'transform.html', context)

def redirect_short_url(request):
    short_url = request.get_full_path().replace('/', '')
    print short_url
    large_url = compreser.key_in_cache(short_url)
    print large_url
    if large_url:
        Url_Transformations.objects.filter(short_url=short_url).update(count_visited=F('count_visited')+1)
        return redirect(large_url)
    else:
        return render(request, 'index.html')
