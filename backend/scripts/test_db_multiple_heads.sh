#!/bin/bash

# SPDX-FileCopyrightText: 2021 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

lines=`python3 manage.py db heads | grep -c "head"`
if [ $lines -ne 1 ]
then
    echo "Error: Multiple Migration Heads"
	exit 1
else
	exit 0
fi
