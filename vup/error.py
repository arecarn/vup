"""
All the exceptions and their messages used by the program
"""

ERROR_HEAD = 'vup {subcmd} error: '

# pylint: disable=missing-docstring


def bump_type_is_invalid(subcmd):
    msg = ERROR_HEAD + "bump type is invalid"
    msg = msg.format(subcmd=subcmd)
    return ValueError(msg)


def repository_has_uncommited_changes(subcmd):
    msg = ERROR_HEAD + "repository has uncommited changes"
    msg = msg.format(subcmd=subcmd)
    return ValueError(msg)


def file_is_not_not_under_revision_control(subcmd, a_file):
    msg = ERROR_HEAD + "{a_file} is not under revision control"
    msg = msg.format(subcmd=subcmd, a_file=a_file)
    return ValueError(msg)


def current_directory_is_not_a_git_repository(subcmd):
    msg = ERROR_HEAD + "the current directory is not a Git repository"
    msg = msg.format(subcmd=subcmd)
    return ValueError(msg)


def file_does_not_have_a_version_number(subcmd, a_file):
    msg = ERROR_HEAD + "{file} does not have a version number"
    msg = msg.format(subcmd=subcmd, a_file=a_file)
    return ValueError(msg)


def file_contains_multiple_version_numbers(subcmd, a_file):
    msg = ERROR_HEAD + "{file} contains multiple version numbers"
    msg = msg.format(subcmd=subcmd, a_file=a_file)
    return ValueError(msg)


def files_dont_have_matching_versions(subcmd, files):
    msg = ERROR_HEAD + "version numbers in {files} don't match"
    msg = msg.format(subcmd=subcmd, files=files)
    return ValueError(msg)


def prehook_failed(subcmd, hook):
    msg = ERROR_HEAD + "prehook {hook} failed"
    msg = msg.format(subcmd=subcmd, hook=hook)
    return ValueError(msg)


def posthook_failed(subcmd, hook):
    msg = ERROR_HEAD + "posthook {hook} failed"
    msg = msg.format(subcmd=subcmd, hook=hook)
    return ValueError(msg)


def version_tag_already_exists(subcmd, tag):
    msg = ERROR_HEAD + "tag version {tag} already exists"
    msg = msg.format(subcmd=subcmd, tag=tag)
    return ValueError(msg)