#!/bin/bash

# SPDX-FileCopyrightText: 2021
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

lines=`python3 manage.py db heads | grep -c "head"`
if [ $lines -ne 1 ]
then
    echo "Error: Multiple Migration Heads"
	exit 1
else
	exit 0
fi