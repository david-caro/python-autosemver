#!/bin/bash -e

FIXTURES="$BATS_TEST_DIRNAME/fixtures"
GIT="env HOME=$BATS_TEST_DIRNAME git"


common.add_bug_commits() {
    echo "something" >> newfile
    $GIT add newfile
    $GIT commit -a -m 'Mèssage with ûtf-8 ßtuff'

    echo "something" >> newfile
    $GIT add newfile
    $GIT commit -a \
        -m "Mèssage with ûtf-8 ßtuff

Sôme description
Sem-Ver: bugfix
"

    echo "something" >> newfile
    $GIT add newfile
    $GIT commit -a \
        -m "Mèssage with ûtf-8 ßtuff

Sôme description (closes #42)
"
}


common.add_feature_commits() {
    echo "something" >> newfile
    $GIT add newfile
    # Dummy old date to make sure the commit order is hierarchycal
    $GIT commit -a \
        --date="Wed Feb 16 14:00 2011 +0100" \
        -m "Mèssage with ûtf-8 ßtuff

Sôme desc
Sem-Ver: feature
"
    echo "something" >> newfile
    $GIT add newfile
    $GIT commit -a \
        -m "Mèssage with ûtf-8 ßtuff

* NEW Sôme description
"
}


common.add_api_breaking_commits() {
    echo "something" >> newfile
    $GIT add newfile
    $GIT commit -a \
        -m "Mèssage with ûtf-8 ßtuff withaverylonglonglongonglonglonglonglonglonglonglonglonglonglonglonglonglongsubject

Sôme desc, with withaverylonglonglongonglonglonglonglonglonglonglonglonglonglonglonglonglongline
Sem-Ver: api breaking
"
    echo "something" >> newfile
    $GIT add newfile
    $GIT commit -a \
        -m "Mèssage with ûtf-8 ßtuff

* INCOMPATIBLE Sôme description
"
}


common.set_git_config() {
    local author="${1:-Wöndérfûl nàmé}"
    $GIT config --add user.name "$author"
    $GIT config --add user.email "wöndérfûl@éma.il"
}


common.create_dummy_git_repo() {
    local basedir="${1?}"
    rm -rf "$basedir"
    mkdir -p "$basedir"
    pushd "$basedir"
    $GIT init .
    common.set_git_config
    common.add_bug_commits
    common.set_git_config "author2"
    common.add_feature_commits
    common.set_git_config
    common.add_api_breaking_commits
    common.add_feature_commits
    common.add_api_breaking_commits
    common.add_bug_commits
    common.add_api_breaking_commits
    common.add_feature_commits
    common.add_bug_commits
}

common.create_dummy_git_repo_with_tags() {
    local basedir="${1?}"
    rm -rf "$basedir"
    mkdir -p "$basedir"
    pushd "$basedir"
    $GIT init .
    common.set_git_config
    common.add_bug_commits
    git tag '1.2.3'
    common.set_git_config "author2"
    common.add_feature_commits
    git tag 'v2.2.3'
    common.set_git_config
    common.add_api_breaking_commits
    git tag 'v2343.3'
    common.add_feature_commits
    common.add_api_breaking_commits
    git tag 'v3'
    common.add_bug_commits
    common.add_api_breaking_commits
    git tag '3'
    common.add_feature_commits
    common.add_bug_commits
    git tag '4.3123.1'
    common.add_feature_commits
    common.add_bug_commits
    git tag '5.6.7.8'
}


common.create_setup.py() {
    cat >> setup.py <<EOS
#encoding: utf-8
import setuptools

URL = 'https://github.com/david-caro/python-autosemver'

setuptools.setup(
        author='Sômeone',
        author_email='david@dcaro.es',
        description='Tools to handle automatic semantic versioning in python',
        install_requires=['autosemver'],
        setup_requires=['autosemver'],
        license='GPLv3',
        name='dummytest',
        package_data={'': ['CHANGELOG', 'AUTHORS']},
        packages=['dummytest'],
        url=URL,
        autosemver={
            'bugtracker_url': URL + '/issues/',
            'with_release_notes': True,
            'with_authors': True,
            'with_changelog': True,
        },
)
EOS
}


common.create_main_module() {
    mkdir dummytest
    cat >> dummytest/__init__.py <<EOI
from .version import __version__

__all__ = ('__version__')
EOI

    cat >> dummytest/version.py <<EOS
import autosemver

__version__ = autosemver.packaging.get_current_version(
    project_name='dummytest'
)

EOS
}


common.create_python_package(){
    common.create_setup.py
    common.create_main_module
}


common.mask_commit_hashes() {
    local fpath="${1?}"
    sed -i -e 's/\(^ *\(MAJOR\|MINOR\|FEATURE\) \).\{8\}: /\1 11111111: /g' \
        "$fpath"
}


common.mask_dates() {
    local fpath="${1?}"
    sed -i -e 's/^\* ... ... .. .... /* --fake_date_placeholder-- /' "$fpath"
}


common.cleanup_changelog() {
    local changelog="${1?}"
    cp "$changelog" "$changelog.clean"
    common.mask_commit_hashes "$changelog.clean"
    common.mask_dates "$changelog.clean"
}


common.cleanup_releasenotes() {
    releasenotes="${1?}"
    cp "$releasenotes" "$releasenotes.clean"
    common.mask_commit_hashes "$releasenotes.clean"
}
