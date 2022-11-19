#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

""" Contains functionality to test the mapping of URLs to views and arguments.

:copyright: (c) 2022 by Alan Verresen.
:license: MIT, see LICENSE for more details.
"""

# DEV NOTE: CAPTURING VALUES WHEN USING BOTH NAMED AND UNNAMED REGEX GROUPS
# ----------------------------------------------------------------------------
# The official Django docs explicitly mention that when both named and
# unnamed/positional regex groups are used, the unnamed/positional arguments
# are not captured.
#
# For example, the following URL pattern contains two unnamed regex groups
# used for the year and the month, and one named regex group for the slug.
#
#   ^([0-9]{4})/(0[1-9]|1[0-2])/(?P<slug>[\w-]+)$
#
# The path `/2020/03/hello-world` would match the pattern above, but only the
# named value "hello-world" will be captured by Django.
#
#   found = resolve_url("/2020/03/hello-world")
#   found.args == ()
#   found.kwargs == {"slug": "hello-world"}
#
# So, Django only ever captures one type or the other. In order to help
# prevent developers from making a mistake due to this behavior, functions
# should only expose a single parameter for passing the expected arguments:
#
# - `dict` is used when testing the values captured by named groups
# - `list` or `tuple` is used when the values captured by unnamed groups
# - raise an exception when another data type is used to alert the developer
#
# There's a potential issue related to this approach that one needs to be wary
# of. If the developer passes an empty instance of the wrong data type, an
# incorrect implementation could accidentally return True if it blindly
# compares the values that weren't captured and the expected values. In more
# concrete terms, this comes down to the following situations:
#
# - URL pattern contains only named regex groups,
#   BUT developer passes an empty `list` or `tuple` instance
# - URL pattern contains only unnamed regex groups,
#   BUT developer passes an empty `dict` instance
#
# Therefore, False should be returned when Django captures the values of the
# named regex groups, but the test calls for checking against the values of
# the unnamed regex groups, or vice versa.
#
# For reference, check out the link below:
# https://docs.djangoproject.com/en/dev/topics/http/urls/#using-unnamed-regular-expression-groups

from django.urls import resolve as resolve_url
from django.urls.exceptions import Resolver404

from .exceptions import InvalidArgumentType


def resolves_to(url, expected_view, expected_args):
    """ Checks whether URL is resolved to the expected view and arguments.

    To distinguish between the use of named arguments and unnamed (or
    positional) arguments, a dictionary should be used when checking against
    named arguments and a list or tuple should be used when checking against
    unnamed arguments. Note that Django does not capture unnamed arguments
    when mixing named and unnamed arguments in a URL pattern.

    :param str url: URL being mapped to a view and arguments
    :param function expected_view: expected view
    :param tuple|list|dict expected_args: expected arguments
    :rtype: bool
    :return: Is the URL mapped to a view and arguments as expected?
    :raises InvalidArgumentType: arguments expressed using invalid type
    """
    return resolves_to_view(url, expected_view) and \
        resolves_to_args(url, expected_args)


def resolves_to_view(url, expected_view):
    """ Checks whether URL is resolved to the expected view.

    :param str url: URL being mapped to a view
    :param function expected_view: expected view
    :rtype: bool
    :return: Is the URL mapped to a view as expected?
    """
    try:
        found = resolve_url(url)
    except Resolver404:
        return False
    return found.func == expected_view


def resolves_to_args(url, expected_args):
    """ Checks whether URL is resolved to the expected arguments.

    To distinguish between the use of named arguments and unnamed (or
    positional) arguments, a dictionary should be used when checking against
    named arguments and a list or tuple should be used when checking against
    unnamed arguments. Note that Django does not capture unnamed arguments
    when mixing named and unnamed arguments in a URL pattern.

    :param str url: URL being mapped to arguments
    :param tuple|list|dict expected_args: expected arguments
    :rtype: bool
    :return: Is the URL mapped to arguments as expected?
    :raises InvalidArgumentType: arguments expressed using invalid type
    """
    if type(expected_args) not in {dict, tuple, list}:
        raise InvalidArgumentType()
    if type(expected_args) == list:
        expected_args = tuple(expected_args)

    try:
        found = resolve_url(url)
    except Resolver404:
        return False

    if len(found.args) == 0 and len(found.kwargs) == 0:
        return len(expected_args) == 0
    elif len(found.args) > 0 and type(expected_args) == tuple:
        return found.args == expected_args
    elif len(found.kwargs) > 0 and type(expected_args) == dict:
        return found.kwargs == expected_args
    else:
        return False  # tried to check against wrong arguments


def resolves_to_404(url):
    """ Checks whether URL couldn't be mapped to a view, resulting in a 404.

    :param str url: URL being mapped to a view and arguments
    :rtype: bool
    :return: Is URL resolved to a 404?
    """
    try:
        _ = resolve_url(url)
        return False
    except Resolver404:
        return True
