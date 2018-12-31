#!/usr/bin/env python3
"""
The entry point when called as a module
"""

import sys
import argparse
from . import version
from . import bump
from . import error


def create_parser():
    """create the CLI argument parser"""
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
        '--version-file',
        '-f',
        action='append',
        dest='version_files',
        help='file containing version number')
    bump_parser.add_argument('type', help='major, minor, or patch')
    bump_parser.add_argument(
        '--prehook', help='script to run before bumping version')
    bump_parser.add_argument(
        '--posthook', help='script to run after bumping version')
    return parser


SUBCMD_MAP = {
    'bump': bump,
}
PARSER = create_parser()
ARGS = PARSER.parse_args()

if ARGS.subcmd in SUBCMD_MAP:
    try:
        SUBCMD = SUBCMD_MAP[ARGS.subcmd]
        SUBCMD(ARGS.version_files, ARGS.type, ARGS.prehook, ARGS.posthook,
               ARGS.is_dry_run)
    except error.VupError as err:
        print(err, file=sys.stderr)
        sys.exit(1)

else:
    PARSER.print_help()
    sys.exit(1)
