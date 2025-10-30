#!/bin/sh
# SPDX-FileCopyrightText: 2020 - 2024
# - Tobias Kuhnert <tobias.kuhnert@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

search_dir="/usr/share/nginx/html/"

environmentPlaceholders="
NUXT_ENV_OIDC_REFRESH_TOKEN_ENV_PLACEHOLDER
NUXT_ENV_OIDC_REFRESH_EXPIRE_ENV_PLACEHOLDER
NUXT_ENV_OIDC_RESPONSE_TYPE_ENV_PLACEHOLDER
NUXT_ENV_OIDC_GRANT_TYPE_ENV_PLACEHOLDER
NUXT_ENV_CLIENT_ID_ENV_PLACEHOLDER
NUXT_ENV_SCOPE_ENV_PLACEHOLDER
NUXT_ENV_OIDC_CHALLANGE_ENV_PLACEHOLDER
NUXT_ENV_OIDC_WELL_KNOWN_ENV_PLACEHOLDER
NUXT_ENV_OIDC_REFRESH_INTERVAL_TIME_ENV_PLACEHOLDER
NUXT_ENV_MATOMO_SITE_ID_ENV_PLACEHOLDER
NUXT_ENV_MATOMO_URL_ENV_PLACEHOLDER
NUXT_ENV_MATOMO_TRACKER_URL_ENV_PLACEHOLDER
NUXT_ENV_MATOMO_SCRIPT_URL_ENV_PLACEHOLDER
BASE_URL_ENV_PLACEHOLDER
SMS_BACKEND_URL_ENV_PLACEHOLDER
SMS_FRONTEND_URL_ENV_PLACEHOLDER
CV_BACKEND_URL_ENV_PLACEHOLDER
IDL_SYNC_URL_ENV_PLACEHOLDER
INSTITUTE_ENV_PLACEHOLDER
NUXT_ENV_PID_BASE_URL_ENV_PLACEHOLDER
NUXT_ENV_ALLOWED_MIMETYPES_ENV_PLACEHOLDER
SHOW_RELEASE_NOTES_ENV_PLACEHOLDER
NUXT_ENV_MAINTENANCE_DOCUMENT_URL_PLACEHOLDER
"

replaceValue()
{
  passedPlaceholder=$1
  value=$(printenv $passedPlaceholder)

  # $@ contains all arguments passed to a function
  # shift removes the first argument passed to the function
  # the remaining arguments are the paths to the files
  shift

  passedFiles=$@

  echo "placeholder: $passedPlaceholder | value: $value"
  sed -i "s|\b$passedPlaceholder\b|${value:-}|g" $passedFiles
}

findFilesByExtensionAndReplacePlaceholders()
{
  fileExtension=$1
  files=$(find "$search_dir" -type f -name "$fileExtension")

  if [ -n "$files" ]; then
    echo "Replacing files with extention: $fileExtension"
    for placeholder in $environmentPlaceholders; do
     replaceValue $placeholder $files
    done
  else
    echo "No files found with extension: $fileExtension"
  fi
}

removeEmptyScriptTags()
{
    # this function is needed to replace the empty script tag of the matomo module in the index.html if no matomo url was passed
    fileExtension=$1
    files=$(find "$search_dir" -type f -name "$fileExtension")

    if [ -n "$files" ]; then
      echo "Replacing empty script tags"
      sed -i 's|<script[^>]*src=""[^>]*></script>||g' $files
    else
      echo "No files found with extension: $fileExtension to replace empty script tags"
    fi
}

findFilesByExtensionAndReplacePlaceholders "*.js"
findFilesByExtensionAndReplacePlaceholders "*.html"
findFilesByExtensionAndReplacePlaceholders "*.json"
removeEmptyScriptTags "*.html"

exec "$@"
