# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Count
from django.db.models import Max, Min
from django.shortcuts import redirect
from django.shortcuts import render
from models import Url_Transformations
from multiprocessing import Process
from django.db import transaction

from tools import RedisHandler, get_real_url
from validators import transform_validator, redirect_validator

redis_handler = RedisHandler()


def async_insertion(short_url, large_url):
    Url_Transformations.objects.create(short_url=short_url, large_url=large_url, count=0).save()


def async_plus_one(short_url, large_url):
    with transaction.atomic():
        transf = Url_Transformations.objects.select_for_update().filter(short_url=short_url, large_url=large_url)
        if transf:
            transf[0].count = transf[0].count + 1
            transf[0].save()


def index(request):
    return render(request, 'index.html')


def view(request):
    results_clicks = Url_Transformations.objects.all()

    context = {'results_clicks': results_clicks, 'host': request.get_host()}

    return render(request, 'view.html', context)


def transform(request):
    context = {}

    is_valid_request, error_response = transform_validator(request)

    if is_valid_request:
        if request.method == 'POST':
            large_url = request.POST.get("large_url")
            desired_url = request.POST.get("desired_url")

            large_url = get_real_url(large_url)
            short_url = redis_handler.key_in_cache(large_url)

            if not short_url:
                short_url = redis_handler.compress_url(large_url, desired_url)
                Process(target=async_insertion, args=(short_url, large_url,)).run()

            context = {'short_url': short_url, 'host': request.get_host()}
    else:

        return error_response

    return render(request, 'transform.html', context)


def redirect_short_url(request):
    is_valid_request, error_response = redirect_validator(request)

    if is_valid_request:
        short_url = request.get_full_path().replace('/', '')
        large_url = redis_handler.key_in_cache(short_url)

        Process(target=async_plus_one, args=(short_url, large_url,)).run()

        return redirect(large_url)
    else:

        return error_response
