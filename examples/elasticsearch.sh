#!/usr/bin/env bash

set -e
export DEBIAN_FRONTEND=noninteractive

echo 'Acquire::http::Proxy "http://192.168.0.1:3142";' > /etc/apt/apt.conf.d/80proxy
apt-get update
apt-get install -yq --no-install-recommends wget
wget -qO - http://packages.elasticsearch.org/GPG-KEY-elasticsearch | apt-key add -
echo 'deb http://packages.elasticsearch.org/elasticsearch/1.4/debian stable main' >> /etc/apt/sources.list.d/elasticsearch.list
echo 'deb http://packages.elasticsearch.org/logstash/1.4/debian stable main' >> /etc/apt/sources.list.d/elasticsearch.list
apt-get update
apt-get dist-upgrade -yq
apt-get install -yq --no-install-recommends elasticsearch openjdk-7-jre-headless
apt-get autoremove -y
apt-get clean
rm -rf /var/lib/apt/lists/*
rm /etc/apt/apt.conf.d/80proxy
