#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME=final-project:latest
APP_PORT=${FLASK_RUN_PORT:-5000}

docker build -t "${IMAGE_NAME}" .
docker run --rm -p "${APP_PORT}:5000" --env-file .env.example "${IMAGE_NAME}"
