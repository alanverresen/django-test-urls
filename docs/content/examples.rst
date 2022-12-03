===============================================================================
Examples
===============================================================================

.. note::
    The examples in this document use the `pytest` package, but
    `django-test-urls` can be used with any test framework. Also, obvious
    imports are omitted from examples for the sake of brevity.


-------------------------------------------------------------------------------
A Common Example
-------------------------------------------------------------------------------

We will test the URL mapping of a fictional app with a view that lists all
articles for a given month. The following URL pattern captures two keyword
arguments, `year` and `month`, which will be passed on to the aforementioned
view as arguments for the respective parameters.

.. code-block:: python

    # urls.py
    urlpatterns = [
        ...
        path('articles/<str:year>/<str:month>/', views.month_archive),
        ...
    ]


In order to test that a URL is mapped to the correct view and that arguments
are captured as expected, this package provides the functions
`resolves_to_view` and `resolves_to_arguments`.

.. code-block:: python

    # test_urls.py
    from django_test_urls import resolves_to_view
    from django_test_urls import resolves_to_arguments


    def test_monthly_archive():
        assert resolves_to_view("articles/2022/11/", views.month_archive)
        assert resolves_to_arguments("articles/2022/11", (), {"year": "2022", "month": "11"})


The function `resolves_to_view` is used to assert which view the URL is mapped
to, and the function `resolves_to_arguments` is used to assert which
positional and keyword arguments are extracted from the URL:

- the first argument has to be a `tuple` or `list` used to assert which
  positional arguments are captured by Django using unnamed regex groups
- the second argument has to be a `dict` used to assert which keyword
  arguments are captured by Django using named regex groups, and/or added as
  extra arguments

.. note::
    When a URL pattern contains both named and unnamed regex groups, then
    Django drops the values captured by unnamed regex groups! As a result,
    one of the following is usually true, while the other one isn't:

    - no positional arguments are captured (first argument is empty)
    - no keyword arguments are captured (second argument is empty)

    However, when a URL pattern contains only unnamed regex groups, and extra
    arguments are provided, the positional arguments are not dropped by Django.
    This is the only case where both collections aren't empty.


These two assertions are often used together, so the package also provides
the function `resolves_to` which combines these two calls. The only downside
of this function is that one receives less specific feedback about whether the
URL was mapped to the wrong view or the wrong arguments.

.. code-block:: python

    # test_urls.py
    from django_test_urls import resolves_to


    def test_monthly_archive():
        assert resolves_to("articles/2022/11/", views.month_archive, (), {"year": 2022, "month": 11})


-------------------------------------------------------------------------------
Improving the Previous Example
-------------------------------------------------------------------------------

The URL pattern of the previous example would match nonsensical URLs. For
example, there is no 13th month, so we can rewrite the previous URL pattern
by using named regex groups.

.. code-block:: python

    # urls.py
    urlpatterns = [
        ...
        re_path(route=r'^articles/(?P<year>[0-9]{4})/(?P<month>0[1-9]|1[0-2])/$', view=views.month_archive),
        ...
    ]


We have now improved the URL pattern, which still passes our old test. We can
also add a test to verify that our URL pattern only matches URLs for which
the value of the month is "01", "12", or in between.

.. code-block:: python

    # test_urls.py
    from django_test_urls import resolves_to_view


    def test_monthly_archive__month_range():
        assert not resolves_to_view("articles/2022/00/", views.month_archive)
        assert resolves_to_view("articles/2022/01/", views.month_archive)
        assert resolves_to_view("articles/2022/12/", views.month_archive)
        assert not resolves_to_view("articles/2022/13/", views.month_archive)


The first and last assertions check that the URL is not mapped to a specific
view, but do not account for the possibility that the URL is mapped to
different view. That's why the package also provides the function
`resolves_to_404`, because Django serves a 404 error page when a URL cannot be
mapped to a view.

.. code-block:: python

    # test_urls.py
    from django_test_urls import resolves_to_404
    from django_test_urls import resolves_to_view


    def test_monthly_archive__month_range():
        assert resolves_to_404("articles/2022/00/")
        assert resolves_to_view("articles/2022/01/", views.month_archive)
        assert resolves_to_view("articles/2022/12/", views.month_archive)
        assert resolves_to_404("articles/2022/13/")


-------------------------------------------------------------------------------
URL Patterns without Regex Groups
-------------------------------------------------------------------------------

It's not uncommon to have URL patterns that do not capture any values. In this
case, an empty `tuple` or `list`, and an empty `dict` are used to assert that
no arguments are captured.

.. code-block:: python

    # urls.py
    urlpatterns = [
        ...
        path('articles/', views.all_archive),
        ...
    ]


    # test_urls.py
    from django_test_urls import resolves_to


    def test_all_archive():
        assert resolves_to("articles/", views.all_archive, (), {})


-------------------------------------------------------------------------------
URL Patterns with Unnamed Regex Groups
-------------------------------------------------------------------------------

A URL pattern might also contain unnamed regex groups. Let's take the URL
pattern with named regex groups from a previous example, and remove the names.
Captured arguments will now be passed on to the view as positional arguments.

.. code-block:: python

    # urls.py
    urlpatterns = [
        ...
        re_path(route=r'^articles/([0-9]{4})/(0[1-9]|1[0-2])/$', view=views.month_archive),
        ...
    ]


    # test_urls.py
    from django_test_urls import resolves_to


    def test_monthly_archive():
        assert resolves_to("articles/2022/11/", views.month_archive, ("2022" , "11"), {})
        assert resolves_to("articles/2022/11/", views.month_archive, ["2022" , "11"], {})  # equivalent


-------------------------------------------------------------------------------
URL Patterns with Named and Unnamed Regex Groups
-------------------------------------------------------------------------------

When you use both named and unnamed regex groups in a URL pattern, Django will
drop the values captured by unnamed regex groups. As a result, an empty tuple
or list instance must be passed as the argument of the `args` parameter in
this case.

.. code-block:: python

    # urls.py
    urlpatterns = [
        ...
        re_path(r'^articles/([0-9]{4})/([0-9]{2})/(?P<slug>[\w-]+)/$', views.article_detail),
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
URL Patterns with Extra Arguments
-------------------------------------------------------------------------------

When extra arguments are added to a URL pattern using the optional `kwargs`
parameter, Django will treat these as keyword arguments.

.. code-block:: python

    # urls.py
    urlpatterns = [
        ...
        re_path(r'^articles/current-year/(?P<month>0[1-9]|1[0-2])/$', views.article_detail, kwargs={"year": "2022"}),
        ...
    ]


    # test_urls.py
    from django_test_urls import resolves_to


    def test_monthly_archive__current_year():
        assert resolves_to("articles/current-year/11/", views.article_detail, (), {"year": "2022", "month": "11"})


It is important to note that if extra arguments are used with URL patterns
that contain unnamed regex groups, but no named regex groups, then the
positional arguments captured by those unnamed regex groups are not dropped.

.. code-block:: python

    # urls.py
    urlpatterns = [
        ...

        # BAD: positional and keyword arguments will both be mapped to "year" parameter of view
        re_path(r'^articles/current-year/(0[1-9]|1[0-2])/$', views.article_detail, kwargs={"year": "2022"}),

        # OKAY: positional arg mapped to `year` parameter, keyword arg mapped to `month` parameter of view
        re_path(r'^articles/[0-9]{4}/current-month/$', views.article_detail, kwargs={"month": "11"}),
        ...
    ]


However, this situation requires you to be careful so that positional
arguments and keyword arguments do not try to set the value of the same
parameter. If the view has two parameters `year` and `month`, in that order,
then the

.. code-block:: python

    # test_urls.py
    from django_test_urls import resolves_to

    def test_monthly_archive__current_month():
        # this is correct, but will raise an exception when arguments are passed to view
        assert resolves_to("articles/current-year/11/", views.article_detail, ("11",), {"year": "2022"})

    def test_monthly_archive__current_year():
        # this is correct, and won't lead to problems
        assert resolves_to("articles/2022/current-month/", views.article_detail, ("2022",), {"month": "11"})


-------------------------------------------------------------------------------
Mismatches Between URL Patterns and Views
-------------------------------------------------------------------------------

**Will be added in the future.**

As you can see, there's plenty of room to mess up when creating URL patterns
and mapping URLs to views. This package will help you prevent such mistakes by
also reporting such argument mismatches:

- missing positional arguments
- missing keyword arguments
- ...
