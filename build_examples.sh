#!/usr/bin/env bash

set -e

pushd examples
rm *.sh
for CONFIGFILE in *.yaml; do
    apt-config-tool "${CONFIGFILE}" > "${CONFIGFILE%.*}".sh
done
popd
