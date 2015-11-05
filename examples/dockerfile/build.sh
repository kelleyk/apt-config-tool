#!/usr/bin/env bash
set -e

IMAGE_TAG="changeme"

apt-config-tool image/apt-config.yaml image/apt-config.sh
docker build -t "${IMAGE_TAG}" "$@" image/
