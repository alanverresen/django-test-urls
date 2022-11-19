#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Contains tests for the function `resolves_to_args()`.

# Test Design
# -----------
# There are several situations that one needs to consider, depending on
# the groups used in a URL pattern to capture arguments:
# - contains no groups to capture arguments
# - contains unnamed groups to capture unnamed arguments
# - contains named groups to capture named arguments
# - contains both named and unnamed group to capture arguments
#   (in this case, only named groups are captured, not unnamed groups!)
#
# For each situation, the following cases should be tested; not that
# multiple variants per case are possible:
# - values of captured groups match expected values (-> TRUE)
# - values of captured groups do not match expected values (-> FALSE)
# - checking named instead of unnamed groups, or vice versa (-> FALSE)
#
# Additional test cases are warranted for the following circumstances that
# one should be careful of:
# - if Django captured unnamed groups, but an empty `dict` was passed,
#   then an improper implementation might check the named groups that were
#   captured (none!) against the empty `dict` and incorrectly return True
#   instead of False
# - if Django captured named args, but an empty `list` or `tuple` was
#   passed, then an improper implementation might check the unnamed groups
#   that were captured (none!) against the empty `list` or `tuple` and
#   incorrectly return True instead of False
#
# Also, when a URL pattern contains both named and unnamed groups, it is
# important to keep in mind that the arguments of unnamed groups are never
# captured, and thus cannot be checked against. Thus, we need to test that
# uncaptured groups cannot be checked against.
#
# Also, when a URL doesn't match with a single URL pattern, there is no
# URL pattern to work off of. A test case needs to make sure that False
# is returned in this case.
#
# Last but not least, tests are also needed to cover the situation where
# an invalid data type (not `dict`, `tuple`, or `list`) is used to express
# the expected arguments.

from pytest import raises

from django_test_urls import resolves_to_args
from django_test_urls.exceptions import InvalidArgumentType


def test__resolves_to_args__url_with_no_args__match_tuple():
    """ Returns True when a URL without arguments is checked against an
        empty tuple.
    """
    assert resolves_to_args("/articles/", ())


def test__resolves_to_args__url_with_no_args__match_list():
    """ Returns True when a URL without arguments is checked against an
        empty list.
    """
    assert resolves_to_args("/articles/", [])


def test__resolves_to_args__url_with_no_args__match_dict():
    """ Returns True when a URL without arguments is checked against an
        empty dict.
    """
    assert resolves_to_args("/articles/", {})


def test__resolves_to_args__url_with_no_args__mismatch_tuple():
    """ Returns False when a URL without arguments is checked against a
        non-empty tuple.
    """
    assert not resolves_to_args("/articles/", ("nope",))


def test__resolves_to_args__url_with_no_args__mismatch_list():
    """ Returns False when a URL without arguments is checked against a
        non-empty list.
    """
    assert not resolves_to_args("/articles/", ["nope"])


def test__resolves_to_args__url_with_no_args__mismatch_dict():
    """ Returns False when a URL without arguments is checked against a
        dictionary with the right values.
    """
    assert not resolves_to_args("/articles/", {"a": "nope"})


# ----------------------------------------------------------------------------

def test__url_with_unnamed_args__match_tuple():
    """ Returns True when a URL with unnamed arguments is checked against
        a tuple with matching values.
    """
    assert resolves_to_args("/articles/2020/03", ("2020", "03"))


def test__url_with_unnamed_args__match_list():
    """ Returns True when a URL with unnamed arguments is checked against
        a list with matching values.
    """
    assert resolves_to_args("/articles/2020/03", ["2020", "03"])


def test__url_with_unnamed_args__mismatch_tuple():
    """ Returns False when a URL with unnamed arguments is checked against
        a tuple with non-matching values.
    """
    assert not resolves_to_args("/articles/2020/03", ("2020", "05"))


def test__url_with_unnamed_args__mismatch_list():
    """ Returns False when a URL with unnamed arguments is checked against
        a list with non-matching values.
    """
    assert not resolves_to_args("/articles/2020/03", ["2021", "03"])


def test__url_with_unnamed_args__mismatch_dict():
    """ Returns False when a URL with unnamed arguments is checked against
        the right values, but the wrong data type is used.
    """
    assert not resolves_to_args("/articles/2020/03", {0: "2020", 1: "03"})


def test__url_with_positional_args__mismatch_empty_dict():
    """ Returns False when a URL with unnamed arguments is checked against
        an empty dictionary.
    """
    assert not resolves_to_args("/articles/2020/03", {})


# ----------------------------------------------------------------------------

def test__url_with_named_args__match():
    """ Returns True when a URL with named arguments is checked against a
        dictionary with matching values.
    """
    assert resolves_to_args("/articles/food", {"category": "food"})


def test__url_with_named_args__mismatch_dict():
    """ Returns False when a URL with named arguments is checked against a
        dictionary with non-matching values.
    """
    assert not resolves_to_args("/articles/food", {"category": "movies"})


def test__url_with_named_args__mismatch_tuple():
    """ Returns False when a URL with named arguments is checked against a
        tuple with the right values.
    """
    assert not resolves_to_args("/articles/food", ("movies",))


def test__url_with_named_args__mismatch_list():
    """ Returns False when a URL with named arguments is checked against a
        list with the right values.
    """
    assert not resolves_to_args("/articles/food", ["movies"])


def test__url_with_named_args__mismatch_empty_tuple():
    """ Returns False when a URL with named arguments is checked against
        an empty tuple.
    """
    assert not resolves_to_args("/articles/food", ())


def test__url_with_named_args__mismatch_empty_list():
    """ Returns False when a URL with named arguments is checked against
        an empty tuple.
    """
    assert not resolves_to_args("/articles/food", [])


# ----------------------------------------------------------------------------

def test__url_with_both_args__match():
    """ Returns True when a URL with both named and unnamed arguments is
        checked against a dict with values matching named arguments.
    """
    assert resolves_to_args("/articles/2020/03/hello", {'slug': 'hello'})


def test__url_with_both_args__mismatch_dict():
    """ Returns False when a URL with both named and unnamed arguments is
        checked against a dict with values not matching named arguments.
    """
    assert not resolves_to_args("/articles/2020/03/hello", {'slug': 'bye'})


def test__url_with_mixed_args__mismatch_tuple():
    """ Returns False when a URL with both named and unnamed arguments is
        checked against a tuple with values matching unnamed arguments.
    """
    assert not resolves_to_args("/articles/2020/03/hello", ("hello",))


def test__url_with_mixed_args__mismatch_list():
    """ Returns False when a URL with both named and unnamed arguments is
        checked against a list with values matching unnamed arguments.
    """
    assert not resolves_to_args("/articles/2020/03/hello", ["hello"])


def test__url_with_mixed_args__mismatch_empty_tuple():
    """ Returns False when a URL with both named and unnamed arguments is
        checked against an empty tuple.
    """
    assert not resolves_to_args("/articles/2020/03/hello", ())


def test__url_with_mixed_args__mismatch_empty_list():
    """ Returns False when a URL with both named and unnamed arguments is
        checked against an empty list.
    """
    assert not resolves_to_args("/articles/2020/03/hello", [])


def test__url_with_mixed_args__checking_against_unnamed_tuple():
    """ Returns False when a URL with both named and unnamed arguments is
        checked against a tuple of values of unnamed groups.
    """
    assert not resolves_to_args("/articles/2020/03/hello", ("2020", "03"))


def test__url_with_mixed_args__checking_against_unnamed_list():
    """ Returns False when a URL with both named and unnamed arguments is
        checked against a list of values of unnamed groups.
    """
    assert not resolves_to_args("/articles/2020/03/hello", ["2020", "03"])


# ----------------------------------------------------------------------------

def test__url_does_not_match_any_pattern():
    """ Returns False when a URL does not match any URL pattern.
    """
    assert not resolves_to_args("/this/url/does/not/match/any/pattern", [])


# ----------------------------------------------------------------------------

def test__invalid_argument_type():
    """ Exception is raised when no matching view is found for URL.
    """
    with raises(InvalidArgumentType):
        assert not resolves_to_args("/articles/2020/03", {"2020", "03"})
