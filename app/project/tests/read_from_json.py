# SPDX-FileCopyrightText: 2020
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

import json


def extract_data_from_json_file(path_to_file, type_name):
    with open(path_to_file) as json_file:
        data = json.load(json_file)
    return data[type_name]
