#!/bin/bash

# SPDX-FileCopyrightText: 2021
# - Wilhelm Becker <wilhelm.becker@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0


# Web backend of the Sensor Management System software developed within
# the Helmholtz DataHub Initiative by GFZ and UFZ.
#
# Copyright (C) 2020
# - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
# - Helmholtz Centre Potsdam - GFZ German Research Centre for
#   Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# Parts of this program were developed within the context of the
# following publicly funded projects or measures:
# - Helmholtz Earth and Environment DataHub
#   (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
#
# Licensed under the HEESIL, Version 1.0 or - as soon they will be
# approved by the "Community" - subsequent versions of the HEESIL
# (the "Licence").
#
# You may not use this work except in compliance with the Licence.
#
# You may obtain a copy of the Licence at:
# https://gitext.gfz-potsdam.de/software/heesil
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the Licence is distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the Licence for the specific language governing
# permissions and limitations under the Licence.

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
