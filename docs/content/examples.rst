===============================================================================
Examples
===============================================================================

.. note::
    The examples in this document use the `pytest` package,
    but `django-test-urls` can be used with any test framework.
    Also, obvious imports are omitted from examples.


-------------------------------------------------------------------------------
A Common Example
-------------------------------------------------------------------------------

We will test the URL mapping of a fictional app with a view that lists all
articles for a given year and month. The following URL pattern captures two
values, `year` and `month`, which are passed on to the view by Django.

.. code-block:: python

    # urls.py
    urlpatterns = [
        ...
        path('articles/<int:year>/<int:month>/', views.month_archive),
        ...
    ]


In order to test that an example URL is mapped correctly to the right view and
that the arguments are captured as expected, this package provides the
functions `resolves_to_view` and `resolves_to_args`.

.. code-block:: python

    # test_urls.py
    from django_test_urls import resolves_to_view
    from django_test_urls import resolves_to_args


    def test_monthly_archive():
        assert resolves_to_view("articles/2022/11/", views.month_archive)
        assert resolves_to_args("articles/2022/11", {"year": 2022, "month": 11})


These two assertions are often used together, so the package also provides
the function `resolves_to` which combines these two calls.

.. code-block:: python

    # test_urls.py
    from django_test_urls import resolves_to


    def test_monthly_archive():
        assert resolves_to("articles/2022/11/", views.month_archive, {"year": 2022, "month": 11})


-------------------------------------------------------------------------------
Improving the Previous Example
-------------------------------------------------------------------------------

The URL pattern of the previous example would match nonsensical URLs. For
example, there is no 13th month, so in order to fix this problem, we rewrite
the previous URL pattern by using named regex groups.

.. code-block:: python

    # urls.py
    urlpatterns = [
        ...
        re_path(route=r'^articles/(?P<year>[0-9]{4})/(?P<month>0[1-9]|1[0-2])/$', view=views.month_archive),
        ...
    ]


We now add a test to verify that our URL pattern only matches URLs for which
the value of the month is "01", "12", or in between.

.. code-block:: python

    # test_urls.py
    from django_test_urls import resolves_to_view


    def test_monthly_archive__month_range():
        assert not resolves_to_view("articles/2022/00/", views.month_archive)
        assert resolves_to_view("articles/2022/01/", views.month_archive)
        assert resolves_to_view("articles/2022/12/", views.month_archive)
        assert not resolves_to_view("articles/2022/13/", views.month_archive)


However, these assertions do not account for the possibility that these URLs
are mapped to a different view. That's why the package also provides the
function `resolves_to_404`, because Django serves a 404 error page when a URL
cannot be mapped to a view.

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
URL Patterns without Captured Values
-------------------------------------------------------------------------------

It's not uncommon to have URL patterns that do not capture any values.

.. code-block:: python

    # urls.py
    urlpatterns = [
        ...
        path('articles/', views.all_archive),
        ...
    ]

In this case, an empty instance of a `tuple`, `list` or `dict` can be used to
specify that no values are captured. All of the statements shown below are
okay.

.. code-block:: python

    # test_urls.py
    from django_test_urls import resolves_to


    def test_all_archive():
        assert resolves_to("articles/", views.all_archive, [])
        assert resolves_to("articles/", views.all_archive, ())  # equivalent
        assert resolves_to("articles/", views.all_archive, {})  # equivalent


-------------------------------------------------------------------------------
URL Patterns with Unnamed Regex Groups
-------------------------------------------------------------------------------

A URL pattern might also contain unnamed URL regex groups. Let's take the URL
pattern with named regex groups from a previous example, and remove the names.
Captured arguments will now be passed on to the view as positional arguments.

.. code-block:: python

    # urls.py
    urlpatterns = [
        ...
        re_path(route=r'^articles/([0-9]{4})/(0[1-9]|1[0-2])/$', view=views.month_archive),
        ...
    ]


In order to test that the arguments are captured correctly, we now need to use
a `tuple` or `list` instance instead of a `dict` instance. Both of the statements
shown below are okay.

.. code-block:: python

    # test_urls.py
    from django_test_urls import resolves_to


    def test_monthly_archive():
        assert resolves_to("articles/2022/11/", views.month_archive, ("2022" , "11"))
        assert resolves_to("articles/2022/11/", views.month_archive, ["2022" , "11"])  # equivalent


-------------------------------------------------------------------------------
URL Patterns with Named and Unnamed Regex Groups
-------------------------------------------------------------------------------

When you use both named and unnamed regex groups in a URL pattern, Django will
only pass on the values captured by named regex groups to the view. As a
result, you can/should only verify the values captured by named regex groups.

.. code-block:: python

    # urls.py
    urlpatterns = [
        ...
        re_path(r'^articles/([0-9]{4})/([0-9]{2})/(?P<slug>[\w-]+)/$', views.article_detail),
        ...
    ]

In this case, we expect that only the value of the named regex group `slug`
will be captured, so our test would look something like the following.

.. code-block:: python

    # test_urls.py
    from django_test_urls import resolves_to


    def test_article_detail():
        assert resolves_to("articles/2022/11/hello-world/", views.article_detail, {"slug": "hello-world"})

.. note::
    Check the `documentation`_ for more information about named and unnamed regex groups.

.. _documentation: https://docs.djangoproject.com/en/dev/topics/http/urls/#using-unnamed-regular-expression-groups