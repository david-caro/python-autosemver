#!/bin/bats

load common


@test "tags: preparing" {
    common.create_dummy_git_repo_with_tags "$FIXTURES/repo1"
    common.create_python_package
}


@test "tags: tagged repo" {
    pushd "$FIXTURES/repo1"
    autosemver . version > VERSION
    autosemver . changelog > CHANGELOG
    common.cleanup_changelog "$FIXTURES/EXPECTED_TAGGED_CHANGELOG"
    common.cleanup_changelog CHANGELOG
    [[ "$" ]]
    diff VERSION "$FIXTURES/EXPECTED_VERSION"
    diff "$FIXTURES/EXPECTED_TAGGED_CHANGELOG.clean" CHANGELOG.clean
}
