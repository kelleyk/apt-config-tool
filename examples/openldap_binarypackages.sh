#!/usr/bin/env bash

set -e
export DEBIAN_FRONTEND=noninteractive

echo 'Acquire::http::Proxy "http://192.168.0.1:3142";' > /etc/apt/apt.conf.d/80proxy
apt-get update
apt-get install -yq --no-install-recommends wget
apt-get update
apt-get dist-upgrade -yq
apt-get install -yq --no-install-recommends libltdl7 libodbc1 unixodbc libperl5.18 libslp1 sasl2-bin libsasl2-2 libsasl2-modules libsasl2-modules-gssapi-mit
dpkg -i /tmp/packages/libldap-2.4-2_*.deb /tmp/packages/libldap2-dev_*.deb /tmp/packages/slapd_*.deb /tmp/packages/ldap-utils_*.deb
apt-get autoremove -y
apt-get clean
rm -rf /var/lib/apt/lists/*
rm /etc/apt/apt.conf.d/80proxy
