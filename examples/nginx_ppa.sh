#!/usr/bin/env bash

set -e
export DEBIAN_FRONTEND=noninteractive

echo 'Acquire::http::Proxy "http://192.168.0.1:3142";' > /etc/apt/apt.conf.d/80proxy
apt-get update
apt-get install -yq --no-install-recommends wget
add-apt-repository -y ppa:nginx/stable
apt-get update
apt-get dist-upgrade -yq
apt-get install -yq --no-install-recommends nginx nginx-extras
apt-get autoremove -y
apt-get clean
rm -rf /var/lib/apt/lists/*
rm /etc/apt/apt.conf.d/80proxy
