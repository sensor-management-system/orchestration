# SPDX-FileCopyrightText: 2025
# - Maximilian Schaldach <maximilian.schaldach@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

# Script to check the validation of the CHANGELOG.md file.

# The following checks are done:
#
# - Ensure every line is followed by an allowed successor type:
#   v: version line
#   s: section line
#   r: release note line
#
#   Valid transitions:
#   V -> vS
#   S -> sR
#   R -> r | rV | rS | rR
#
# Versions
# - Ensure every version consists of a valid semantic version tag and a well-formatted date or Unreleased-mark.
#   valid syntax with date: <MAJOR>.<MINOR>.<PATCH> - <YYYY>-<MM>-<DD>
#   valid syntax for unreleased: <MAJOR>.<MINOR>.<PATCH> (Unreleased)
# - Ensure there is exactly one unreleased version at the top of the changelog.
# - Ensure every version is a correct semantic increment of its predecessor
#   (one of the subversions is incremented while subordinate versions are set to 0).
#
# Sections
# - Ensure there are no invalid section keys. Allowed keys are: Added, Changed, Fixed
# - Ensure there is no duplicate section entry per version.
# - Ensure there is no empty section without a release note.
#
# Release notes
# - Ensure every release note line starts with a dash.
# - Ensure every release note entry of the latest version contains a Merge Request link.
#   valid syntax for links: ([<LINK-TITLE>](<LINK>))
#   valid link titles are: Merge Request, Wiki

import argparse
import sys

from .utils import (
    get_changelog_from_file,
    get_changelog_from_branch,
    ChangelogNotFoundError,
    Console,
)
from .parser import Parser


def die(message, exit_code=1):
    Console.print_error(message)
    sys.exit(exit_code)


def main():
    # file fetching/reading
    arg_parser = argparse.ArgumentParser(
        description="Parse a SMS CHANGELOG.md file from a branch or local file."
    )
    group = arg_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--branch", type=str, help="Specify a branch name")
    group.add_argument("--file", type=str, help="Specify a CHANGELOG.md file path")

    args = arg_parser.parse_args()
    selected_branch = args.branch
    selected_file = args.file

    changelog = None
    try:
        if selected_branch:
            changelog = get_changelog_from_branch(selected_branch)
        if selected_file:
            changelog = get_changelog_from_file(selected_file)
    except ChangelogNotFoundError as e:
        die(str(e))

    # parse and validate
    errors = Parser(changelog).get_line_errors()
    for error in errors:
        print(error)

    # fail on error
    if errors:
        die("Changelog invalid, sorry :-(")

    # pass
    Console.print("Changelog valid.", Console.Style.OK)


if __name__ == "__main__":
    main()
