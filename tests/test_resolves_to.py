#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Contains tests for the function `resolves_to()`.

# Test Design
# -----------
# The function `resolves_to()` combines the functionality of the functions
# `resolves_to_view()` and `resolves_to_args()`, for which a set of tests is
# already available. A simple combinatorial set of tests should suffice to
# provide confidence:
# - matching/mismatching view
# - matching/mismatching args
#
# Also, because `resolves_to_args()` raises an exception if the expected
# arguments are expressed using an invalid type, there's a need for one
# additional test.

import pytest

from django_test_urls import resolves_to
from django_test_urls.exceptions import InvalidArgumentType
from tests import app_views as views


def test__resolves_to__match_view__match_args():
    """ Returns True when URL is mapped to view and args as expected.
    """
    assert resolves_to(
        "/url6/two-zero-two-two/11/",
        views.monthly_archive,
        (),
        {"year": "2022", "month": "11"})


def test__resolves_to__mismatch_view__match_args():
    """ Returns False when URL is mapped to a different view than expected.
    """
    assert not resolves_to(
        "/url2/2022/11/",
        views.article,
        (),
        {"year": "2022", "month": "11"})


def test__resolves_to__match_view__mismatch_args():
    """ Returns False when URL is mapped to different arguments than expected.
    """
    assert not resolves_to(
        "/url6/two-zero-two-two/11/",
        views.monthly_archive,
        (),
        {"year": "2021", "month": "03"})


def test__resolves_to__mismatch_view__mismatch_args():
    """ Returns False when URL is mapped to a different view and arguments.
    """
    assert not resolves_to(
        "/url6/two-zero-two-two/11/",
        views.article,
        (),
        {"year": "2021", "month": "03"})


def test__resolves_to__invalid_argument_type__args():
    """ Raises exception when arguments are expressed using invalid type.
    """
    with pytest.raises(InvalidArgumentType):
        resolves_to(
            "/url6/two-zero-two-two/11/",
            views.monthly_archive,
            {},  # not allowed!
            {"year": "2022", "month": "11"})


def test__resolves_to__invalid_argument_type__kwargs():
    """ Raises exception when arguments are expressed using invalid type.
    """
    with pytest.raises(InvalidArgumentType):
        resolves_to(
            "/url6/two-zero-two-two/11/",
            views.monthly_archive,
            (),
            {"2022", "11"})  # not allowed!
