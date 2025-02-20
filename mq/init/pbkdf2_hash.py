#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2024
# - Joost Hemmen <joost.hemmen@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

from hashlib import pbkdf2_hmac
from os import urandom
from sys import argv, exit
import base64

if len(argv) > 1:
    password = argv[1]
else:
    print("Usage: hash <password> [digest] [iterations]")
    exit(0)

digest = 'sha512'
iterations = 100000
if len(argv) > 2:
    digest = argv[2]
if len(argv) > 3:
    iterations = int(argv[3])


salt = urandom(16)

pbkdf2_hash = pbkdf2_hmac(
    digest,           # The hash digest algorithm to use
    password.encode(),  # Convert the password to bytes
    salt,               # Provide the salt
    iterations          # It is the number of iterations
)

salt_b64 = base64.b64encode(salt).decode('utf-8')
pbkdf2_hash_b64 = base64.b64encode(pbkdf2_hash).decode('utf-8')

# Combine the components into the desired format
stored_hash = f"PBKDF2${digest}${iterations}${salt_b64}${pbkdf2_hash_b64}"

print(stored_hash)
