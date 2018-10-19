#!/usr/bin/env python3
"""
The entry point when called as a module
"""

import sys
import argparse
from . import version
from . import bump


def create_parser():
    """
    create the CLI argument parser
    """
    parser = argparse.ArgumentParser(prog='vup')

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {version}'.format(version=version.__version__))

    parser.add_argument(
        '--dry-run',
        dest='is_dry_run',
        action='store_true',
        help='show what would be done without doing it')

    sub_parsers = parser.add_subparsers(dest="subcmd")

    bump_parser = sub_parsers.add_parser('bump')
    bump_parser.add_argument(
        'file', help='file containing version number')
    bump_parser.add_argument(
        'type', help='major, minor, or patch')
    return parser


SUBCMD_MAP = {
    'bump': bump,
}

PARSER = create_parser()
ARGS = PARSER.parse_args()

try:
    SUBCMD = SUBCMD_MAP[ARGS.subcmd]
    SUBCMD(ARGS.file, ARGS.type)
except KeyError:
    PARSER.print_help()
    sys.exit(1)
