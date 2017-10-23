#!/usr/bin/env python2.7
# -*- mode: python; encoding: utf-8; -*-
from __future__ import division, absolute_import, unicode_literals, print_function
from future_builtins import *

import logging
import subprocess

from intensional import Re


log = logging.getLogger('apt-config-tool')


def parse_apt_config(dump):
    for line in dump.splitlines():
        if line not in Re(r'^([^ ]+) "(.*)";$'):
            raise AssertionError('Horrible parsing code has horribly failed!')
        yield (Re._[1], Re._[2])


def get_apt_config():
    try:
        return dict(parse_apt_config(subprocess.check_output(('apt-config', 'dump'))))
    except OSError as exc:
        if exc.errno == 2:
            return {}
        raise


def get_apt_proxy():
    config = get_apt_config()

    proxy = config.get('Acquire::http::Proxy')
    if proxy:
        log.debug('Using host\'s apt proxy: {}'.format(proxy))
        return proxy

    # You can install squid-deb-proxy-client, which supplies a tiny little script that asks avahi
    # for any zeroconf-advertised apt proxies.
    proxy_autodetect = config.get('Acquire::http::ProxyAutoDetect')
    if proxy_autodetect:
        log.debug('Using host\'s apt proxy autodetection script: {}'.format(proxy_autodetect))
        proxy = subprocess.check_output((proxy_autodetect,)).strip()
    if proxy:
        log.debug('Autodetected apt proxy: {}'.format(proxy))
        return proxy

    log.debug('Couldn\'t find an apt proxy.')
    return None
