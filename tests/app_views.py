#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.http import HttpResponse


def articles(request):
    return HttpResponse("<h1>Articles</h1>")


def monthly_archive(request, year, month):
    return HttpResponse("<h1>Monthly Archive</h1>")


def categorical_archive(request, category):
    return HttpResponse("<h1>Categorical Archive</h1>")


def article(request, year, month, slug):
    return HttpResponse("<h1>Article</h1>")
