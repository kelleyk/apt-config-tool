# apt-config-tool

(c) 2014-2015 Kevin Kelley <kelleyk@kelleyk.net>.  All rights reserved.

This script is made available under a BSD license.  See the LICENSE file for details.

It comes with no warranty express or implied.  If it breaks, you get to keep both pieces.

## Overview

  Set up apt and install packages as part of a scripted provisioning process (such as building a Dockerfile).

## The tool can

  - retrieve signing keys via HTTP or from a keyserver

  - add package repositories, such as those commonly provided by software vendors

  - add PPAs

  - automatically detect and use the host's apt proxy, if any (including one detected via Zeroconf/Avahi, which is what
    the `squid-deb-proxy-client` package does)

  - remove cached packages, indices, and other things that are unnecessary unless you intend to install more packages

  - install binary packages (.deb/.ddeb) before cleaning up apt (see the 'binary_packages' key)

## It works by

  - reading a YAML file (that I tend to call 'apt-config.yaml') describing the above

  - generating a simple shell script (that I tend to call 'apt-config.sh'); you should add this file to your
    `.gitignore` so that, like other build products, it is not committed

  - having you add a couple of boilerplate lines to your Dockerfile that add and execute that script (see below)

## It should, in the future

  - allow packages to be downloaded by URL (and optionally verified by checksum)

  - allow pinning based on version or source

  - allow the user to specify that only explicitly-listed packages should be pulled in from a given source

## Using with Docker

  - See examples/dockerfile/.

## Notes

  - If you want to install more packages, you'll have to `apt-get update`, because all of the
    package lists are removed in the clean-up phase.

## Motivation

  - All of my Dockerfiles were accumulating lines that resembled the scripts that this tool
    generates.

  - This makes it easy to accomplish all of this in one step (and hence create only a single
    intermediate image).
