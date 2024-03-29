.. image:: https://travis-ci.org/david-caro/python-autosemver.svg?branch=master
   :alt: Latest commit build status
   :target: https://travis-ci.org/david-caro/python-autosemver

.. image:: https://readthedocs.org/projects/autosemver/badge/?version=latest
   :alt: Documentation
   :target: https://autosemver.readthedocs.io

.. image:: https://img.shields.io/github/license/david-caro/python-autosemver?color=blue
   :alt: License
   :target: https://github.com/david-caro/python-autosemver/blob/master/LICENSE

.. image:: https://badge.fury.io/py/autosemver.svg
   :alt: Latest PyPI - Version
   :target: https://badge.fury.io/py/autosemver

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :alt: Code style
   :target: https://github.com/ambv/black

.. image:: https://img.shields.io/pypi/dm/autosemver
   :alt: PyPI - Downloads

===========
Autosemver
===========

This small module provides an easy way to automatically manage the version of
your python modules by extracting information directly from the version control
system (currently only git supported, patches welcome).

Once installed (ex. ``pip install autosemver``), adding a single line in your
``setup.py`` file is enough to start using it::

    setup(
        name='some-package',
        url='http://my.fancy/shrubbery',
        ...
        install_requires=['some_important_dep', 'autosemver'],
        ...
        setup_requires=['autosemver'],
        ...
        autosemver=True,
    )

That will use tags, commit messages (searches for lines like ``Sem-Ver: ...``
and ``* Incompatible``) to generate a version compatible with the semantic
versioning standard (https://semver.org/).

Read the full documentation here: http://autosemver.readthedocs.io

