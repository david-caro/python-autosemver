# -*- coding: utf-8 -*-
#
# This file was part of lago project.
# This file was part of INSPIRE-SCHEMAS.
# This file is part of autosemver.
# Copyright (C) 2016 CERN.
#
# autosemver is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# autosemver is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with autosemver; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.
"""Automatic semantic versioning from git history for python packages"""

import os

from setuptools import setup

IN_A_PACKAGE = False
PKG_INFO = os.path.join(os.path.dirname('__file__'), 'PKG-INFO')
if not os.path.exists(PKG_INFO):
    from autosemver import PROJECT_NAME
    from autosemver.packaging import (
        get_authors,
        get_changelog,
        get_current_version,
    )
    __version__ = get_current_version(project_name=PROJECT_NAME)
else:
    IN_A_PACKAGE = True
    with open(PKG_INFO) as info_fd:
        for line in info_fd.readlines():
            if line.startswith('Version: '):
                __version__ = line.split(' ', 1)[-1]
                break
        else:
            raise ImportError('Unable to find version for autosemver')



if __name__ == '__main__':
    if not IN_A_PACKAGE:
        with open('AUTHORS', 'w') as authors_fd:
            authors_fd.write('\n'.join(get_authors()))

        with open('CHANGELOG', 'w') as changelog_fd:
            changelog_fd.write(get_changelog())

    setup(
        author='David Caro',
        author_email='david@dcaro.es',
        install_requires=['dulwich'],
        license='GPLv3',
        name='autosemver',
        package_data={'': ['CHANGELOG', 'AUTHORS']},
        packages=['autosemver'],
        url='https://github.com/david-caro/python-autosemver',
        version=__version__,
        entry_points={
            'console_scripts': 'autosemver=autosemver:main',
            'distutils.setup_keywords': [
                'autosemver=autosemver:distutils',
                'bugtracker_url=autosemver:distutils',
            ],
        }
    )
