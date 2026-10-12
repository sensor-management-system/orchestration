#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2021 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""This is a script to make backups of the minio server from within the gitlab CI."""

import io
import os
import logging
import xml.etree.ElementTree as ET

import boto3
import botocore.exceptions
import requests

logger = logging.getLogger(__name__)


def main():
    """Query the minio storage and send it to an external (backuped) s3 storage."""
    MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", "sms-attachments")
    S3_EXTERNAL_BACKUP_ACCESS_KEY = os.getenv("S3_EXTERNAL_BACKUP_ACCESS_KEY")
    S3_EXTERNAL_BACKUP_SECRET_KEY = os.getenv("S3_EXTERNAL_BACKUP_SECRET_KEY")
    S3_EXTERNAL_BACKUP_BUCKET_NAME = os.getenv("S3_EXTERNAL_BACKUP_BUCKET_NAME")

    s3_source_response = requests.get(url=f"http://minio:9000/{MINIO_BUCKET_NAME}")
    tree = ET.ElementTree(ET.fromstring(s3_source_response.text))
    root = tree.getroot()
    contents = root.findall("{http://s3.amazonaws.com/doc/2006-03-01/}Contents")

    s3_target = boto3.client(
        "s3",
        endpoint_url="https://s3.gfz.de:443",
        aws_access_key_id=S3_EXTERNAL_BACKUP_ACCESS_KEY,
        aws_secret_access_key=S3_EXTERNAL_BACKUP_SECRET_KEY,
    )

    keys_not_uploaded = set()
    keys_uploaded = set()
    number_of_keys = len(contents)
    for nr, content in enumerate(contents, 1):
        print(f"Upload {nr}/{number_of_keys}...")
        key = content.find("{http://s3.amazonaws.com/doc/2006-03-01/}Key").text
        url_to_access = f"http://minio:9000/{MINIO_BUCKET_NAME}/{key}"
        resp_content = requests.get(url_to_access)
        metadata = {}
        for header in ["x-amz-meta-uploaded-by-id"]:
            header_value = resp_content.headers.get(header)
            if header_value:
                metadata[header.replace("x-amz-meta-", "")] = header_value
        try:
            s3_target.upload_fileobj(
                io.BytesIO(resp_content.content),
                S3_EXTERNAL_BACKUP_BUCKET_NAME,
                key,
                ExtraArgs={"Metadata": metadata},
            )
            keys_uploaded.add(key)
        except botocore.exceptions.ClientError as err:
            logger.exception(err)
            keys_not_uploaded.add(key)
    # If the key itself couldn't be transferred, we might have the situation
    # that we still transferred the file.
    # Usually we design the format in a way that the the key consists of
    # a checksum (md5), a slash, and a filename.
    md5sums_uploaded = set()
    for key in keys_uploaded:
        md5sum = key.split("/", 1)[0]
        md5sums_uploaded.add(md5sum)
    missing_keys = set()
    for key in keys_not_uploaded:
        md5sum = key.split("/", 1)[0]
        if md5sum not in md5sums_uploaded:
            missing_keys.add(key)
    if missing_keys:
        raise Exception(f"Failed to sync the keys: {missing_keys}")


if __name__ == "__main__":
    main()
