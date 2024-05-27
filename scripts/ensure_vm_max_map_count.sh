#!/bin/bash

# SPDX-FileCopyrightText: 2021 - 2024
# - Wilhelm Becker <wilhelm.becker@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

# This script is meant to check the current vm.max_map_count
# setting. It is necessary as elasticsearch may need a higher
# value than the default os setting (even for a proper start).
#
# The script will run and stop in case of a too low setting.
# If the setting is high enough the script just runs and
# returns with a success return value without any text output.

CURRENT_VM_MAX_MAP_COUNT=$(sysctl vm.max_map_count --values)
TARGET_VM_MAX_MAP_COUNT=262144

if [ $CURRENT_VM_MAX_MAP_COUNT -lt $TARGET_VM_MAX_MAP_COUNT ]
then
    echo 'Please check your `sysctl vm.max_map_count`'
    echo "The current value is: $CURRENT_VM_MAX_MAP_COUNT"
    echo "The necessary value is: $TARGET_VM_MAX_MAP_COUNT"
    echo 'You can fix it with the following command:'
    echo ''
    echo "    sudo sysctl vm.max_map_count=$TARGET_VM_MAX_MAP_COUNT"
    echo ''
    echo 'Please fix it before you go on!'
    exit 1
fi
