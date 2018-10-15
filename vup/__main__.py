#!/usr/bin/env python3
"""
The entry point when called as a module
"""

from __init__ import bump
import sys
import argparse
import version


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


subcmd_map = {
    'bump': bump,
}

parser = create_parser()
args = parser.parse_args()

try:
    subcmd = subcmd_map[args.subcmd]
    subcmd(args.file, args.type)
except KeyError:
    parser.print_help()
    sys.exit(1)
