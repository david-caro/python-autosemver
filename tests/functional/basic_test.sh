#!/bin/bats


FIXTURES="$BATS_TEST_DIRNAME/fixtures"


add_bug_commits() {
    echo "something" >> newfile
    git add newfile
    git commit -a -m 'Mèssage with ûtf-8 ßtuff'

    echo "something" >> newfile
    git add newfile
    git commit -a \
        -m "Mèssage with ûtf-8 ßtuff

Sôme description
Sem-Ver: bugfix
"

    echo "something" >> newfile
    git add newfile
    git commit -a \
        -m "Mèssage with ûtf-8 ßtuff

Sôme description (closes #42)
"
}


add_feature_commits() {
    echo "something" >> newfile
    git add newfile
    git commit -a \
        -m "Mèssage with ûtf-8 ßtuff

Sôme desc
Sem-Ver: feature
"
    echo "something" >> newfile
    git add newfile
    git commit -a \
        -m "Mèssage with ûtf-8 ßtuff

* NEW Sôme description
"
}


add_api_breaking_commits() {
    echo "something" >> newfile
    git add newfile
    git commit -a \
        -m "Mèssage with ûtf-8 ßtuff

Sôme desc
Sem-Ver: api breaking
"
    echo "something" >> newfile
    git add newfile
    git commit -a \
        -m "Mèssage with ûtf-8 ßtuff

* INCOMPATIBLE Sôme description
"
}


set_git_config() {
    local author="${1:-Wöndérfûl nàmé}"
    git config --add user.name "$author"
    git config --add user.email "wöndérfûl@éma.il"
}


create_dummy_git_repo() {
    local basedir="${1?}"
    rm -rf "$basedir"
    mkdir -p "$basedir"
    pushd "$basedir"
    git init .
    set_git_config
    add_bug_commits
    set_git_config "author2"
    add_feature_commits
    set_git_config
    add_api_breaking_commits
}


create_setup.py() {
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
        bugtracker_url=URL + '/issues/',
        autosemver=True,
)
EOS
}


create_main_module() {
    mkdir dummytest
    touch dummytest/__init__.py
    cat >> dummytest/version.py <<EOS
import autosemver

__version__ = autosemver.packaging.get_current_version(
    package_name='dummytest'
)

EOS
}


create_python_package(){
    create_setup.py
    create_main_module
}


mask_commit_hashes() {
    local fpath="${1?}"
    sed -e 's/\(^ *\(MAJOR\|MINOR\|FEATURE\) \).\{8\}: /\1 11111111: /g' \
        "$fpath" \
    > "$fpath.clean"
}


@test "basic: preparing" {
    create_dummy_git_repo "$FIXTURES/repo1"
    create_python_package
}


@test "basic: sdist" {
    pushd "$FIXTURES/repo1"
    python setup.py sdist
    tree
    [[ -f dist/dummytest-2.0.0.tar.gz ]]
}


@test "basic: changelog" {
    pushd "$FIXTURES/repo1"
    mask_commit_hashes "$FIXTURES/EXPECTED_CHANGELOG"
    mask_commit_hashes CHANGELOG
    diff "$FIXTURES/EXPECTED_CHANGELOG.clean" CHANGELOG.clean
}


@test "basic: authors" {
    pushd "$FIXTURES/repo1"
    diff "$FIXTURES/EXPECTED_AUTHORS" AUTHORS
}


@test "basic: rpm changelog" {
    pushd "$FIXTURES/repo1"
    mask_commit_hashes "$FIXTURES/EXPECTED_RPM_CHANGELOG"
    autosemver . changelog --rpm > RPM_CHANGELOG
    mask_commit_hashes RPM_CHANGELOG
    diff "$FIXTURES/EXPECTED_RPM_CHANGELOG.clean" RPM_CHANGELOG.clean
}


@test "basic: releasenotes" {
    pushd "$FIXTURES/repo1"
    mask_commit_hashes "$FIXTURES/EXPECTED_RELEASENOTES"
    autosemver . releasenotes > RELEASENOTES
    mask_commit_hashes RELEASENOTES
    diff "$FIXTURES/EXPECTED_RELEASENOTES.clean" RELEASENOTES.clean
}
