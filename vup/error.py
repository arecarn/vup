"""
All the exceptions and their messages used by the program
"""

ERROR_HEAD = 'vup {subcmd} error: '

# pylint: disable=missing-docstring


class VupError(Exception):
    pass


class VupErrorBumpTypeIsInvalid(VupError):
    def __init__(self, subcmd):
        msg = ERROR_HEAD + "bump type is invalid"
        msg = msg.format(subcmd=subcmd)
        super().__init__(msg)


class VupErrorRepositoryHasUncommitedChanges(VupError):
    def __init__(self, subcmd):
        msg = ERROR_HEAD + "repository has uncommited changes"
        msg = msg.format(subcmd=subcmd)
        super().__init__(msg)


class VupErrorFileIsNotNotUnderRevisionControl(VupError):
    def __init__(self, subcmd, a_file):
        msg = ERROR_HEAD + "{a_file} is not under revision control"
        msg = msg.format(subcmd=subcmd, a_file=a_file)
        super().__init__(msg)


class VupErrorCurrentDirectoryIsNotAGitRepository(VupError):
    def __init__(self, subcmd):
        msg = ERROR_HEAD + "the current directory is not a Git repository"
        msg = msg.format(subcmd=subcmd)
        super().__init__(msg)


class VupErrorFileDoesNotHaveAVersionNumber(VupError):
    def __init__(self, subcmd, a_file):
        msg = ERROR_HEAD + "{file} does not have a version number"
        msg = msg.format(subcmd=subcmd, a_file=a_file)
        super().__init__(msg)


class VupErrorFileContainsMultipleVersionNumbers(VupError):
    def __init__(self, subcmd, a_file):
        msg = ERROR_HEAD + "{file} contains multiple version numbers"
        msg = msg.format(subcmd=subcmd, a_file=a_file)
        super().__init__(msg)


class VupErrorFilesDontHaveMatchingVersions(VupError):
    def __init__(self, subcmd, files):
        msg = ERROR_HEAD + "version numbers in {files} don't match"
        msg = msg.format(subcmd=subcmd, files=files)
        super().__init__(msg)


class VupErrorPrehookFailed(VupError):
    def __init__(self, subcmd, hook):
        msg = ERROR_HEAD + "prehook {hook} failed"
        msg = msg.format(subcmd=subcmd, hook=hook)
        super().__init__(msg)


class VupErrorPosthookFailed(VupError):
    def __init__(self, subcmd, hook):
        msg = ERROR_HEAD + "posthook {hook} failed"
        msg = msg.format(subcmd=subcmd, hook=hook)
        super().__init__(msg)


class VupErrorVersionTagAlreadyExists(VupError):
    def __init__(self, subcmd, tag):
        msg = ERROR_HEAD + "tag version {tag} already exists"
        msg = msg.format(subcmd=subcmd, tag=tag)
        super().__init__(msg)
