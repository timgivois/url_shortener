# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from shortener_app.tools import compress_url
from django.shortcuts import render
from shortener_app.models import Url_Transformations


def index(request):
    return render(request, 'index.html')

def view(request):
    all_urls = Url_Transformations.objects.all()
    context = {'all_urls': all_urls}

    return render(request, 'view.html', context)

def transform(request):
    context = {}

    if request.method == 'POST':
        print request.POST.items()
        large_url = request.POST.get("large_url", "asd")
        url_transformation = Url_Transformations.objects.get_or_create(large_url=large_url)[0]
        url_transformation.short_url = url_transformation.short_url if url_transformation.short_url else compress_url(large_url)
        url_transformation.save()
        context = {'short_url':url_transformation.short_url}

    return render(request, 'transform.html', context)

def redirect_short_url(request):

    large_url = request.get_host() + request.get_full_path()
    print large_url
    if Url_Transformations.objects.filter(short_url=large_url):

        return redirect(Url_Transformations.objects.filter(short_url=large_url)[0].large_url)

    else:
        return render(request, 'index.html')
