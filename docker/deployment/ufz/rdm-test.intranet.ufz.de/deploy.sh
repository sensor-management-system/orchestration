#!/usr/bin/env sh
cd "$(dirname "$0")"
docker-compose pull && docker-compose up -d
