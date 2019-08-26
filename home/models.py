# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Image(models.Model):
    name = models.CharField(max_length=524, blank=True)
    images = models.FileField(upload_to='uploads/')


class Api_Images(models.Model):
    image = models.FileField(upload_to='api_uploads/')
