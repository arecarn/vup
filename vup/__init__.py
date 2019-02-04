import re
import os
import subprocess
import git
import semantic_version
import yaml

from . import error

BUILD_META_DATA_REGEX = r'\+(?P<BuildMetadataTag>[\dA-Za-z-]+(\.[\dA-Za-z-]*)*)'

# TODO add tests for this regex
REGEX = (
    r'(?P<Major>0|[1-9]\d*)\.'
    r'(?P<Minor>0|[1-9]\d*)\.'
    r'(?P<Patch>0|[1-9]\d*)'
    r'(?P<PreReleaseTagWithSeparator>'
    r'-(?P<PreReleaseTag>'
    r'((0|[1-9]\d*|\d*[A-Z-a-z-][\dA-Za-z-]*))(\.(0|[1-9]\d*|\d*[A-Za-z-][\dA-Za-z-]*))*'
    r')'
    r')?'
    r'(?P<BuildMetadataTagWithSeparator>' + BUILD_META_DATA_REGEX + r')?')


# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
class Config():
    """Opens and reads the YAML config file"""

    def __init__(self, version_files, bump_type, prehook, posthook,
                 is_dry_run):

        self.version_files = version_files
        self.prehook = prehook
        self.posthook = posthook

        self.bump_type = bump_type
        self.is_dry_run = is_dry_run

        try:
            with open('.vup.yaml') as yaml_file:
                self.yaml_config = yaml.safe_load(yaml_file)

                if not self.version_files:
                    self.version_files = self.yaml_config.get(
                        'version_files', [])
                if not self.prehook:
                    self.prehook = self.yaml_config.get('prehook', None)
                if not self.posthook:
                    self.posthook = self.yaml_config.get('posthook', None)

        # TODO handle the case where version files is empty
        # TODO handle permission error permission
        except FileNotFoundError:
            pass


# pylint: disable=too-few-public-methods
class VersionFile():
    """Maintains the state of the version file"""

    def __init__(self, filename, is_dry_run=False):
        self.filename = filename
        self.is_dry_run = is_dry_run
        self.version = None
        self._get_version()

    def replace_version(self, new_version):
        """Replace the version in the file with a different version

        :param new_version: new version to update the version in the file to

        """
        filedata_to_write = re.sub(
            REGEX, str(new_version), self.filedata, count=1)
        if not self.is_dry_run:
            with open(self.filename, 'w') as a_file:
                a_file.write(filedata_to_write)
        self._get_version()

    def _get_version(self):
        with open(self.filename, 'r') as a_file:
            self.filedata = a_file.read()
        found_versions = list(re.finditer(REGEX, self.filedata))
        if not found_versions:
            raise error.VupErrorFileDoesNotHaveAVersionNumber(
                'bump', self.filename)
        if len(found_versions) != 1:
            raise error.VupErrorFileContainsMultipleVersionNumbers(
                'bump', self.filename)
        self.version = semantic_version.Version(found_versions[0][0])


def get_bumped_version(version, bump_type):
    """Return a new version number based on the bump type.

    :param version: inital version to be bumped
    :param bump_type: The type of bump either 'major', 'minor', 'patch'

    """
    bumped_version = None
    if bump_type == 'major':
        bumped_version = version.next_major()
    elif bump_type == 'minor':
        bumped_version = version.next_minor()
    elif bump_type == 'patch':
        if not version.prerelease:
            bumped_version = version.next_patch()
    else:
        raise error.VupErrorBumpTypeIsInvalid('bump')
    bumped_version.prerelease = None
    return bumped_version


def get_bumped_prerelease_version(version):
    """Return the pre-release version of the specified version.

    :param version: version to get the pre-release version of

    """
    prerelease_version = version.next_patch()
    prerelease_version.prerelease = ('beta', )
    return prerelease_version


def _get_repo():
    """Return the repo of the current directory.


    :raises VupErrorCurrentDirectoryIsNotAGitRepository: when the current
        directory is not a git repository
    :raises VupErrorRepositoryHasUncommitedChanges: when the repository has
        uncommited changes

    """
    try:
        repo = git.Repo('.')
    except git.exc.InvalidGitRepositoryError:
        raise error.VupErrorCurrentDirectoryIsNotAGitRepository('bump')
    if repo.is_dirty():
        raise error.VupErrorRepositoryHasUncommitedChanges('bump')
    return repo


def commit_version_changes(repo, files, old_version, new_version, is_dry_run):
    """Add and commits changes to a version file.

    This function assumes changes have already been made to the version file.

    :param repo: The repo to commit to
    :param files: files to commit
    :param old_version: the old version before it was modified
    :param new_version: the new version after it was modified
    :param is_dry_run: if this function will actually make changes or just print
        what it would do

    """
    if not is_dry_run:
        repo.index.add(files)
    commit_message = 'Increment version from {old_version} to {new_version}'
    commit_message = commit_message.format(
        new_version=new_version, old_version=old_version)
    print(commit_message)
    if not is_dry_run:
        repo.index.commit(commit_message)


def tag_version_file_change(repo, version, is_dry_run):
    """

    :param repo: The repo to add the tag to
    :param version: the version to use as the tag name
    :param is_dry_run: if this function will actually make changes or just print
    what it would do

    """
    tag_message = 'Version {version}'.format(version=version)
    if not is_dry_run:
        repo.create_tag(version, message=tag_message)


def run_hook(cmd, is_dry_run):
    """

    :param cmd: The command line command to run
    :param is_dry_run: if this function will actually make changes or just print
    what it would do

    """
    print(cmd)
    if not is_dry_run:
        result = subprocess.run(cmd, shell=True)
        if result.stdout:
            print(result.stdout)
        return result.returncode == 0
    return True


# pylint: disable=too-many-branches
def bump(version_files,
         bump_type='patch',
         prehook=None,
         posthook=None,
         is_dry_run=False):
    """
    :param version_files: The version files to bump
    :param bump_type: The type of bump either 'major', 'minor', 'patch' (Default
        value = 'patch')
    :param prehook: the command to run before bumping. If this command fails the
        bump will not be processed (Default value = None)
    :param posthook: the command to run after bumping. (Default value = None)
    :param is_dry_run: if this function will actually make changes or just print
    what it would do (Default value = False)

    """

    # TODO Validate bump_type

    if not version_files:
        raise error.VupErrorNoVersionFilesProvided('bump')

    config = Config(version_files, bump_type, prehook, posthook, is_dry_run)

    repo = _get_repo()

    version_file_set = set()
    current_version = None

    for a_file in config.version_files:
        if not os.path.isfile(a_file):
            raise error.VupErrorVersionFileDoesNotExist('bump', a_file)

        if not is_file_in_repo(repo, os.path.abspath(a_file)):
            raise error.VupErrorFileIsNotNotUnderRevisionControl(
                'bump', a_file)
        version_file = VersionFile(a_file, is_dry_run)

        # check that all the versions match
        if current_version:
            if current_version != version_file.version:
                raise error.VupErrorFilesDontHaveMatchingVersions(
                    'bump', config.version_files)
        current_version = version_file.version
        version_file_set.add(version_file)

    if config.prehook:
        if not run_hook(config.prehook, is_dry_run):
            raise error.VupErrorPrehookFailed('bump', config.prehook)

    release_version = get_bumped_version(current_version, bump_type)
    prerelease_version = get_bumped_prerelease_version(release_version)

    if str(release_version) in repo.tags:
        raise error.VupErrorVersionTagAlreadyExists('bump',
                                                    str(release_version))

    for a_file in version_file_set:
        a_file.replace_version(release_version)
    commit_version_changes(repo, config.version_files, current_version,
                           release_version, is_dry_run)
    tag_version_file_change(repo, release_version, is_dry_run)

    for a_file in version_file_set:
        a_file.replace_version(prerelease_version)
    commit_version_changes(repo, config.version_files, release_version,
                           prerelease_version, is_dry_run)
    if config.posthook:
        if not run_hook(config.posthook, is_dry_run):
            raise error.VupErrorPosthookFailed('bump', config.posthook)


def is_file_in_repo(repo, a_file):
    """repo is a git Python Repo object
    a_file is the full path to the file from the repository root
    returns True if file is found in the repo at the specified path, False
            otherwise

    :param repo: The repo to use in the check
    :param a_file: the file to check

    """
    relative_file = os.path.relpath(a_file, repo.working_tree_dir)

    pathdir = os.path.dirname(relative_file)
    # Build up reference to desired repo path
    try:
        commit_tree = repo.head.commit.tree
    except ValueError:  # occurs when there are no commits in a repository
        return False

    if pathdir != '':
        for path_element in pathdir.split(os.path.sep):
            try:
                commit_tree = commit_tree[path_element]
            except KeyError:
                return False
    return relative_file in commit_tree
