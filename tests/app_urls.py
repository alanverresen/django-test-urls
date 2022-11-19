#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.urls import path
from django.urls import re_path

from tests import app_views as views


urlpatterns = [

    # an example of a URL with no named/unnamed groups
    path(
        route="",
        view=views.articles,
    ),

    # an example of a URL with unnamed groups
    re_path(
        route=r"^([0-9]{4})/(0[1-9]|1[0-2])$",
        view=views.monthly_archive,
    ),

    # an example of a URL with a named group
    path(
        route='<str:category>',
        view=views.categorical_archive,
    ),

    # an example of a URL with both named and unnamed groups
    re_path(
        route=r'^([0-9]{4})/(0[1-9]|1[0-2])/(?P<slug>[\w-]+)$',
        view=views.article,
    ),

]
