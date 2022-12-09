#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Contains tests for the function `resolves_to_404()`.

# Test Design
# -----------
# Whether the function `resolves_to_404()` returns True or False depends
# solely on whether the URL can be mapped to an existing view or not. As such,
# only two tests are needed to cover these cases.

import pytest

from django_test_urls.resolves_to import resolves_to_404
from django_test_urls.exceptions import InvalidArgumentType


def test__resolves_to_404__invalid_argument_type__url_path():
    """ Raises an exception when the URL isn't expressed as a `str`.
    """
    with pytest.raises(InvalidArgumentType):
        resolves_to_404(None)


def test__resolves_to_404__no_match_with_view():
    """ Returns True when URL cannot be mapped to a view.
    """
    assert resolves_to_404("/not/a/url")


def test__resolves_to_404__match_with_view():
    """ Returns False when URL can be mapped to a view.
    """
    assert not resolves_to_404("/url1/")
