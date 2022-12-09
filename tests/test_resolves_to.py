#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Contains tests for the function `resolves_to()`.

# Test Design
# -----------
# The function `resolves_to()` makes consecutive calls to the functions
# `check_for_mismatches()`, `resolves_to_view()`, and `resolves_to_args()`,
# which have been tested individually.
#
# A simple combinatorial set of tests should suffice to provide confidence:
# - URL is mapped to the correct view (y/n)
# - arguments are captured as expected (y/n)
# - no mismatch between view's parameter and captured arguments (y/n)
#
# Also, tests are needed to verify that:
# - exceptions are raised when an argument with the wrong type is passed
# - a list can be used instead of a tuple to express keyword arguments

import pytest

from django_test_urls.resolves_to import resolves_to
from django_test_urls.exceptions import ArgumentParameterMismatch
from django_test_urls.exceptions import InvalidArgumentType

from tests import app_views as views


def test__revolves_to__invalid_argument_type__url_path():
    """ Raises exception when argument for URL path has the wrong type.
    """
    with pytest.raises(InvalidArgumentType) as e:
        resolves_to(
            None,  # <-- bad type
            views.monthly_archive,
            (),
            {"year": "2021", "month": "11"})
    assert "url_path must be a str" in str(e)


def test__revolves_to__invalid_argument_type__view():
    """ Raises exception when argument for view has the wrong type.
    """
    with pytest.raises(InvalidArgumentType) as e:
        resolves_to(
            "/url6/two-zero-two-two/11/",
            None,  # <-- bad type
            (),
            {"year": "2021", "month": "11"})
    assert "expected_view must be a function" in str(e)


def test__resolves_to__invalid_argument_type__args():
    """ Raises exception when argument for positional args has the wrong type.
    """
    with pytest.raises(InvalidArgumentType) as e:
        resolves_to(
            "/url6/two-zero-two-two/11/",
            views.monthly_archive,
            {},  # `set` instance is not allowed!
            {"year": "2022", "month": "11"})
    assert "expected_args must be a tuple or list" in str(e)


def test__resolves_to__invalid_argument_type__kwargs():
    """ Raises exception when argument for keyword args has the wrong type.
    """
    with pytest.raises(InvalidArgumentType) as e:
        resolves_to(
            "/url6/two-zero-two-two/11/",
            views.monthly_archive,
            (),
            {"2022", "11"})  # `set` instance is not allowed!
    assert "expected_kwargs must be a dict" in str(e)


def test__resolves_to__using_a_list_for_positional_arguments():
    """ Can use a list to express positional arguments instead of a tuple.
    """
    assert resolves_to(
        "/url3/2022/11/",
        views.monthly_archive,
        ["2022", "11"],
        {})


def test__resolves_to__match_view__match_args__match_sign():
    """ Returns True when:
        - [O] URL is mapped to the correct view
        - [O] arguments are captured as expected
        - [O] no mismatch between view's parameter and captured arguments
    """
    assert resolves_to(
        "/url6/two-zero-two-two/11/",
        views.monthly_archive,
        (),
        {"year": "2022", "month": "11"})


def test__resolves_to__match_view__match_args__mismatch_sign():
    """ Raises exception when:
        - [O] URL is mapped to the correct view
        - [O] arguments are captured as expected
        - [X] no mismatch between view's parameter and captured arguments
    """
    with pytest.raises(ArgumentParameterMismatch):
        resolves_to(
            "/bad4/2022/",
            views.monthly_archive,
            (),
            {"year": "2022"}
        )


def test_resolves_to__match_view__mismatch_args__match_sign():
    """ Returns False when:
        - [O] URL is mapped to the correct view
        - [X] arguments are captured as expected
        - [O] no mismatch between view's parameter and captured arguments
    """
    assert not resolves_to(
        "/url6/two-zero-two-two/11/",
        views.monthly_archive,
        (),
        {"year": "2021", "month": "03"})


def test_resolves_to__match_view__mismatch_args__mismatch_sign():
    """ Raises exception when:
        - [O] URL is mapped to the correct view
        - [X] arguments are captured as expected
        - [X] no mismatch between view's parameter and captured arguments
    """
    with pytest.raises(ArgumentParameterMismatch):
        resolves_to(
            "/bad4/2022/",
            views.monthly_archive,
            (),
            {"year": "2021"})


def test__resolves_to__mismatch_view__match_args__match_sign():
    """ Returns False when:
        - [X] URL is mapped to the correct view
        - [O] arguments are captured as expected
        - [O] no mismatch between view's parameter and captured arguments
    """
    assert not resolves_to(
        "/url6/two-zero-two-two/11/",
        views.other_monthly_archive,
        (),
        {"year": "2022", "month": "11"})


def test__resolves_to__mismatch_view__match_args__mismatch_sign():
    """ Raises exception when:
        - [X] URL is mapped to the correct view
        - [O] arguments are captured as expected
        - [X] no mismatch between view's parameter and captured arguments
    """
    with pytest.raises(ArgumentParameterMismatch):
        resolves_to(
            "/bad4/2022/",
            views.other_monthly_archive,
            (),
            {"year": "2022"})


def test__resolves_to__mismatch_view__mismatch_args__match_sign():
    """ Returns False when:
        - [X] URL is mapped to the correct view
        - [X] arguments are captured as expected
        - [O] no mismatch between view's parameter and captured arguments
    """
    assert not resolves_to(
        "/url6/two-zero-two-two/11/",
        views.other_monthly_archive,
        (),
        {"year": "2021", "month": "03"})


def test__resolves_to__mismatch_view__mismatch_args__mismatch_sign():
    """ Raises exception when:
        - [X] URL is mapped to the correct view
        - [X] arguments are captured as expected
        - [X] no mismatch between view's parameter and captured arguments
    """
    with pytest.raises(ArgumentParameterMismatch):
        resolves_to(
            "/bad4/2022/",
            views.other_monthly_archive,
            (),
            {"year": "2021"})
