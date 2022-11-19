#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.urls import include
from django.urls import re_path

ROOT_URLCONF = __name__
urlpatterns = [re_path(r"^articles/", include('tests.app_urls'))]
