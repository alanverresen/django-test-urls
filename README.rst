##############################################################################
django-test-urls 0.3.0
##############################################################################

.. image:: https://github.com/alanverresen/django-test-urls/actions/workflows/build.yml/badge.svg
    :target: https://github.com/alanverresen/django-test-urls/actions/workflows/build.yml
    :alt: Build Status

.. image:: https://github.com/alanverresen/django-test-urls/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/alanverresen/django-test-urls/actions/workflows/tests.yml
    :alt: Tests Status

.. image:: https://readthedocs.org/projects/django-test-urls/badge/?version=latest
    :target: https://django-test-urls.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

This small Python package defines a small set of functions that can be used
to test the mapping of URLs in a Django application:

* whether a URL is mapped correctly to a view
* whether a URL is not mapped to a view
* whether arguments are captured as expected
* detects mismatches between captured arguments and view's parameters


==============================================================================
Installation
==============================================================================

This package is available on the Python Package Index (PyPI), so you can
install this package using `pip`:

.. code-block:: sh

    $ python -m pip install django-test-urls


==============================================================================
Usage
==============================================================================

The fictional app that is being tested in this example contains a view that
lists every article that has been released in a given month. The following
URL pattern is used to map URLs to the aforementioned view, and captures two
values, `year` and `month`, to pass along.

.. code-block:: python

    # urls.py
    urlpatterns = [
        ...
        path('articles/<int:year>/<int:month>/', views.month_archive),
        ...
    ]


The following test verifies that an example URL is mapped correctly to the
correct view and that arguments are captured as expected.

.. code-block:: python

    # test_urls.py
    from django_test_urls import resolves_to
    from my_app import views


    def test_monthly_archive():
        assert resolves_to("articles/2022/11/", views.month_archive, (), {"year": 2022, "month": 11})

