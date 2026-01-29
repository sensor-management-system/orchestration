# SPDX-FileCopyrightText: 2025
# - Maximilian Schaldach <maximilian.schaldach@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

# Script to test parse_changelog.py

from scripts.bin.parse_changelog import *


class ValidChangelogTestCase:
    def __init__(self, changelog: str):
        self.changelog = changelog

    def run(self):
        errors = Parser(self.changelog).get_line_errors()
        assert len(errors) == 0


class InvalidChangelogTestCase:
    def __init__(self, changelog: str, expected: LineError):
        self.changelog = changelog
        self.expected = expected

    def error_equals(self, actual: LineError):
        assert issubclass(actual.__class__, LineError)
        assert actual.error_text == self.expected.error_text
        assert actual.error_description == self.expected.error_description
        assert actual.line.line_number == self.expected.line.line_number

    def run(self):
        errors = Parser(self.changelog).get_line_errors()
        assert len(errors) > 0
        error = errors[0]
        self.error_equals(error)


def get_changelog_text_with_license(text):
    return (
        """<!--
...
-->"""
        + text
    )


# ============================
# Test cases
# ============================


def test_semver_increments():
    valid_increments = [
        ("1.0.1", "1.0.0"),
        ("1.1.0", "1.0.0"),
        ("1.0.0", "0.1.0"),
    ]
    invalid_increments = [
        ("1.0.0", "1.0.0"),
        ("1.0.0", "1.1.0"),
        ("1.0.0", "1.0.1"),
        ("2.0.0", "0.0.9"),
    ]

    for valid_increment in valid_increments:
        new, old = valid_increment
        assert ReleaseNoteVersion.from_version_string(new).check_semver_increment(
            ReleaseNoteVersion.from_version_string(old)
        )

    for invalid_increment in invalid_increments:
        new, old = invalid_increment
        assert not ReleaseNoteVersion.from_version_string(new).check_semver_increment(
            ReleaseNoteVersion.from_version_string(old)
        )


def test_missing_license():
    InvalidChangelogTestCase(
        """No license
""",
        LineError(
            Line(1, "No license", None),
            "Missing end of license.",
            "License was never ended.",
        ),
    ).run()


def test_missing_unreleased_version():
    InvalidChangelogTestCase(
        get_changelog_text_with_license(
            """
## 1.1.0 - 01-01-2025

Added:
- ...
"""
        ),
        LineError(
            Line(4, "## 1.1.0 - 01-01-2025", None),
            "Missing unreleased version.",
            "First version must be unreleased.",
        ),
    ).run()


def test_forbidden_section_key():

    InvalidChangelogTestCase(
        get_changelog_text_with_license(
            """
## 1.1.0 (Unreleased)

ForbiddenKey:
- ...
"""
        ),
        LineError(
            Line(6, "ForbiddenKey:", None),
            "Invalid line.",
            "Expected a valid SectionLine, found InvalidLine.",
        ),
    ).run()


def test_missing_section_key():

    InvalidChangelogTestCase(
        get_changelog_text_with_license(
            """
## 1.1.0 (Unreleased)

- Missing section key before Release Note.
"""
        ),
        LineError(
            Line(6, "ForbiddenKey:", None),
            "Invalid line.",
            "Expected a valid SectionLine, found ReleaseNoteLine.",
        ),
    ).run()


def test_invalid_release_note_line():
    InvalidChangelogTestCase(
        get_changelog_text_with_license(
            """
## 1.1.0 (Unreleased)

Added:
Release note without dash.
"""
        ),
        LineError(
            Line(7, "Release note without dash.", None),
            "Invalid line.",
            "Expected a valid ReleaseNoteLine, found InvalidLine.",
        ),
    ).run()


def test_release_note_without_merge_request():
    InvalidChangelogTestCase(
        get_changelog_text_with_license(
            """
## 1.1.0 (Unreleased)

Added:
- Release note without Merge Request.
"""
        ),
        LineError(
            Line(7, "- Release note without Merge Request.", None),
            "Missing Merge Request.",
            "Every Release Note of unreleased version requires a valid Merge Request link.",
        ),
    ).run()


def test_release_note_with_invalid_link_title():
    InvalidChangelogTestCase(
        get_changelog_text_with_license(
            """
## 1.1.0 (Unreleased)

Added:
- Release note with invalid link tile ([Invalid](www.example.com)).
"""
        ),
        LineError(
            Line(
                7,
                "- Release note with invalid link tile ([Invalid](www.example.com)).",
                None,
            ),
            "Invalid link title.",
            "Allowed titles are: Merge Request, Wiki.",
        ),
    ).run()


def test_version_with_duplicate_section():
    InvalidChangelogTestCase(
        get_changelog_text_with_license(
            """
## 1.1.0 (Unreleased)

Added:
- Release note with Merge Request ([Merge Request](www.example.com)).

Added:
"""
        ),
        LineError(
            Line(9, "Added:", None),
            "Duplicate section 'Added'.",
            "Please merge sections.",
        ),
    ).run()


def test_section_without_release_notes():
    InvalidChangelogTestCase(
        get_changelog_text_with_license(
            """
## 1.1.0 (Unreleased)

Added:

Fixed:
"""
        ),
        LineError(
            Line(8, "Added:", None),
            "Invalid line.",
            "Expected a valid ReleaseNoteLine, found SectionLine.",
        ),
    ).run()


def test_changelog_with_multiple_unreleased_versions():
    InvalidChangelogTestCase(
        get_changelog_text_with_license(
            """
## 1.1.0 (Unreleased)

Added:
- Release note with Merge Request ([Merge Request](www.example.com)).

## 1.0.9 (Unreleased)
"""
        ),
        LineError(
            Line(9, "Added:", None),
            "Invalid unreleased version.",
            "Unreleased version is only allowed at top.",
        ),
    ).run()


def test_version_with_invalid_increment():
    InvalidChangelogTestCase(
        get_changelog_text_with_license(
            """
## 1.1.0 (Unreleased)

Added:
- Release note with Merge Request ([Merge Request](www.example.com)).

## 0.1.0 - 01-01-2025
"""
        ),
        LineError(
            Line(9, "Added:", None),
            "Incorrect version increment.",
            "Version 1.1.0 is not a valid successor to version 0.1.0.",
        ),
    ).run()


def test_valid_changelog():
    ValidChangelogTestCase(
        get_changelog_text_with_license(
            """
## 1.1.0 (Unreleased)
Added:
- Release note with Merge Request ([Merge Request](www.example.com)).
- Another release note with Merge Request ([Merge Request](www.example.com)) and Wiki ([Wiki](www.example.com)).

Fixed:
- Release note with Merge Request ([Merge Request](www.example.com)).

Changed:
- Release note with Merge Request ([Merge Request](www.example.com)).

## 1.0.9 - 01-01-2025
Added:
- Release note without Merge Request.

## 1.0.8 - 01-01-2024
Added:
- Release note without Merge Request.
"""
        )
    ).run()


def test_valid_changelog_with_newly_created_empty_unreleased_version():
    ValidChangelogTestCase(
        get_changelog_text_with_license(
            """
## 1.1.1 (Unreleased)

## 1.1.0 - 01-01-2025
Added:
- Release note with Merge Request ([Merge Request](www.example.com)).
- Another release note with Merge Request ([Merge Request](www.example.com)) and Wiki ([Wiki](www.example.com)).
"""
        )
    ).run()
