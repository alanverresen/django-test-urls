#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.urls import path
from django.urls import re_path

from tests import app_views as views


# - use prefix to simplify test design and avoid having to manage URL
#   resolution conflicts

urlpatterns = [

    # an example of a URL with no named/unnamed groups or extra arguments
    path(
        route="url1/",
        view=views.articles,
    ),

    # an example of a URL with a named group
    re_path(
        route=r"^url2/(?P<year>[0-9]{4})/(?P<month>0[1-9]|1[0-2])/$",
        view=views.monthly_archive,
    ),

    # an example of a URL with unnamed groups
    re_path(
        route=r"^url3/([0-9]{4})/(0[1-9]|1[0-2])/$",
        view=views.monthly_archive,
    ),

    # an example of a URL with only extra arguments
    path(
        route="url4/two-zero-two-two/one-one/",
        view=views.monthly_archive,
        kwargs={"year": "2022", "month": "11"},
    ),

    # an example of a URL with named and unnamed groups
    re_path(
        route=r"^url5/([0-9]{4})/(0[1-9]|1[0-2])/(?P<slug>[\w-]+)$",
        view=views.article,
    ),

    # an example of a URL with named groups and extra arguments
    re_path(
        route=r"^url6/two-zero-two-two/(?P<month>0[1-9]|1[0-2])/",
        view=views.monthly_archive,
        kwargs={"year": "2022"}
    ),

    # an example of a URL with unnamed groups and extra arguments
    re_path(
        route=r"^url7/two-zero-two-two/(0[1-9]|1[0-2])/",
        view=views.monthly_archive,
        kwargs={"year": "2022"},
    ),

    # an example of a URL with named, unnamed, and extra arguments
    re_path(
        route=r'^url8/two-zero-two-two/(0[1-9]|1[0-2])/(?P<slug>[\w-]+)$',
        view=views.article,
        kwargs={"year": "2022"},
    ),

    # extra: captures value for year, but then overwrites it
    re_path(
        route=r"^bad1/(?P<year>[0-9]{4})/(?P<month>0[1-9]|1[0-2])/$",
        view=views.monthly_archive,
        kwargs={"year": "2022"}
    ),

    # extra: maps positional and keyword arguments to same parameter
    re_path(
        route=r"^bad2/([0-9]{4})/(0[1-9]|1[0-2])/$",
        view=views.monthly_archive,
        kwargs={"year": "2022"},
    ),

    # extra: provides no positional argument for month parameter
    re_path(
        route=r"^bad3/([0-9]{4})/$",
        view=views.monthly_archive,
    ),

    # extra: provides no keyword argument for month parameter
    re_path(
        route=r"^bad4/(?P<year>[0-9]{4})/$",
        view=views.monthly_archive,
    ),

    # extra: captures too many positional arguments
    re_path(
        route=r"^bad5/([0-9]{4})/(0[1-9]|1[0-2])/([0-9]{2})/$",
        view=views.monthly_archive,
    ),

    # extra: captures too many keyword arguments
    re_path(
        route=r"^bad6/(?P<year>[0-9]{4})/(?P<month>0[1-9]|1[0-2])/(?P<day>[0-9]{2})/$",  # noqa: E501
        view=views.monthly_archive,
    ),

]
