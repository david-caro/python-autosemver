#!/bin/bats

load common


@test "lib: preparing" {
    common.create_dummy_git_repo "$FIXTURES/repo1"
    common.create_python_package
}


@test "lib: sdist" {
    pushd "$FIXTURES/repo1"
    python setup.py sdist
    tree
    [[ -f dist/dummytest-6.2.3.tar.gz ]]
}


@test "lib: changelog" {
    pushd "$FIXTURES/repo1"
    common.cleanup_changelog "$FIXTURES/EXPECTED_CHANGELOG"
    common.cleanup_changelog CHANGELOG
    diff "$FIXTURES/EXPECTED_CHANGELOG.clean" CHANGELOG.clean
}


@test "lib: authors" {
    pushd "$FIXTURES/repo1"
    diff "$FIXTURES/EXPECTED_AUTHORS" AUTHORS
}


@test "lib: releasenotes" {
    pushd "$FIXTURES/repo1"
    common.cleanup_releasenotes "$FIXTURES/EXPECTED_RELEASE_NOTES"
    common.cleanup_releasenotes RELEASE_NOTES
    diff "$FIXTURES/EXPECTED_RELEASE_NOTES.clean" RELEASE_NOTES.clean
}


@test "lib: package version pattern" {
    pushd "$FIXTURES/repo1"
    python setup.py sdist
    pip uninstall -y dummytest || :
    pip install dist/*tar.gz
    cd /tmp

    expected_version="6.2.3"
    version="$(python -c '
from __future__ import print_function;
import dummytest
print(dummytest.__version__)')"

    echo "Checking that '$version'=='$expected_version'"
   [[ "$version" == "$expected_version" ]]

}
