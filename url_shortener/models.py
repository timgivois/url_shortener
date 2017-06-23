# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from tools import clean_url

# Create your models here.

class Url_Transformations(models.Model):
    large_url = models.CharField(db_index=True, max_length=2000)
    short_url = models.CharField(db_index=True, max_length=10)
    retrieved_at = models.DateTimeField(db_index=True, auto_now=True)

    def save(self, *args, **kwargs):
        self.large_url = clean_url(self.large_url)
        super(Url_Transformations, self).save(*args, **kwargs)