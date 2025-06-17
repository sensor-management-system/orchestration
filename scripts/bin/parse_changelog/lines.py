# SPDX-FileCopyrightText: 2025
# - Maximilian Schaldach <maximilian.schaldach@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

import re

from .errors import (
    DuplicateSectionLineError,
    InvalidSuccessorLineError,
    InvalidLinkTitleLineError,
    IncorrectVersionIncrementLineError,
    InvalidUnreleasedVersionLineError,
    MissingUnreleasedVersionLineError,
    MissingMergeRequestLinkLineError,
)


LINK_PATTERN = r"\(\[(.*?)\]\(.*?\)\)"

class Line:
    def __init__(
        self,
        line_number,
        content,
        previous_line,
        current_version=None,
        current_section=None,
    ):
        self.errors = []
        self.line_number = line_number
        self.content = content
        self.previous_line = previous_line
        self.current_version = (
            current_version or previous_line.current_version if previous_line else None
        )
        self.current_section = (
            current_section or previous_line.current_section if previous_line else None
        )

    @staticmethod
    def get_allowed_successor_line_types():
        return []

    @classmethod
    def get_allowed_successor_line_type_strings(cls):
        return [
            allowed_type.__name__
            for allowed_type in cls.get_allowed_successor_line_types()
        ]

    # validation of line type appearance in context of successor
    def validate_successor_line_type(self, successor):
        if not successor:
            return
        if successor.__class__ not in self.get_allowed_successor_line_types():
            return successor.errors.append(InvalidSuccessorLineError(successor))

    # custom validation for each line type
    def validate(self):
        pass

    def get_errors(self):
        self.errors = []
        if self.previous_line:
            self.previous_line.validate_successor_line_type(self)
        self.validate()
        return self.errors


class VersionLine(Line):
    @staticmethod
    def get_allowed_successor_line_types():
        return [SectionLine]

    def validate(self):
        if (
            self.previous_line
            and self.previous_line.current_version
            and not self.previous_line.current_version.check_semver_increment(
                self.current_version
            )
        ):
            self.errors.append(IncorrectVersionIncrementLineError(self))

        if (
            self.current_version.is_unreleased
            and self.previous_line.current_version is not None
        ):
            self.errors.append(InvalidUnreleasedVersionLineError(self))

        if (
            self.current_version.is_unreleased == False
            and self.previous_line.current_version is None
        ):
            self.errors.append(MissingUnreleasedVersionLineError(self))


class SectionLine(Line):
    @staticmethod
    def get_allowed_successor_line_types():
        return [ReleaseNoteLine]

    def validate(self):
        if self.current_version and not self.current_version.check_section(
            self.current_section
        ):
            self.errors.append(DuplicateSectionLineError(self))


class ReleaseNoteLine(Line):
    @staticmethod
    def get_allowed_successor_line_types():
        return [VersionLine, SectionLine, ReleaseNoteLine]

    def validate(self):
        allowed_link_titles = ["Merge Request", "Wiki"]
        link_pattern_matches = re.findall(LINK_PATTERN, self.content)
        for match in link_pattern_matches:
            if not match in allowed_link_titles:
                self.errors.append(InvalidLinkTitleLineError(self))
        if (
            self.current_version
            and self.current_version.is_unreleased
            and not "Merge Request" in link_pattern_matches
        ):
            self.errors.append(MissingMergeRequestLinkLineError(self))


class InvalidLine(Line):
    @staticmethod
    def get_allowed_successor_line_types():
        return [VersionLine, SectionLine, ReleaseNoteLine]


class LicenseFinishedLine(Line):
    @staticmethod
    def get_allowed_successor_line_types():
        return [VersionLine]


class EmptyLine(Line):
    @staticmethod
    def get_allowed_successor_line_types():
        return []


class LicenseLine(Line):
    @staticmethod
    def get_allowed_successor_line_types():
        return [LicenseLine, LicenseFinishedLine]
