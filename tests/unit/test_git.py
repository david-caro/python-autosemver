# -*- coding: utf-8 -*-
#
# This file is part of autosemver.
# Copyright (C) 2018 David Caro.
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
from __future__ import absolute_import, division, print_function

import pytest
import six

from autosemver import git


def _get_possible_params(test_matrix):
    params = {}
    for case in test_matrix.values():
        params.update(case)

    return list(sorted(params.keys()))


def _get_ordered_test_params(params_list, test_params, default_value=None):
    ordered_test_params = []
    for param in params_list:
        ordered_test_params.append(test_params.get(param, default_value))

    return ordered_test_params


def parametrize(test_matrix, default_value=None):
    ids = []
    tests_params = []
    available_params = _get_possible_params(test_matrix)

    for test_name, params in six.iteritems(test_matrix):
        ids.append(test_name)
        tests_params.append(
            _get_ordered_test_params(
                params_list=available_params,
                test_params=params,
                default_value=default_value,
            )
        )

    return lambda func: pytest.mark.parametrize(
        ','.join(available_params),
        tests_params,
        ids=ids,
    )(func)


@parametrize({
    'not indented, no space': {
        'what': 'myspacebarisbrokenreallyreallybad',
        'cols': 5,
        'expected': ('acebarisbrokenreallyreallybad', 'mysp-'),
    },
    'not indented, space in the middle': {
        'what': 'a' * 10 + ' ' + 'a' * 10,
        'cols': 14,
        'expected': ('a' * 10, 'a' * 10),
    },
    'not indented, multiple spaces': {
        'what': 'finally got it fixed :)',
        'cols': 10,
        'expected': ('got it fixed :)', 'finally'),
    },
    'not indented, space at the beggining': {
        'what': ' oopsIthinkIbrokeitagain',
        'cols': 5,
        'expected': ('IthinkIbrokeitagain', 'oops-'),
    },
    'not indented, space at the end': {
        'what': 'dammitlettrythis ',
        'cols': 5,
        'expected': ('itlettrythis ', 'damm-'),
    },
    'indented, multiple spaces': {
        'what': 'got   it  working  again  but   now  it   gets   stuck',
        'cols': 10,
        'indent': '    ',
        'expected': (
            'it  working  again  but   now  it   gets   stuck',
            '    got',
        ),
    },
    'indented, no space': {
        'what': 'dammitlettrythis',
        'cols': 10,
        'indent': '    ',
        'expected': ('tlettrythis', '    dammi-'),
    },
})
def test_strip_line(cols, expected, indent, what):
    params = {'what': what}
    if cols is not None:
        params['cols'] = cols
    if indent is not None:
        params['indent'] = indent

    result = git.split_line(**params)
    assert result == expected


@parametrize({
    'not indented, not wrapped': {
        'text': 'some short string',
        'expected': 'some short string',
    },
    'not indented, wrapped': {
        'text': 'some short string',
        'cols': 3,
        'expected': 'so-\nme\nsh-\nort\nst-\nri-\nng',
    },
    'indented, wrapped': {
        'text': 'some short string',
        'cols': 5,
        'indent': '  ',
        'expected': '  so-\n  me\n  sh-\n  ort\n  st-\n  ri-\n  ng',
    },
})
def test_fit_to_cols(cols, expected, indent, text):
    params = {
        'what': text,
    }
    if indent is not None:
        params['indent'] = indent
    if cols is not None:
        params['cols'] = cols

    result = git.fit_to_cols(**params)

    assert result == expected
