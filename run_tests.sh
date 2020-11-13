#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# This file is part of autosemver.
# Copyright (C) 2016 David Caro.
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

result=0

echo '########## Running unit tests'
pytest \
    --black \
    --cov=autosemver \
    --cov-report=term-missing \
    -vv \
    "$@" \
    tests/unit \
    autosemver \
|| exit $?

echo
echo '########## Running import format checks'
isort --check-only --diff . \
|| exit $?

echo
echo '########## Building docs'
sphinx-build -qnN docs docs/_build/html \
|| exit $?

echo
echo '########## Running functional tests'
bats tests/functional/*test.sh \
|| exit $?

echo
echo '########## Running type check tests (visualization only)'
mypy . --ignore-missing-imports \
|| exit 0
