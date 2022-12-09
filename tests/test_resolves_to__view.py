#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Contains tests for the function `resolves_to_view()`.

# Test Design
# -----------
# There are only 3 test cases that need to be tested:
# - URL is mapped to expected view
# - URL is mapped to a different view
# - URL cannot be mapped to a view

from django_test_urls.resolves_to import resolves_to_view
from tests import app_views as views


def test__matches_correct_view():
    """ Returns True when URL is mapped as expected.
    """
    assert resolves_to_view("/url1/", views.articles)


def test__matches_wrong_view():
    """ Returns False when URL is mapped to a different view.
    """
    assert not resolves_to_view("/url1/", views.monthly_archive)


def test__matches_no_view():
    """ Returns False when URL cannot be mapped to an existing view.
    """
    assert not resolves_to_view("/not/a/url", views.article)
