#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Contains tests for the function `check_for_mismatches()`.

import pytest

from django_test_urls.exceptions import ArgumentParameterMismatch
from django_test_urls.resolves_to import check_for_mismatches


def test__function_view():
    """ No exception is raised when there is no mismatch between the captured
        arguments and the view's parameters.
    """
    def view(request, a, b):
        pass

    check_for_mismatches(view, (), {"a": "1", "b": "2"})
    check_for_mismatches(view, ("1",), {"b": "2"})
    check_for_mismatches(view, ("1", "2",), {})


def test__missing_positional_argument():
    """ Raises an exception when there's a mismatch between the captured
        arguments and the view's parameters: not enough positional arguments.
    """
    def view(request, a, b):
        pass

    with pytest.raises(ArgumentParameterMismatch) as e:
        check_for_mismatches(view, ("1",), {})
    assert "missing a required argument: 'b'" in str(e)


def test__unexpected_positional_argument():
    """ Raises an exception when there's a mismatch between the captured
        arguments and the view's parameters: too many positional arguments.
    """
    def view(request, a, b):
        pass

    with pytest.raises(ArgumentParameterMismatch) as e:
        check_for_mismatches(view, ("1", "2", "3"), {})
    assert "too many positional arguments" in str(e)


def test__missing_keyword_argument():
    """ Raises an exception when there's a mismatch between the captured
        arguments and the view's parameters: missing keyword argument.
    """
    def view(request, a, b):
        pass

    with pytest.raises(ArgumentParameterMismatch) as e:
        check_for_mismatches(view, (), {"a": 1})
    assert "missing a required argument: 'b'" in str(e)


def test__unexpected_keyword_argument():
    """ Raises an exception when there's a mismatch between the captured
        arguments and the view's parameters: unexpected keyword argument.
    """
    def view(request, a, b):
        pass

    with pytest.raises(ArgumentParameterMismatch) as e:
        check_for_mismatches(view, (), {"a": 1, "b": 2, "c": 3})
    assert "got an unexpected keyword argument 'c'" in str(e)


def test__multiple_args_mapped_to_parameter():
    """ Raises an exception when there's a mismatch between the captured
        arguments and the view's parameters: args mapped to same parameter.
    """
    def view(request, a, b):
        pass

    with pytest.raises(ArgumentParameterMismatch) as e:
        check_for_mismatches(view, ("1", "2"), {"a": "3"})
    assert "multiple values for argument 'a'" in str(e)
