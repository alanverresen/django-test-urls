#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.urls import include
from django.urls import path


ROOT_URLCONF = __name__
urlpatterns = [path("", include('tests.app_urls'))]
