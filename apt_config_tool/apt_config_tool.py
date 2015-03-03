#!/usr/bin/env python2.7
# -*- mode: python; encoding: utf-8; -*-
from __future__ import division, absolute_import, unicode_literals, print_function
from future_builtins import *

"""apt-config-tool: Set up apt and install packages as part of a scripted provisioning process (such as building a Dockerfile).

(c) 2014-2015 Kevin Kelley <kelleyk@kelleyk.net>.  All rights reserved.
This script is made available under a BSD license.  See the LICENSE file for details.
It comes with no warranty express or implied.  If it breaks, you get to keep both pieces.

"""

# TODOs:
#  - implement keyserver support

import os
import os.path
import re
import sys
import json
import logging
import argparse
import subprocess
from itertools import chain
from pipes import quote as shell_quote  # shlex.quote in Py3

import yaml
from intensional import Re


log = logging.getLogger('apt-config-tool')


def build_parser():
    p = argparse.ArgumentParser()
    # sp = p.add_subparsers(help='command help')
    p.add_argument('-v', '--verbose', action='store_true')

    # p_preprocess = sp.add_parser('preprocess', help='Convert YAML configuration to ready-to-run shell script.')
    p_preprocess = p
    p_preprocess.add_argument('input_file', metavar='apt-config.yaml')
    p_preprocess.add_argument('output_file', metavar='apt-config.sh', nargs='?')
    #p_preprocess.add_argument('--apt-proxy', metavar='proxy url', nargs='?', default=True)  # TODO: Should have a flag to set/disable this.
    p_preprocess.set_defaults(func=cmd_preprocess)

    # p_run = sp.add_parser('run')
    # p_run.add_argument('config_file', metavar='path', nargs='?', default='/opt/apt-config-tool/apt-config.json')
    # p_run.set_defaults(func=cmd_run)

    return p


def parse_apt_config(dump):
    for line in dump.splitlines():
        if line not in Re(r'^([^ ]+) "(.*)";$'):
            raise AssertionError('Horrible parsing code has horribly failed!')
        yield (Re._[1], Re._[2])


def get_apt_config():
    return dict(parse_apt_config(subprocess.check_output(('apt-config', 'dump'))))


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


def cmd_preprocess(args):

    proxy = get_apt_proxy()

    with open(args.input_file, 'r') as f:
        data = f.read(yaml.load(raw_data))

    output = [
        '#!/usr/bin/env bash',
        '',
        'set -e',
        'export DEBIAN_FRONTEND=noninteractive',
        '',
    ]

    if proxy:
        output.append('echo {} > /etc/apt/apt.conf.d/80proxy'.format(shell_quote(
            'Acquire::http::Proxy "{}";'.format(proxy))))

    # TODO: We really only need wget if we're going to have to fetch a key.
    output.append('apt-get update')  # Must update first; otherwise, there are no package lists.
    output.extend(apt_install(('wget',)))

    for key_spec in data.get('keys') or ():
        output.extend(install_key(key_spec))
    for source_name, source_spec in (data.get('sources') or {}).items():
        output.extend(install_source(source_name, source_spec))
    for ppa_spec in data.get('ppas') or ():
        output.extend(install_ppa(ppa_spec))

    output.extend(('apt-get update', 'apt-get dist-upgrade -yq'))

    output.extend(apt_install(data.get('packages') or ()))

    output.extend((
        'apt-get autoremove -y',
        'apt-get clean',
        'rm -rf /var/lib/apt/lists/*',
        ))

    if proxy:
        output.append('rm /etc/apt/apt.conf.d/80proxy')

    output = '\n'.join(output)
    if not args.output_file:
        print(output)
    else:
        skip_write = False
        if os.path.exists(args.output_file):
            with open(args.output_file, 'r') as f:
                existing_output = f.read()
            if existing_output == output:
                print('{}: Output would be unchanged; not modifying the output file!'.format(sys.argv[0]))
                skip_write = True
        if not skip_write:
            with open(args.output_file, 'w') as f:
                f.write(output)


def apt_install(packages):
    return ('apt-get install -yq --no-install-recommends ' + ' '.join(packages),)


# def cmd_run(args):
#     with open(args.config_file, 'r') as f:
#         data = json.loads(f.read())

#     pass


def install_key(key_spec):
    if 'url' in key_spec:
        return ('wget -qO - {} | apt-key add -'.format(shell_quote(key_spec['url'])),)

    elif 'keyid' in key_spec:
        raise NotImplementedError()

    else:
        raise Exception('Not sure what to do with key description: {}'.format(key_spec))


def install_source(source_name, source_spec):
    for key_spec in source_spec['keys']:
        for line in install_key(key_spec):
            yield line

    for line in source_spec['sources']:
        yield 'echo {} >> /etc/apt/sources.list.d/{}.list'.format(shell_quote(line), source_name)


def install_ppa(ppa_spec):
    yield 'add-apt-repository -y ppa:{}'.format(ppa_spec)


def main():
    args = build_parser().parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
        logging.debug('herro')
        #log.setLevel(logging.DEBUG)
    return args.func(args)


if __name__ == '__main__':
    raise SystemExit(main())
