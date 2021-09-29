#!/usr/bin/env bash

# Install essential packages from Apt
apt-get update -y
apt-get install -y  --no-install-recommends gcc libssl-dev libffi-dev musl-dev cargo curl python3-distutils

apt-get clean

pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir -r requirements.txt

echo ""
echo "Successfully installed the requirements."
echo ""