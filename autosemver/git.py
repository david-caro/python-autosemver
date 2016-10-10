#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file was part of lago project.
# This file was part of INSPIRE-SCHEMAS.
# This file is part of autosemver.
# Copyright (C) 2014 Red Hat, Inc.
# Copyright (C) 2016 CERN.
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
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""
Script to generate the version, changelog and releasenotes from the git
repository.
"""
from __future__ import print_function

import os
import re
from collections import OrderedDict, defaultdict

import dulwich.repo
import dulwich.walk

BUG_URL_REG = re.compile(
    r'.*(closes #|fixes #|adresses #)(?P<bugid>\d+)'
)
VALID_TAG = re.compile(r'^\d+\.\d+$')
FEAT_HEADER = re.compile(
    r'\nsem-ver:\s*.*(feature|deprecat).*\n',
    flags=re.IGNORECASE,
)
FEAT_MSG = re.compile(r'\n\* NEW')
MAJOR_HEADER = re.compile(r'\nsem-ver:\s*.*break.*\n', flags=re.IGNORECASE)
MAJOR_MSG = re.compile(r'\n\* INCOMPATIBLE')


def get_repo_object(repo, object_name):
    try:
        object_name = object_name.encode()
    except:
        pass

    return repo.get_object(object_name)


def fit_to_cols(what, indent, cols=79):
    lines = []
    free_cols = cols - len(indent)
    while len(what) > free_cols and ' ' in what.lstrip():
        cutpoint = free_cols
        extra_indent = ''
        if what[free_cols] != ' ':
            try:
                prev_space = what[:free_cols].rindex(' ')
                lines.append(indent + what[:prev_space])
                cutpoint = prev_space + 1
                extra_indent = '          '
            except ValueError:
                lines.append(indent + what[:free_cols] + '-')
        else:
            lines.append(indent + what[:free_cols])
        what = extra_indent + what[cutpoint:]
    lines.append(indent + what)
    return '\n'.join(lines)


def get_bugs_from_commit_msg(commit_msg):
    bugs = []
    for line in commit_msg.split(b'\n'):
        match = BUG_URL_REG.match(line.decode('utf-8'))
        if match:
            bugs.append(match.groupdict()['bugid'])
    return bugs


def pretty_commit(commit, version=None, commit_type='bug', bugtracker_url=''):
    message = commit.message.decode('utf-8')
    subject = commit.message.split(b'\n', 1)[0]  # noqa
    short_hash = commit.sha().hexdigest()[:8]  # noqa
    author = commit.author  # noqa
    bugs = get_bugs_from_commit_msg(commit.message)
    if bugs:
        changelog_bugs = fit_to_cols(
            'FIXED ISSUES: ' + ', '.join(
                '{bugtracker_url}{bug}'.format(
                    bugtracker_url=bugtracker_url,
                    bug=bug,
                ) for bug in bugs
            ),
            indent='    ',
        ) + '\n'
    else:
        changelog_bugs = ''  # noqa

    feature_header = ''
    if commit_type == 'feature':
        feature_header = 'FEATURE'
    elif commit_type == 'api_break':
        feature_header = 'MAJOR'
    else:
        feature_header = 'MINOR'

    changelog_message = fit_to_cols(  # noqa
        '{feature_header} {short_hash}: {subject}'.format(**vars()),
        indent='    ',
    )

    return (
        (
            '* {version} "{author}"\n'
            if version is not None else ''
        ) + '{changelog_message}\n' + '{changelog_bugs}'
    ).format(**vars())


def get_tags(repo):
    return {
        commit.decode('utf-8'): os.path.basename(tag_ref)
        for tag_ref, commit in repo.get_refs().items()
        if tag_ref.startswith(b'refs/tags/') and VALID_TAG.match(
            tag_ref[len('refs/tags/'):].decode('utf-8')
        )
    }


def get_refs(repo):
    refs = defaultdict(set)
    for ref, commit in repo.get_refs().items():
        refs[commit].add(commit)
        refs[commit].add(ref)
    return refs


def fuzzy_matches_ref(fuzzy_ref, ref):
    cur_section = ''
    for path_section in reversed(ref.split(b'/')):
        cur_section = os.path.normpath(os.path.join(path_section, cur_section))
        if fuzzy_ref == cur_section:
            return True
    return False


def fuzzy_matches_refs(fuzzy_ref, refs):
    return any(fuzzy_matches_ref(fuzzy_ref, ref) for ref in refs)


def get_children_per_parent(repo_path):
    repo = dulwich.repo.Repo(repo_path)
    children_per_parent = defaultdict(set)

    for entry in repo.get_walker(order=dulwich.walk.ORDER_TOPO):
        for parent in entry.commit.parents:
            children_per_parent[parent].add(entry.commit.sha().hexdigest())

    return children_per_parent


def get_first_parents(repo_path):
    repo = dulwich.repo.Repo(repo_path)
    #: these are the commits that are parents of more than one other commit
    first_parents = []
    on_merge = False

    for entry in repo.get_walker(order=dulwich.walk.ORDER_TOPO):
        commit = entry.commit
        # In order to properly work on python 2 and 3 we need some utf magic
        parents = commit.parents and [i.decode('utf-8') for i in
                                      commit.parents]
        if not parents:
            if commit.sha().hexdigest() not in first_parents:
                first_parents.append(commit.sha().hexdigest())
        elif len(parents) == 1 and not on_merge:
            if commit.sha().hexdigest() not in first_parents:
                first_parents.append(commit.sha().hexdigest())
            if parents[0] not in first_parents:
                first_parents.append(parents[0])
        elif len(parents) > 1 and not on_merge:
            on_merge = True
            if commit.sha().hexdigest() not in first_parents:
                first_parents.append(commit.sha().hexdigest())
            if parents[0] not in first_parents:
                first_parents.append(parents[0])
        elif parents and commit.sha().hexdigest() in first_parents:
            if parents[0] not in first_parents:
                first_parents.append(parents[0])

    return first_parents


def has_firstparent_child(sha, first_parents, parents_per_child):
    return any(
        child for child in parents_per_child[sha] if child in first_parents
    )


def get_merged_commits(repo, commit, first_parents, children_per_parent):
    merge_children = set()

    to_explore = set([commit.sha().hexdigest()])

    while to_explore:
        next_sha = to_explore.pop()
        next_commit = get_repo_object(repo, next_sha)
        if (
            next_sha not in first_parents and not has_firstparent_child(
                next_sha, first_parents, children_per_parent
            ) or next_sha in commit.parents
        ):
            merge_children.add(next_sha)

        non_first_parents = (
            parent
            for parent in next_commit.parents if parent not in first_parents
        )
        for child_sha in non_first_parents:
            if child_sha not in merge_children and child_sha != next_sha:
                to_explore.add(child_sha)

    return merge_children


def get_children_per_first_parent(repo_path):
    repo = dulwich.repo.Repo(repo_path)
    first_parents = get_first_parents(repo_path)
    children_per_parent = get_children_per_parent(repo_path)
    children_per_first_parent = OrderedDict()

    for first_parent in first_parents:
        commit = get_repo_object(repo, first_parent)
        if len(commit.parents) > 1:
            children = get_merged_commits(
                repo=repo,
                commit=commit,
                first_parents=first_parents,
                children_per_parent=children_per_parent,
            )
        else:
            children = set()

        children_per_first_parent[first_parent] = [
            get_repo_object(repo, child) for child in children
        ]

    return children_per_first_parent


def get_version(commit, tags, maj_version=0, feat_version=0, fix_version=0,
                children=None):
    children = children or []
    commit_type = get_commit_type(commit, children)
    commit_sha = commit.sha().hexdigest()

    if commit_sha in tags:
        maj_version, feat_version = tags[commit_sha].split(b'.')
        maj_version = int(maj_version)
        feat_version = int(feat_version)
        fix_version = 0
    elif commit_type == 'api_break':
        maj_version += 1
        feat_version = 0
        fix_version = 0
    elif commit_type == 'feature':
        feat_version += 1
        fix_version = 0
    else:
        fix_version += 1

    version = (maj_version, feat_version, fix_version)
    return version


def is_api_break(commit):
    return (
        MAJOR_HEADER.search(commit.message.decode('utf-8')) or
        MAJOR_MSG.search(commit.message.decode('utf-8'))
    )


def is_feature(commit):
    return (
        FEAT_HEADER.search(commit.message.decode('utf-8')) or
        FEAT_MSG.search(commit.message.decode('utf-8'))
    )


def get_commit_type(commit, children=None, tags=None, prev_version=None):
    children = children or []
    tags = tags or []
    prev_version = prev_version or (0, 0, 0)
    commit_sha = commit.sha().hexdigest()

    if commit_sha in tags:
        maj_version, feat_version = tags[commit_sha].split(b'.')
        maj_version = int(maj_version)
        feat_version = int(feat_version)
        if maj_version > prev_version[0]:
            return 'api_break'
        elif feat_version > prev_version[1]:
            return 'feature'
        return 'bug'

    if any(is_api_break(child) for child in children + [commit]):
        return 'api_break'
    elif any(is_feature(child) for child in children + [commit]):
        return 'feature'
    else:
        return 'bug'
