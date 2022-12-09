===============================================================================
Examples
===============================================================================

.. note::
    The examples in this document use the `pytest` package, but
    `django-test-urls` can be used with any test framework. Also, obvious
    imports are omitted from examples for the sake of clarity.


-------------------------------------------------------------------------------
Using `resolves_to`
-------------------------------------------------------------------------------

In this example, we will test the mapping of URLs for a view that displays a
list of all articles that were published in a given month. The URL pattern
captures two keyword arguments, `year` and `month`, which will be passed on to
the view by Django, in addition to the `request` parameter.

.. code-block:: python

    # views.py
    def monthly_archive(request, year, month):
        # do stuff
        return response


    # urls.py
    urlpatterns = [
        ...
        path("articles/<int:year>/<int:month>/", views.monthly_archive),
        ...
    ]


In order to test that a URL is mapped to the correct view and that the correct
arguments are captured, this package provides the function `resolves_to`. This
function takes the path of a URL as its first argument, followed by the view
that the URL should be mapped to, and the positional and keyword arguments
that one expects to be captured by Django.

.. code-block:: python

    # test_urls.py
    from django_test_urls import resolves_to


    def test_monthly_archive():
        assert resolves_to("/articles/2022/11/", views.monthly_archive, (), {"year": 2022, "month": 11})


When expressing the values of the positional arguments captured by unnamed
regex groups, a `tuple` or `list` must be used. Likewise, a `dict` has to be
used to express the keyword arguments captured by named regex groups, and/or
added as extra arguments.

.. note::
    When a URL pattern contains both named and unnamed regex groups, Django
    drops the values captured by unnamed regex groups! As a result, the
    `tuple` (or `list`) of positional arguments is typically empty if one
    expects that any keyword arguments are captured.

    However, when a URL pattern contains unnamed regex groups, but no named
    regex groups, the positional arguments are not dropped, even if extra
    keyword arguments are provided. This is the only case where both
    positional arguments and keyword arguments are passed on to the view.


-------------------------------------------------------------------------------
Using `resolves_to_404`
-------------------------------------------------------------------------------

The URL pattern of the previous example would match with some nonsensical
URLs, allowing for cases like the year zero, or the zeroth/thirteenth month.
So, let's rewrite that URL pattern so that it only accepts values "01" to "12"
as the value of the month.

.. code-block:: python

    # urls.py
    urlpatterns = [
        ...
        re_path(route=r"^articles/(?P<year>[0-9]{4})/(?P<month>0[1-9]|1[0-2])/$", view=views.monthly_archive),
        ...
    ]


When writing tests for these new restrictions, we could use `resolves_to` in
order to assert that a URL isn't mapped to a view, but then we would run into
two problems:

- which arguments do we need to specify?
- what if the URL accidentally matches another view?

In order to avoid these issues, this package also provides the function
`resolves_to_404` for asserting that a URL isn't mapped to any view. It is
named as such, because Django serves a 404 error page when a URL does not
match any URL pattern.

.. code-block:: python

    # test_urls.py
    from django_test_urls import resolves_to
    from django_test_urls import resolves_to_404


    def test_monthly_archive():
        assert resolves_to("/articles/2022/11/", views.monthly_archive, (), {"year": "2022", "month": "11"})


    def test_monthly_archive__month_range():
        assert resolves_to_404("/articles/2022/00/")
        assert resolves_to("/articles/2022/01/", views.monthly_archive, (), {"year": "2022", "month": "01"})
        assert resolves_to("/articles/2022/12/", views.monthly_archive, (), {"year": "2022", "month": "12"})
        assert resolves_to_404("/articles/2022/13/")


-------------------------------------------------------------------------------
No Arguments
-------------------------------------------------------------------------------

It's not uncommon to have URL patterns that do not capture any values. In this
case, an empty `tuple` or `list`, and an empty `dict` must be used to
express that no arguments are captured.

.. code-block:: python

    # urls.py
    urlpatterns = [
        ...
        path("articles/", views.all_archive),
        ...
    ]


    # test_urls.py
    from django_test_urls import resolves_to


    def test_all_archive():
        assert resolves_to("articles/", views.all_archive, (), {})


-------------------------------------------------------------------------------
Positional Arguments
-------------------------------------------------------------------------------

A URL pattern can use unnamed regex groups to capture positional arguments.
Let's take the URL pattern with named regex groups from a previous example,
and remove the names. Captured arguments will now be passed on to the view as
positional arguments.

.. code-block:: python

    # urls.py
    urlpatterns = [
        ...
        re_path(route=r"^articles/([0-9]{4})/(0[1-9]|1[0-2])/$", view=views.monthly_archive),
        ...
    ]


    # test_urls.py
    from django_test_urls import resolves_to


    def test_monthly_archive():
        assert resolves_to("articles/2022/11/", views.monthly_archive, ("2022" , "11"), {})
        assert resolves_to("articles/2022/11/", views.monthly_archive, ["2022" , "11"], {})  # equivalent


.. note::
    A lot of the issues described in this document can be avoided by not using
    unnamed regex groups. Use unnamed regex groups with caution, and give
    preference to named regex groups.


-------------------------------------------------------------------------------
Extra Arguments
-------------------------------------------------------------------------------

When extra arguments are specified using the optional `kwargs` parameter,
Django will add these to the collection of keyword arguments captured by named
regex groups. Extra keyword arguments will overwrite captured keyword
arguments with the same key.

.. code-block:: python

    # urls.py
    urlpatterns = [
        ...
        re_path(r"^articles/current-year/(?P<month>0[1-9]|1[0-2])/$", views.monthly_archive, kwargs={"year": "2022"}),
        ...
    ]


    # test_urls.py
    from django_test_urls import resolves_to


    def test_monthly_archive__current_year():
        assert resolves_to("articles/current-year/11/", views.monthly_archive, (), {"year": "2022", "month": "11"})


-------------------------------------------------------------------------------
Positional and Keyword Arguments
-------------------------------------------------------------------------------

When you use both named and unnamed regex groups in a URL pattern, Django will
drop the positional arguments captured by unnamed regex groups. Therefore, the
tuple (or list) of positional arguments must be empty.

.. code-block:: python

    # urls.py
    urlpatterns = [
        ...
        re_path(r"^articles/([0-9]{4})/([0-9]{2})/(?P<slug>[\w-]+)/$", views.article_detail),
        ...
    ]


    # test_urls.py
    from django_test_urls import resolves_to


    def test_article_detail():
        assert resolves_to("articles/2022/11/hello-world/", views.article_detail, (), {"slug": "hello-world"})


.. note::
    Check the `documentation`_ for more information about named and unnamed regex groups.

.. _documentation: https://docs.djangoproject.com/en/dev/topics/http/urls/#using-unnamed-regular-expression-groups


-------------------------------------------------------------------------------
Positional and Extra Arguments
-------------------------------------------------------------------------------

It is important to point out that values captured by unnamed regex groups will
not be dropped by Django if the URL pattern does not contain any named regex
groups, even if extra arguments are provided. This can result into various
issues when mapping arguments to a view's parameters.

.. code-block:: python

    # urls.py
    urlpatterns = [
        ...

        # BAD, multiple arguments mapped to same parameter
        # - one positional argument is captured, which will be mapped to the first parameter, `year`
        # - one extra keyword argument, which will be mapped to the parameter `year`
        re_path(r"^articles/current-year/(0[1-9]|1[0-2])/$", views.monthly_archive, kwargs={"year": "2022"}),

        # OKAY
        # - one positional argument is captured, which will be mapped to the first parameter, `year`
        # - one extra keyword argument, which will be mapped to the parameter `month`
        re_path(r"^articles/[0-9]{4}/current-month/$", views.monthly_archive, kwargs={"month": "11"}),

        ...
    ]


If we would use these URL patterns, then the behavior described by the
following tests can be expected. The exception raised by the first test is
primarily meant to inform the person writing tests about there being a
mismatch between the captured arguments and the view's parameters, and
normally shouldn't be asserted.

.. code-block:: python

    # test_urls.py
    from django_test_urls import resolves_to
    from django_test_urls.exceptions import ArgumentParameterMismatch

    def test_monthly_archive__current_month():
        with pytest.raises(ArgumentParameterMismatch):  # multiple arguments mapped to same parameter!
            assert resolves_to("articles/current-year/11/", views.monthly_archive, ("11",), {"year": "2022"})

    def test_monthly_archive__current_year():
        # this won't result any problems, but you should avoid this
        assert resolves_to("articles/2022/current-month/", views.monthly_archive, ("2022",), {"month": "11"})


-------------------------------------------------------------------------------
Argument/Parameter Mismatches
-------------------------------------------------------------------------------

There's plenty of room to mess up when creating URL patterns and mapping URLs
to views. This package helps to prevent such mistakes by preemptively checking
for any mismatches between a view's parameters and the captured arguments, and
raising an exception if there's a problem:

- missing/unexpected positional arguments
- missing/unexpected keyword arguments
- multiple arguments mapped to the same parameter
- etc.
