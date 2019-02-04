"""
All the exceptions and their messages used by the program
"""

ERROR_HEAD = 'vup {subcmd} error: '


class VupError(Exception):
    """Base Vup Exception.
    Using a base exception will ensure internally generated exceptions will be
    caught and unexpected and unhandled exceptions won't be silenced.
    """


class VupErrorBumpTypeIsInvalid(VupError):
    """Thrown when the bump type specified is not valid"""

    def __init__(self, subcmd):
        msg = ERROR_HEAD + "bump type is invalid"
        msg = msg.format(subcmd=subcmd)
        super().__init__(msg)


class VupErrorRepositoryHasUncommitedChanges(VupError):
    """Thrown when the current repository has uncommited changes that should
    not be considered for any release.
    """

    def __init__(self, subcmd):
        msg = ERROR_HEAD + "repository has uncommited changes"
        msg = msg.format(subcmd=subcmd)
        super().__init__(msg)


class VupErrorNoVersionFilesProvided(VupError):
    """Thrown when no version files have been specified"""

    def __init__(self, subcmd):
        msg = ERROR_HEAD + "no version files provided"
        msg = msg.format(subcmd=subcmd)
        super().__init__(msg)


class VupErrorVersionFileDoesNotExist(VupError):
    """Thrown when the version file does not exist"""

    def __init__(self, subcmd, a_file):
        msg = ERROR_HEAD + "version file {a_file} does not exist"
        msg = msg.format(subcmd=subcmd, a_file=a_file)
        super().__init__(msg)


class VupErrorFileIsNotNotUnderRevisionControl(VupError):
    """Thrown when the file specified is not under any supported version control"""

    def __init__(self, subcmd, a_file):
        msg = ERROR_HEAD + "{a_file} is not under revision control"
        msg = msg.format(subcmd=subcmd, a_file=a_file)
        super().__init__(msg)


class VupErrorCurrentDirectoryIsNotAGitRepository(VupError):
    """Thrown when the current directory is not a git repository"""

    def __init__(self, subcmd):
        msg = ERROR_HEAD + "the current directory is not a Git repository"
        msg = msg.format(subcmd=subcmd)
        super().__init__(msg)


class VupErrorFileDoesNotHaveAVersionNumber(VupError):
    """Thrown when a file does not contain a valid version number"""

    def __init__(self, subcmd, a_file):
        msg = ERROR_HEAD + "{a_file} does not have a version number"
        msg = msg.format(subcmd=subcmd, a_file=a_file)
        super().__init__(msg)


class VupErrorFileContainsMultipleVersionNumbers(VupError):
    """Thrown when a file contains multiple version numbers"""

    def __init__(self, subcmd, a_file):
        msg = ERROR_HEAD + "{a_file} contains multiple version numbers"
        msg = msg.format(subcmd=subcmd, a_file=a_file)
        super().__init__(msg)


class VupErrorFilesDontHaveMatchingVersions(VupError):
    """Thrown when a files version numbers do not match one another"""

    def __init__(self, subcmd, files):
        msg = ERROR_HEAD + "version numbers in {files} don't match"
        msg = msg.format(subcmd=subcmd, files=files)
        super().__init__(msg)


class VupErrorPrehookFailed(VupError):
    """Thrown when a pre-hook fails"""

    def __init__(self, subcmd, hook):
        msg = ERROR_HEAD + "prehook {hook} failed"
        msg = msg.format(subcmd=subcmd, hook=hook)
        super().__init__(msg)


class VupErrorPosthookFailed(VupError):
    """Thrown when a post-hook fails"""

    def __init__(self, subcmd, hook):
        msg = ERROR_HEAD + "posthook {hook} failed"
        msg = msg.format(subcmd=subcmd, hook=hook)
        super().__init__(msg)


class VupErrorVersionTagAlreadyExists(VupError):
    """Thrown when version tag already exists"""

    def __init__(self, subcmd, tag):
        msg = ERROR_HEAD + "tag version {tag} already exists"
        msg = msg.format(subcmd=subcmd, tag=tag)
        super().__init__(msg)
