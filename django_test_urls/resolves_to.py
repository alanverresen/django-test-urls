#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

""" Contains functionality to test the mapping of URLs to views and parameters.

:copyright: (c) 2022 by Alan Verresen
:license: MIT, see LICENSE for more details.
"""

# DEV NOTES
# ----------------------------------------------------------------------------
#
# Django's URL Dispatching Quirks
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# It is important to be aware of the following (seemingly arbitrary) aspects
# of URL dispatching in Django:
#
# - if unnamed regex groups are used in addition to named regex groups,
#   then the values captured by unnamed regex groups are dropped by Django
# - key-value pairs captured by named regex groups will be overwritten by
#   key-value pairs with the same key specified as extra arguments
# - extra arguments can be used in addition to unnamed regex groups, and in
#   this case only, both `args` and `kwargs` will have values
#
# For example, the following URL pattern contains two unnamed regex groups
# used for the year and the month, and one named regex group for the slug.
#
#   ^([0-9]{4})/(0[1-9]|1[0-2])/(?P<slug>[\w-]+)$
#
# The path `/2020/03/hello-world` would match the pattern above, but only
# "hello-world" for the keyword argument `slug` will be captured by Django.
#
#   found = resolve_url("/2020/03/hello-world")
#   found.args == ()
#   found.kwargs == {"slug": "hello-world"}
#
# For more information, check out the link below:
# https://docs.djangoproject.com/en/dev/topics/http/urls/#using-unnamed-regular-expression-groups

from inspect import isfunction
from inspect import signature

from django.urls import resolve as resolve_url
from django.urls.exceptions import Resolver404

from .exceptions import ArgumentParameterMismatch
from .exceptions import InvalidArgumentType


def resolves_to(url_path, expected_view, expected_args, expected_kwargs):
    """ Checks whether URL is resolved to the given view and arguments.

    This method preemptively checks for any mismatches between the given
    view's parameters and the given arguments. If there's a mismatch, then an
    exception will be raised to notify the test developer of this problem.

    Also, note that Django drops arguments captured by unnamed regex groups
    when using both named and unnamed regex groups in a URL pattern.

    :param str url_path: path of URL being mapped to a view and arguments
    :param function expected_view: expected view
    :param tuple|list expected_args: expected positional arguments
    :param dict expected_kwargs: expected keyword arguments
    :rtype: bool
    :return: Is the URL mapped to a view and arguments as expected?
    :raises InvalidArgumentType:
        passed an argument with an unexpected/invalid type
    :raises ArgumentParameterMismatch:
        mismatch between expected view's parameters and arguments
    """
    if not isinstance(url_path, str):
        raise InvalidArgumentType("url_path must be a str")
    if not isfunction(expected_view):
        raise InvalidArgumentType("expected_view must be a function")
    if not isinstance(expected_args, (tuple, list)):
        raise InvalidArgumentType("expected_args must be a tuple or list")
    if not isinstance(expected_kwargs, dict):
        raise InvalidArgumentType("expected_kwargs must be a dict")

    if isinstance(expected_args, list):
        expected_args = tuple(expected_args)

    check_for_mismatches(expected_view, expected_args, expected_kwargs)
    return \
        resolves_to_view(url_path, expected_view) and \
        resolves_to_arguments(url_path, expected_args, expected_kwargs)


def resolves_to_view(url_path, expected_view):
    """ Checks whether a URL is resolved to the expected view.

    :param str url_path: path of URL being mapped to a view
    :param function expected_view: expected view
    :rtype: bool
    :return: Is the URL mapped to a view as expected?
    """
    try:
        found = resolve_url(url_path)
    except Resolver404:
        return False

    return found.func == expected_view


def resolves_to_arguments(url_path, expected_args, expected_kwargs):
    """ Checks whether a URL is resolved to the expected arguments.

    :param str url_path: path of URL being mapped to arguments
    :param tuple expected_args: expected positional arguments
    :param dict expected_kwargs: expected keyword arguments
    :rtype: bool
    :return: Is the URL mapped to arguments as expected?
    """
    try:
        found = resolve_url(url_path)
    except Resolver404:
        return False

    return expected_args == found.args and expected_kwargs == found.kwargs


def check_for_mismatches(view, args, kwargs):
    """ Check for mismatches between arguments and the view's parameters.

    :param function view: expected view
    :param tuple args: positional arguments
    :param dict kwargs: keyword arguments
    :rtype: NoneType
    :return: N/A
    :raises ArgumentParameterMismatch:
        mismatch between captured arguments and the view's parameters
    """
    args = (None,) + args  # add stub for `request` parameter
    try:
        signature(view).bind(*args, **kwargs)
    except TypeError as e:
        msg = f"mismatch found: {view} <- {args}, {kwargs} - {e.args[0]}"
        raise ArgumentParameterMismatch(msg)


def resolves_to_404(url_path):
    """ Checks whether URL couldn't be mapped to a view, resulting in a 404.

    :param str url_path: path of URL
    :rtype: bool
    :return: Is URL resolved to a 404?
    :raises InvalidArgumentType:
        passed argument with an unexpected type
    """
    if not isinstance(url_path, str):
        raise InvalidArgumentType("url_path must be a str")

    try:
        _ = resolve_url(url_path)
        return False
    except Resolver404:
        return True
