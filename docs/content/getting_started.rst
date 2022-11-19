===============================================================================
Installation
===============================================================================

.. note::
    Some OS distributions will use the command `python3` instead of `python`.
    Similarly, if you want to run the `pip` command instead of `python -m pip`,
    then you might have to use `pip3` instead.


.. note::
    It's recommended that you use a `virtual environment`_. If you are not
    using a virtual environment, you should use the `\-\-user` switch when
    installing the package using `pip`.


-------------------------------------------------------------------------------
Python Package Index (PyPI)
-------------------------------------------------------------------------------

This package is available on the Python Package Index (PyPI). You can install
this package using `pip` by running the following command in a terminal:

.. code-block:: sh

    $ python -m pip install django-test-urls


-------------------------------------------------------------------------------
Source Code
-------------------------------------------------------------------------------

You can also install this package using a copy of the source code:

.. code-block:: sh

    $ git clone git://github.com/alanverresen/django-test-urls.git
    $ cd django-test-urls
    $ python -m pip install .


-------------------------------------------------------------------------------
Confirmation
-------------------------------------------------------------------------------

To check whether the package was installed correctly, you can run the
following command. If successful, the current version of the package will be
printed.

.. code-block:: sh

    $ python -c "import django_test_urls as m; print(m.VERSION)"



.. _virtual environment: https://docs.python.org/3/tutorial/venv.html