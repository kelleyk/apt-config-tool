#!/usr/bin/env bash

set -e
export DEBIAN_FRONTEND=noninteractive

echo 'Acquire::http::Proxy "http://192.168.0.1:3142";' > /etc/apt/apt.conf.d/80proxy
apt-get update
apt-get install -yq --no-install-recommends wget
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' >> /etc/apt/sources.list.d/mongodb.list
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv C0A52C50
echo 'deb http://www.ubnt.com/downloads/unifi/debian stable ubiquiti' >> /etc/apt/sources.list.d/unifi.list
apt-get update
apt-get dist-upgrade -yq
apt-get install -yq --no-install-recommends unifi-beta openjdk-7-jre-headless
apt-get autoremove -y
apt-get clean
rm -rf /var/lib/apt/lists/*
rm /etc/apt/apt.conf.d/80proxy
