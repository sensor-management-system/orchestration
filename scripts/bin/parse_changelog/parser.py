# SPDX-FileCopyrightText: 2025
# - Maximilian Schaldach <maximilian.schaldach@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

import re

from .lines import (
    EmptyLine,
    InvalidLine,
    LicenseFinishedLine,
    LicenseLine,
    ReleaseNoteLine,
    SectionLine,
    UnreleasedVersionLine,
    VersionLine,
)
from .errors import LicenseEndNotFoundLineError

VERSION_LINE_PATTERN = (
    r"## (\d+\.\d+\.\d+)(?: - (\d{4}-\d{2}-\d{2}))?(?: \(Unreleased\))?"
)
SECTION_LINE_PATTERN = r"^(Added|Fixed|Changed):$"
RELEASE_NOTE_LINE_PATTERN = r"^-\s.*"
LINEBREAK_NOTE_LINE_PATTERN = r"^\s\s.*"
LICENSE_FINISHED_LINE_PATTERN = "-->"
SEMVER_PATTERN = r"(\d+)\.(\d+)\.(\d+)"


class ReleaseNoteVersion:
    def __init__(self, major, minor, patch, is_unreleased=False):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.is_unreleased = is_unreleased
        self.allowed_sections = ["Added", "Fixed", "Changed"]

    @classmethod
    def from_version_string(cls, version_string, is_unreleased=False):
        match = re.match(SEMVER_PATTERN, version_string)
        if match:
            return cls(
                int(match.group(1)),
                int(match.group(2)),
                int(match.group(3)),
                is_unreleased,
            )
        else:
            return None, None, None

    @property
    def version_string(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def check_semver_increment(self, old):
        if self.major == old.major + 1 and self.minor == 0 and self.patch == 0:
            return True
        if self.major == old.major and self.minor == old.minor + 1 and self.patch == 0:
            return True
        if (
            self.major == old.major
            and self.minor == old.minor
            and self.patch == old.patch + 1
        ):
            return True

        return False

    def check_section(self, section):
        if section not in self.allowed_sections:
            return False
        self.allowed_sections.remove(section)
        return True


class Parser:
    def __init__(self, file_content):
        self.current_line = None
        self.license_finished = False
        self.line_errors = []
        self.file_content = file_content

    def get_line_errors(self):
        for index, line_text in enumerate(self.file_content.splitlines()):
            next_line = self.parse_next_line(index, line_text)
            if not isinstance(next_line, EmptyLine):
                self.current_line = next_line
                self.line_errors.extend(self.current_line.get_errors())
        if not self.license_finished:
            self.line_errors.append(LicenseEndNotFoundLineError(self.current_line))
        return self.line_errors

    def parse_next_line(self, index, line_text):
        stripped_line_text = line_text.rstrip()
        line_number = index + 1

        if not stripped_line_text:
            return EmptyLine(line_number, stripped_line_text, self.current_line)

        if re.match(LICENSE_FINISHED_LINE_PATTERN, stripped_line_text):
            self.license_finished = True
            return LicenseFinishedLine(
                line_number, stripped_line_text, self.current_line
            )

        if not self.license_finished:
            return LicenseLine(line_number, stripped_line_text, self.current_line)

        if re.match(VERSION_LINE_PATTERN, stripped_line_text):
            current_version = ReleaseNoteVersion.from_version_string(
                re.match(VERSION_LINE_PATTERN, stripped_line_text).group(1),
                "Unreleased" in stripped_line_text,
            )
            if not current_version.is_unreleased:
                return VersionLine(
                    line_number,
                    stripped_line_text,
                    self.current_line,
                    current_version=current_version,
                )

            return UnreleasedVersionLine(
                line_number,
                stripped_line_text,
                self.current_line,
                current_version=current_version,
            )

        if re.match(SECTION_LINE_PATTERN, stripped_line_text):
            current_section = re.match(SECTION_LINE_PATTERN, stripped_line_text).group(
                1
            )
            return SectionLine(
                line_number,
                stripped_line_text,
                self.current_line,
                current_section=current_section,
            )

        if re.match(RELEASE_NOTE_LINE_PATTERN, stripped_line_text):
            return ReleaseNoteLine(line_number, stripped_line_text, self.current_line)

        if re.match(LINEBREAK_NOTE_LINE_PATTERN, stripped_line_text):
            return ReleaseNoteLine(line_number, stripped_line_text, self.current_line)

        return InvalidLine(line_number, stripped_line_text, self.current_line)
