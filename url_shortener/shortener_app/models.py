# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Url_Transformations(models.Model):
    large_url = models.TextField()
    short_url = models.CharField(max_length=10, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    count_visited = models.IntegerField(default=0)
