..
    This file is part of autosemver.
    Copyright (C) 2016 David Caro.

    autosemver is free software; you can redistribute it
    and/or modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation; either version 2 of the
    License, or (at your option) any later version.

    autosemver is distributed in the hope that it will be
    useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with autosemver; if not, write to the
    Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
    MA 02111-1307, USA.


Usage
=====

To use the automatic semantic versioning scheme, you just have to add some
extra keywords to your `setup.py` file, in the call to the `distutils.setup`,
and add `autosemver` to the `setup_requires` and `install_requires` entries::

   setup(
       name='some-package',
       url='http://my.fancy/shrubbery',
       ...
       install_requires=['some_important_dep', 'autosemver'],
       ...
       setup_requires=['autosemver'],
       ...
       autosemver=True
   )


There is an optional key to specify the url of your bug tracker, currently only
github and bugzilla bug specifications are supported, the key is
`bugtracker_url` and you can use it like::

   setup(
       ...
       bugtracker_url='https://github.com/david-caro/python-autosemver/issues/'
       ...
   )


.. automodule:: autosemver
