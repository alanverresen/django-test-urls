#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.test import SimpleTestCase

from django_test_urls import resolves_to
from django_test_urls import resolves_to_view
from django_test_urls import resolves_to_404
from django_test_urls import resolves_to_args
from tests import app_views as views


class ArticlesUrlMappingTestCase(SimpleTestCase):
    """ Used to test the correct mapping of a URL to a view.
    """

    def test__match(self):
        """ Tests that URL pattern is mapped to correct view and arguments.
        """
        self.assertTrue(resolves_to_view("/articles/", views.articles))
        self.assertTrue(resolves_to_args("/articles/", {}))

    def test__match_alternative(self):
        """ Tests that URL pattern is mapped to correct view and arguments.
        """
        self.assertTrue(resolves_to("/articles/", views.articles, {}))


class MonthlyArchiveUrlMappingTestCase(SimpleTestCase):
    """ Used to test the correct mapping of a URL to a view.
    """

    def test__match(self):
        """ Tests that URL pattern is mapped to correct view and arguments.
        """
        self.assertTrue(
            resolves_to_view("/articles/2020/03", views.monthly_archive))
        self.assertTrue(
            resolves_to_args("/articles/2020/03", ("2020", "03")))

    def test__bad_year(self):
        """ Tests that URL mapping fails in case of bad value of year.
        """
        url = "/articles/99999/03"
        self.assertFalse(resolves_to_view(url, views.monthly_archive))
        self.assertTrue(resolves_to_404(url))

    def test__bad_month(self):
        """ Tests that URL mapping fails in case of bad value of month.
        """
        url = "/articles/2020/13"
        self.assertFalse(resolves_to_view(url, views.monthly_archive))
        self.assertTrue(resolves_to_404(url))


class CategoricalArchiveUrlMappingTestCase(SimpleTestCase):
    """ Used to test the correct mapping of a URL to a view.
    """

    def test__match(self):
        """ Tests that URL pattern is mapped to correct view.
        """
        self.assertTrue(
            resolves_to(
                "/articles/food",
                views.categorical_archive,
                {"category": "food"})
            )


class ArticleUrlMappingTestCase(SimpleTestCase):
    """ Used to test URL mapping for articles.
    """

    def test_URL_pattern_mapped_to_correct_view(self):
        """ Tests that URL pattern is mapped to correct view.
        """
        self.assertTrue(
            resolves_to_view("/articles/2020/03/hello", views.article))
        self.assertTrue(
            resolves_to_args("/articles/2020/03/hello", {"slug": "hello"}))
