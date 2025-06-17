# SPDX-FileCopyrightText: 2025
# - Maximilian Schaldach <maximilian.schaldach@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

import sys
from enum import Enum

import requests


class Console:
    class Style(Enum):
        OK = "\033[92m"
        WARNING = "\033[93m"
        FAIL = "\033[91m"
        ENDC = "\033[0m"
        BOLD = "\033[1m"
        GRAY = "\033[37m"

    @staticmethod
    def get_styled_text(text, *styles):
        return (
            "".join([style.value for style in styles]) + text + Console.Style.ENDC.value
        )

    @staticmethod
    def print(text, *styles):
        print(Console.get_styled_text(text, *styles))

    @staticmethod
    def print_error(text, *styles):
        print(
            Console.get_styled_text(
                text, Console.Style.FAIL, Console.Style.BOLD, *styles
            ),
            file=sys.stderr,
        )


class GitLab:
    def __init__(self, gitlab_host, project_id):
        self.gitlab_host = gitlab_host
        self.project_id = project_id
        self.file_api_base_url = (
            f"{gitlab_host}/api/v4/projects/{str(project_id)}/repository/files/"
        )

    def get_raw_file(self, file_path, branch_name="main"):
        file_url = f"{self.file_api_base_url}{file_path}/raw?ref={branch_name}"
        response = requests.get(file_url)
        response.raise_for_status()
        return response.text


class ChangelogNotFoundError(Exception):
    pass


class ChangelogFileNotFoundError(ChangelogNotFoundError):
    def __init__(self, file_name):
        self.message = f"Failed to fetch CHANGELOG.md from file '{file_name}'."
        super().__init__(self.message)


class ChangelogBranchNotFoundError(ChangelogNotFoundError):
    def __init__(self, branch_name):
        self.message = f"Failed to fetch CHANGELOG.md from branch '{branch_name}'."
        super().__init__(self.message)


def get_changelog_from_branch(branch_name):
    gitlab = GitLab("https://codebase.helmholtz.cloud", 3268)
    try:
        changelog = gitlab.get_raw_file("CHANGELOG.md", branch_name)
        print(f"Got changelog of branch '{branch_name}'.\n")
        return changelog

    except Exception as e:
        Console.print_error(str(e))
        raise ChangelogBranchNotFoundError(branch_name)


def get_changelog_from_file(file_path):
    try:
        with open(file_path) as f:
            changelog = f.read()
    except FileNotFoundError:
        raise ChangelogNotFoundError(f"File '{file_path}' not found!")

    print(f"Got changelog of file '{file_path}'.\n")
    return changelog
