===============================================================================
Changelog
===============================================================================

All notable changes to this project will be documented in this file.
The format is heavily based on
`Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to
`Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.


Types of Changes
----------------

- **PROJECT** for any changes to the project.
- **ADDED** for new features.
- **CHANGED** for changes in existing functionality.
- **DEPRECATED** for soon-to-be removed features.
- **REMOVED** for now removed features.
- **FIXED** for any bug fixes.
- **SECURITY** in case of vulnerabilities.


Unreleased
----------

The following changes are planned to happen in the future:

- Warn the user when trying to test a URL with both named and unnamed regex
  groups, and asserting that positional arguments are captured.
- Add support for class-based views.
- Add support for generic views.


Rejected
--------

The following features and/or changes have been rejected:

- Nothing has been rejected so far.


0.3.0 - 2022-12-10
------------------

ADDED
~~~~~
- Added functionality for reporting mismatches between captured arguments and
  a view's parameters.

CHANGED
~~~~~~~
- The functions `resolves_to_view` and `resolves_to_arguments` aren't part
  anymore of this package's public API; should only be used internally.


0.2.0 - 2022-12-04
------------------

PROJECT
~~~~~~~
- Added ReadTheDocs for hosting documentation.
- Added GitHub workflows for building and thoroughly testing package.

ADDED
~~~~~
- Added support for testing URL patterns with extra arguments.

CHANGED
~~~~~~~
- Added separate parameters for asserting values of both positional arguments
  and keyword arguments so that proper testing is possible.
- Renamed `resolves_to_args` to `resolves_to_arguments` to avoid any confusion
  with the name of the parameter for positional arguments, `args`.


0.1.1 - 2022-11-19
------------------

FIXED
~~~~~
- Fixed project URLs and license metadata.


0.1.0 - 2022-11-19
------------------

PROJECT
~~~~~~~
- Cleaned up project and created public git repository for project.

ADDED
~~~~~
- Added functionality to test mapping of URLs to specific views.
- Added functionality to test capturing of arguments using URL patterns.
- Added function combining both functions into one function.


0.0.0 - 2022-11-14
------------------

PROJECT
~~~~~~~
- It was decided to salvage this project from an older personal project.
