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

Changes needed to the code
--------------------------

To use the automatic semantic versioning scheme, you just have to add some
extra keywords to your `setup.py` file, in the call to the `setuptools.setup`,
and add `autosemver` to the `setup_requires` and `install_requires` entries::

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


**NOTE**: using the old `distutils` module directly might not work due to the
plugin loading, you should try to use the newer (and recomended) `setuptools`.


You can change the default behavior for autosemver, for example, you can define
a bugtracker url to add a link on all the bugs specified in the commit messages
and point them out on the changelog. To pass parameters to autosemver, you can
use a dictionary as the value to the autosemver::

   setup(
        ...
        autosemver={
           'bugtracker_url'='https://github.com/david-caro/python-autosemver/issues/'
        },
        ...
   )

To see a full list of parameters you can check the docs for the function
:mod:`autosemver.distutils_autosemver_case`.


If you use a version module pattern
+++++++++++++++++++++++++++++++++++
It's common on some python packages to have a '__version__' property at the
root of the module to indicate the package version, in that case, you can use
the following call::

    import autosemver

    __version__ = autosemver.packaging.get_current_version(
        project_name='myprojectname'
    )

The parameter 'project_name' is required to avoid import loops and to allow
correct version detection.


Declaring the type of change a commit introduces
------------------------------------------------


Major change
++++++++++++
Once you have the dependency declared on your code, you can start marking your
commits to bump one of the three version numbers as sem-ver defines, major,
feature and minor.

In order to tag a commit as a major change, you can do one of:

* Add a line starting with 'Sem-Ver: api-breaking change' to the commit message
  (similar to the Signed-off header, actually the message after the ':' just
  needs to have 'break' on it for this to work).
* Add a line starting with '* INCOMPATIBLE'.

That will make the version bump the major version number, for example::

    My fancy commit message

    * INCOMPATIBLE: this breaks the backwards compatibility somehow.
      (closes #567)

Or::

    My fancy commit message

    This breaks the backwards compatibility somehow. (addresses #456)

    Sem-Ver: api-breaking

For a package that has the version 1.2.3, will bump it to 2.0.0

Feature change
++++++++++++++
Similar as with the major version number, you can also specify that a change
has to bump the feature number (that is the 2 in 1.2.3), to do so:

* Add a line starting with 'Sem-Ver: new feature' to the commit message.
* Add a line starting with '* NEW'.

For example::

    My fancy commit message

    * NEW: adds some exciting new feature. (closes #345)

Or::

    My fancy commit message

    Adds some exciting new feature (fixes #234)

    Sem-Ver: new feature

For a package with the version 1.2.3, will bump it to 1.3.0

Bug change
++++++++++
As before, you can specify that a change only bumps the bug version of your
package, though if you don't tag you commit on any of the previous ways, they
will be considered bug changes by default.
To explicitly tag a commit as a bug change, do one of:

* Add a line starting with 'Sem-Ver: bugfix' to the commit message.

Remember that this is the default case if you don't specify the commit being a
major or feature change. Examples of this type of commits are::

    My fancy commit message

    * BUGFIX: the message here does not really matter, as long as it does not
      start with the feature or major strings. (addresses #123)

Or::

    My fancy commit message

    This fixes some strange bug (closes #123)

    Sem-Ver: bugfix


Details on merge commits
------------------------

If you are using merge commits to integrate your feature branches on your main
one, the version for the main one will only be bumped according to the most
relevant change of the commits in the merge. For example, if you merged branch
has a commit that is tagged as feature, one tagged as bugfix and one as major
change, the bump on the version once it's merged will be just one bump on the
major number. If your branch have multiple feature changes and multiple
bugfixes, then only the feature number will be increased by one.

That is because once you merge a branch, your commit history looks like this::

      * de86fd4 Merge pull request #2  -> 2.0.0, only the greatest is used
      |\
      | * e728f5a feature commit
      | * e356889 bugfix commit
      | * c9ff08e feature commit
      | * b8dc51e major commit
      |/
      * 2f811c7 Merge pull request #1  -> 1.0.1, just one bump
      |\
      | * af7930f bugfix commit
      | * e356889 bugfix commit
      |/
      * 2e8cf03 major commit           -> 1.0.0
      * d6ff904 feature commit         -> 0.1.0


As you can see, the last commit has two parents, and the main history does not
include the commits that were merged.
