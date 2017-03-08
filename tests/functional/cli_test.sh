#!/bin/bats

load common


@test "cli: preparing" {
    common.create_dummy_git_repo "$FIXTURES/repo1"
    common.create_python_package
}


@test "cli: changelog" {
    pushd "$FIXTURES/repo1"
    autosemver . changelog > CHANGELOG
    common.cleanup_changelog "$FIXTURES/EXPECTED_CHANGELOG"
    common.cleanup_changelog CHANGELOG
    diff "$FIXTURES/EXPECTED_CHANGELOG.clean" CHANGELOG.clean
}


@test "cli: authors" {
    pushd "$FIXTURES/repo1"
    autosemver . authors > AUTHORS
    diff "$FIXTURES/EXPECTED_AUTHORS" AUTHORS
}


@test "cli: rpm changelog" {
    pushd "$FIXTURES/repo1"
    autosemver . changelog --rpm > RPM_CHANGELOG
    common.cleanup_changelog "$FIXTURES/EXPECTED_RPM_CHANGELOG"
    common.cleanup_changelog RPM_CHANGELOG
    diff "$FIXTURES/EXPECTED_RPM_CHANGELOG.clean" RPM_CHANGELOG.clean
}


@test "cli: releasenotes" {
    pushd "$FIXTURES/repo1"
    autosemver . releasenotes > RELEASE_NOTES
    common.cleanup_releasenotes "$FIXTURES/EXPECTED_RELEASE_NOTES"
    common.cleanup_releasenotes RELEASE_NOTES
    diff "$FIXTURES/EXPECTED_RELEASE_NOTES.clean" RELEASE_NOTES.clean
}


@test "cli: tag" {
    pushd "$FIXTURES/repo1"
    autosemver . tag
    git tag > TAGS
    diff "$FIXTURES/EXPECTED_TAGS" TAGS
}
