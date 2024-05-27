#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Norman Ziegner <norman.ziegner@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

# Create self-signed certificates for testing.
# Requires https://pypi.org/project/zeroc-icecertutils/
# Optional arg: CommonName for certificate

import IceCertUtils
import os
import sys

outputs = [
    "server.p12",
    "server.pem",
    "server.key",
]
if all(os.path.exists(o) for o in outputs):
    print("Certificates already exist, not overwriting")
    sys.exit(2)

try:
    cn = sys.argv[1]
except IndexError:
    cn = "localhost"


# Create the certicate factory
factory = IceCertUtils.CertificateFactory(cn="My CA")

# Get the CA certificate and save as JKS and PEM
ca = factory.getCA()

# Create the server certificate
server = factory.create("server", cn=cn)
# Save as PKCS12 and pem
server.save("server.pem")
server.saveKey("server.key")

factory.destroy()

print("Created certificates")

