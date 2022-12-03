#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Contains tests for the function `resolves_to_args()`.

# Test Design
# -----------
# There are 8 different types of URL patterns that need to be tested,
# depending on the combination of types of groups that are used to capture
# arguments:
# - named groups (y/n)
# - unnamed groups (y/n)
# - extra arguments (y/n)
#
# For each combination, the following cases should be tested:
# - correct/incorrect args
# - correct/incorrect kwargs
#
# Extra Cases
# ~~~~~~~~~~~
# When a URL doesn't match with a single URL pattern, there is no URL pattern
# available to extract arguments with. A test case needs to make sure that
# False is returned in this case.
#
# All tests are written with tuples; add an extra test to make sure that a
# list can be used instead of a tuple to express the args.
#
# When an invalid data type is used to express the expected args or kwargs,
# then an exception should be raised.
#
# When a URL has a named regex group and an extra argument with the same key,
# then the extra argument's value should overwrite the one captured by the
# named regex group.
#
# Problems involving mismatches between the captured values and view
# parameters should result in an exception being raised down the line.
# However, at this stage, args and kwargs should be captured as expected.
#

import pytest

from django_test_urls import resolves_to_arguments
from django_test_urls.exceptions import InvalidArgumentType


# ----------------------------------------------------------------------------
# URL PATTERN WITH NO NAMED OR UNNAMED GROUPS OR EXTRA ARGUMENTS
# ----------------------------------------------------------------------------

def test__pattern1__matching_values():
    """ Returns True when a URL pattern with no named groups, no unnamed
        groups, and no extra args is checked against matching values.
    """
    assert resolves_to_arguments("/url1/", (), {})


def test__pattern1__mismatching_values__bad_tuple():
    """ Returns False when a URL pattern with no named groups, no unnamed
        groups, and no extra args is checked against a non-empty tuple.
    """
    assert not resolves_to_arguments("/url1/", ("a",), {})


def test__pattern1__mismatching_values__bad_dict():
    """ Returns False when a URL pattern with no named groups, no unnamed
        groups, and no extra args is checked against a non-empty dict.
    """
    assert not resolves_to_arguments("/url1/", (), {"a": "b"})


def test__pattern1__mismatching_values__bad_all():
    """ Returns False when a URL pattern with no named groups, no unnamed
        groups, and no extra args is checked against all bad values.
    """
    assert not resolves_to_arguments("/url1/", ("a",), {"b": "c"})


# ----------------------------------------------------------------------------
# URL PATTERN WITH NAMED GROUPS
# ----------------------------------------------------------------------------

def test__pattern2__matching_values():
    """ Returns True when a URL pattern with named groups is checked against
        matching values.
    """
    assert resolves_to_arguments(
        "/url2/2022/11/", (), {"year": "2022", "month": "11"})


def test__pattern2__mismatching_values__bad_tuple():
    """ Returns False when a URL pattern with named groups is checked against
        a tuple with mismatching values.
    """
    assert not resolves_to_arguments(
        "/url2/2022/11/", ("a",), {"year": "2022", "month": "11"})


def test__pattern2__mismatching_values__bad_dict():
    """ Returns False when a URL pattern with named groups is checked against
        a dict with mismatching values.
    """
    assert not resolves_to_arguments(
        "/url2/2022/11/", (), {"year": "1970", "month": "01"})


def test__pattern2__mismatching_values__bad_all():
    """ Returns False when a URL pattern with named groups is checked against
        all bad values.
    """
    assert not resolves_to_arguments(
        "/url2/2022/11/", ("a",), {"year": "1970", "month": "01"})


# ----------------------------------------------------------------------------
# URL PATTERN WITH UNNAMED GROUPS
# ----------------------------------------------------------------------------

def test__pattern3__matching_values():
    """ Returns True when a URL pattern with unnamed groups is checked against
        matching values.
    """
    assert resolves_to_arguments("/url3/2022/11/", ("2022", "11"), {})


def test__pattern3__mismatching_values__bad_tuple():
    """ Returns False when a URL pattern with unnamed groups is checked
        against a tuple with mismatching values.
    """
    assert not resolves_to_arguments("/url3/2022/11/", ("1970", "01"), {})


def test__pattern3__mismatching_values__bad_dict():
    """ Returns False when a URL pattern with unnamed groups is checked
        against a dict with mismatching values.
    """
    assert not resolves_to_arguments(
        "/url3/2022/11/", ("2022", "11"), {"a": "b"})


def test__pattern3__mismatching_values__bad_all():
    """ Returns False when a URL pattern with unnamed groups is checked
        against a dict with mismatching values.
    """
    assert not resolves_to_arguments(
        "/url3/2022/11/", ("1970", "01"), {"a": "b"})


# ----------------------------------------------------------------------------
# URL PATTERN WITH EXTRA ARGUMENTS
# ----------------------------------------------------------------------------

def test__pattern4__matching_values():
    """ Returns True when a URL pattern with extra arguments is checked
        against matching values.
    """
    assert resolves_to_arguments(
        "/url4/two-zero-two-two/one-one/",
        (),
        {"year": "2022", "month": "11"})


def test__pattern4__mismatching_values__bad_tuple():
    """ Returns False when a URL pattern with extra arguments is checked
        against a tuple with mismatching values.
    """
    assert not resolves_to_arguments(
        "/url4/two-zero-two-two/one-one/",
        ("a",),
        {"year": "2022", "month": "11"})


def test__pattern4__mismatching_values__bad_dict():
    """ Returns False when a URL pattern with extra arguments is checked
        against a dict with mismatching values.
    """
    assert not resolves_to_arguments(
        "/url4/two-zero-two-two/one-one/",
        (),
        {"year": "1970", "month": "01"})


def test__pattern4__mismatching_values__bad_all():
    """ Returns False when a URL pattern with extra arguments is checked
        against mismatching values.
    """
    assert not resolves_to_arguments(
        "/url4/two-zero-two-two/one-one/",
        ("a",),
        {"year": "1970", "month": "01"})


# ----------------------------------------------------------------------------
# URL PATTERN WITH NAMED AND UNNAMED GROUPS
# ----------------------------------------------------------------------------

def test__pattern5__matching_values():
    """ Returns True when a URL with both named and unnamed groups is checked
        against matching values.
    """
    assert resolves_to_arguments("/url5/2022/11/hello", (), {'slug': 'hello'})


def test__pattern5__mismatching_values__bad_tuple():
    """ Returns False when a URL with both named and unnamed groups is checked
        against a tuple with mismatching values.
    """
    assert not resolves_to_arguments(
        "/url5/2022/11/hello",
        ("2022", "11"),  # values aren't captured by Django!
        {'slug': 'hello'})


def test__pattern5__mismatching_values__bad_dict():
    """ Returns False when a URL with both named and unnamed groups is checked
        against a dict with mismatching values.
    """
    assert not resolves_to_arguments(
        "/url5/2022/11/hello", (), {'slug': 'bye'})


def test__pattern5__mismatching_values__bad_all():
    """ Returns False when a URL with both named and unnamed groups is checked
        against mismatching values.
    """
    assert not resolves_to_arguments(
        "/url/2022/11/hello",
        ("2022", "11"),  # values aren't captured by Django!
        {'slug': 'bye'})


# ----------------------------------------------------------------------------
# URL PATTERN WITH NAMED GROUPS AND EXTRA ARGUMENTS
# ----------------------------------------------------------------------------

def test__pattern6__matching_values():
    """ Returns True when a URL with named groups and extra arguments is
        checked against matching values.
    """
    assert resolves_to_arguments(
        "/url6/two-zero-two-two/11/", (), {"year": "2022", "month": "11"})


def test__pattern6__mismatching_values__bad_tuple():
    """ Returns False when a URL with named groups and extra arguments is
        checked against a tuple with mismatching values.
    """
    assert not resolves_to_arguments(
        "/url6/two-zero-two-two/11/", ("a",), {"year": "2022", "month": "11"})


def test__pattern6__mismatching_values__bad_dict():
    """ Returns False when a URL with named groups and extra arguments is
        checked against a dict with mismatching values.
    """
    assert not resolves_to_arguments(
        "/url6/two-zero-two-two/11/", (), {"year": "1970", "month": "03"})


def test__pattern6__mismatching_values__bad_all():
    """ Returns False when a URL with named groups and extra arguments is
        checked against mismatching values.
    """
    assert not resolves_to_arguments(
        "/url6/two-zero-two-two/11/", ("a",), {"year": "1970", "month": "03"})


# ----------------------------------------------------------------------------
# URL PATTERN WITH UNNAMED GROUPS AND EXTRA ARGUMENTS
# ----------------------------------------------------------------------------

def test__pattern7__matching_values():
    """ Returns True when a URL with unnamed groups and extra arguments is
        checked against matching values.
    """
    assert resolves_to_arguments(
        "/url7/two-zero-two-two/11/", ("11",), {"year": "2022"})


def test__pattern7__mismatching_values__bad_tuple():
    """ Returns False when a URL with unnamed groups and extra arguments is
        checked against a tuple with mismatching values.
    """
    assert not resolves_to_arguments(
        "/url7/two-zero-two-two/11/", ("a",), {"year": "2022"})


def test__pattern7__mismatching_values__bad_dict():
    """ Returns False when a URL with unnamed groups and extra arguments is
        checked against a dict with mismatching values.
    """
    assert not resolves_to_arguments(
        "/url7/two-zero-two-two/11/", ("11",), {"year": "1970"})


def test__pattern7__mismatching_values__bad_all():
    """ Returns False when a URL with unnamed groups and extra arguments is
        checked against mismatching values.
    """
    assert not resolves_to_arguments(
        "/url7/two-zero-two-two/11/", ("a",), {"year": "1970"})


# ----------------------------------------------------------------------------
# URL PATTERN WITH NAMED AND UNNAMED GROUPS AND EXTRA ARGUMENTS
# ----------------------------------------------------------------------------

def test__pattern8__matching_values():
    """ Return True when a URL with named groups, unnamed groups, and extra
        arguments is checked against matching values.
    """
    assert resolves_to_arguments(
        "/url8/two-zero-two-two/11/hello",
        (),
        {"slug": "hello", "year": "2022"})


def test__pattern8__mismatching_values__bad_tuple():
    """ Return False when a URL with named groups, unnamed groups, and extra
        arguments is checked against a tuple with mismatching values.
    """
    assert not resolves_to_arguments(
        "/url8/two-zero-two-two/11/hello",
        ("11",),  # values aren't captured by Django!
        {"slug": "hello", "year": "2022"})


def test__pattern8__mismatching_values__bad_dict():
    """ Return False when a URL with named groups, unnamed groups, and extra
        arguments is checked against a dict with mismatching values.
    """
    assert not resolves_to_arguments(
        "/url8/two-zero-two-two/11/hello",
        (),
        {"slug": "bye", "year": "1970"})


def test__pattern8__mismatching_values__bad_all():
    """ Return False when a URL with named groups, unnamed groups, and extra
        arguments is checked against mismatching values.
    """
    assert not resolves_to_arguments(
        "/url8/two-zero-two-two/11/hello",
        ("11",),  # values aren't captured by Django!
        {"slug": "bye", "year": "1970"})


# ----------------------------------------------------------------------------
# USING LIST INSTEAD OF TUPLE
# ----------------------------------------------------------------------------

def test__using_list_instead_of_tuple_for_args():
    """ Can use a list instead of a tuple for `args` parameter.
    """
    assert resolves_to_arguments("/url3/2022/11/", ["2022", "11"], {})


# ----------------------------------------------------------------------------
# NO MATCHING VIEW
# ----------------------------------------------------------------------------

def test__url_does_not_match_any_pattern():
    """ Returns False when a URL does not match any URL pattern.
    """
    assert not resolves_to_arguments("/no/such/url/", (), {})
    assert not resolves_to_arguments("/no/such/url/", ("a",), {})


# ----------------------------------------------------------------------------
# INVALID ARGUMENT TYPE PASSED
# ----------------------------------------------------------------------------

def test__invalid_argument_type__args():
    """ Exception is raised when wrong data type is used to express args.
    """
    with pytest.raises(InvalidArgumentType):
        assert not resolves_to_arguments("/url3/2022/11/", {"2022", "11"}, {})


def test__invalid_argument_type__kwargs():
    """ Exception is raised when wrong data type is used to express kwargs.
    """
    with pytest.raises(InvalidArgumentType):
        resolves_to_arguments("/url2/2022/11/", (), {"2022", "11"})


# ----------------------------------------------------------------------------
# EXTRA ARGUMENT OVERWRITES KWARGS
# ----------------------------------------------------------------------------

def test__extra_arg_overwrites_keyword_arg__check_against_extra():
    """ True is returned when a URL that overwrites a captured kwarg is
        checked against the value of the extra argument.
    """
    assert resolves_to_arguments(
        "/bad1/1980/11/",
        (),
        {"year": "2022", "month": "11"})


def test__extra_arg_overwrites_keyword_arg__check_against_keyword():
    """ False is returned when a URL that overwrites a captured kwarg is
        checked against the value of the keyword argument.
    """
    assert not resolves_to_arguments(
        "/bad1/1980/11/",
        (),
        {"year": "1980", "month": "11"})


# ----------------------------------------------------------------------------
# MISMATCHES BETWEEN CAPTURED VALUES AND VIEW PARAMETERS
# ----------------------------------------------------------------------------

def test__mapping_parameters_mismatch__pos_key_args_collision():
    """ True is returned, even when captured args and kwargs will cause an
        exception in the future due to multiple arguments being mapped to the
        same parameter of a view. This situation can only occur when extra
        arguments are provided in addition to unnamed regex groups.
    """
    assert resolves_to_arguments(
        "/bad2/1970/11/", ("1970", "11"), {"year": "2022"})


def test__mapping_parameters_mismatch__missing_positional_value():
    """ True is returned, even when captured args and kwargs will cause an
        exception in the future due to capturing fewer values than needed to
        fill a positional parameter of a view.
    """
    assert resolves_to_arguments("/bad3/2022/", ("2022",), {})


def test__mapping_parameters_mismatch__missing_key_value_pair():
    """ True is returned, even when captured args and kwargs will cause an
        exception in the future due to not capturing the key-value pair needed
        to fill a keyword parameter of a view.
    """
    assert resolves_to_arguments("/bad4/2022/", (), {"year": "2022"})


def test__mapping_parameters_mismatch__unused_positional_value():
    """ True is returned, even when captured args and kwargs will cause an
        exception in the future due to an additional positional value.
    """
    assert resolves_to_arguments("/bad5/2022/11/01/", ("2022", "11", "01"), {})


def test__mapping_parameters_mismatch__unused_keyword_value():
    """ True is returned, even when captured args and kwargs will cause an
        exception in the future due to an additional keyword value.
    """
    assert resolves_to_arguments(
        "/bad6/2022/11/01/", (), {"year": "2022", "month": "11", "day": "01"})
