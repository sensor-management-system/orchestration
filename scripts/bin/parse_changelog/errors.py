# SPDX-FileCopyrightText: 2025
# - Maximilian Schaldach <maximilian.schaldach@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

from .utils import Console


class LineError:
    def __init__(self, line, error_text, error_description):
        self.line = line
        self.error_text = error_text
        self.error_description = error_description

    def __str__(self):
        text = Console.get_styled_text("ERROR ", Console.Style.FAIL, Console.Style.BOLD)
        text += f"in line {self.line.line_number}\n"
        text += Console.get_styled_text(self.line.content, Console.Style.GRAY) + "\n"
        text += (
            Console.get_styled_text(
                self.error_text, Console.Style.FAIL, Console.Style.BOLD
            )
            + "\n"
        )
        text += (
            Console.get_styled_text(self.error_description, Console.Style.FAIL) + "\n"
            if self.error_description
            else "\n"
        )
        return text


class InvalidSuccessorLineError(LineError):
    def __init__(self, line):
        self.line = line
        super().__init__(
            line,
            "Invalid line.",
            f"Expected a valid {' or '.join(line.previous_line.get_allowed_successor_line_type_strings())}, found {line.__class__.__name__}.",
        )


class IncorrectVersionIncrementLineError(LineError):
    def __init__(self, line):
        self.line = line
        super().__init__(
            line,
            "Incorrect version increment.",
            f"Version {line.previous_line.current_version.version_string} is not a valid successor to version {line.current_version.version_string}.",
        )


class InvalidUnreleasedVersionLineError(LineError):
    def __init__(self, line):
        self.line = line
        super().__init__(
            line,
            "Invalid unreleased version.",
            f"Unreleased version is only allowed at top.",
        )


class MissingUnreleasedVersionLineError(LineError):
    def __init__(self, line):
        self.line = line
        super().__init__(
            line,
            "Missing unreleased version.",
            f"First version must be unreleased.",
        )


class InvalidLinkTitleLineError(LineError):
    def __init__(self, line):
        self.line = line
        super().__init__(
            line,
            "Invalid link title.",
            "Allowed titles are: Merge Request, Wiki.",
        )


class MissingMergeRequestLinkLineError(LineError):
    def __init__(self, line):
        self.line = line
        super().__init__(
            line,
            "Missing Merge Request.",
            "Every Release Note of unreleased version requires a valid Merge Request link.",
        )


class DuplicateSectionLineError(LineError):
    def __init__(self, line):
        self.line = line
        super().__init__(
            line,
            f"Duplicate section '{line.current_section}'.",
            "Please merge sections.",
        )


class LicenseEndNotFoundLineError(LineError):
    def __init__(self, line):
        self.line = line
        super().__init__(
            line,
            "Missing end of license.",
            "License was never ended.",
        )
