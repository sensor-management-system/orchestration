#!/bin/bash

# SPDX-FileCopyrightText: 2025
# - Maximilian Schaldach <maximilian.schaldach@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

# This script checks two aspects of the current CHANGELOG.md file:
# - Ensure the CHANGELOG.md file was modified on the current branch (meaning a changelog entry was added).
# - Ensure the CHANGELOG.md file of the current branch is NOT behind CHANGELOG.md on main,
#   ensuring the file on main does not contain any changes (new release note entries) that have not been merged
#   into the current branch yet:
#
#     current branch   _________________________________________
#                     /          ^ invalid      /    ^ valid
#     main __________/_________________________/________________
#                           /
#     another branch   ____/

# Define color codes
OK="\033[92m"
WARNING="\033[93m"
FAIL="\033[91m"
ENDC="\033[0m"
BOLD="\033[1m"

# Read branch from env or checked out branch
BRANCH=${CI_COMMIT_REF_NAME:-$(git rev-parse --abbrev-ref HEAD)}
if [ -z "$BRANCH" ]; then
    echo -e "${FAIL}No branch could be determined.${ENDC}"
    exit 1
fi

# Ensure 'origin/main' exists locally
git fetch --no-tags --prune origin main:main || {
    echo -e "${FAIL}Failed to fetch 'main' branch.${ENDC}";
    exit 1;
}
# Ensure the branch to check exists locally
if ! git rev-parse --verify "$BRANCH" &>/dev/null; then
    echo -e "${WARNING}Branch '$BRANCH' not found locally. Fetching...${ENDC}"
    git fetch origin "$BRANCH":"$BRANCH" || {
        echo -e "${FAIL}Failed to fetch branch '$BRANCH'.${ENDC}";
        exit 1;
    }
fi

if [ "$BRANCH" = "main" ]; then
  echo -e "No comparison for branch 'main'."
  exit 0
fi

# Check whether CHANGELOG.md on branch differs from 'main'
echo -en "${BOLD}Checking if CHANGELOG.md was modified on branch '$BRANCH'... ${ENDC}"
if git diff main $BRANCH -- CHANGELOG.md | grep -q .; then
    echo -e "${OK}Looks good!${ENDC}"

    # Now check whether CHANGELOG.md on branch is ahead or equal to 'main'
    echo -en "${BOLD}Checking if CHANGELOG.md is ahead or equal to 'main'... ${ENDC}"
    LAST_CHANGE_MAIN=$(git log -1 --format=%ct main -- CHANGELOG.md)
    LAST_CHANGE_BRANCH=$(git log -1 --format=%ct "$BRANCH" -- CHANGELOG.md)

    if [ "$LAST_CHANGE_MAIN" -gt "$LAST_CHANGE_BRANCH" ]; then
        echo -e "${WARNING}Oh no!${BOLD}\nCHANGELOG.md on '$BRANCH' is behind the version on 'main'.${ENDC}"
        exit 8 # let the pipeline pass with a warning
    else
        echo -e "${OK}Looks good!${BOLD}\nCHANGELOG.md is updated.${ENDC}"
        exit 0
    fi
else
    echo -e "${WARNING}Oh no!${BOLD}\nLooks like no changelog entry has been made so far. Don't forget to add one!${ENDC}"
    exit 8 # let the pipeline pass with a warning
fi
