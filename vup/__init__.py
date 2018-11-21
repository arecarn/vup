import re
import os
import subprocess
import git
import semantic_version

from . import error

BUILD_META_DATA_REGEX = r'\+(?P<BuildMetadataTag>[\dA-Za-z-]+(\.[\dA-Za-z-]*)*)'

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
class VersionFile():
    def __init__(self, filename, is_dry_run=False):
        self.filename = filename
        self.is_dry_run = is_dry_run
        self.version = None
        self._get_version()

    def replace_version(self, new_version):
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
    prerelease_version = version.next_patch()
    prerelease_version.prerelease = ('beta', )
    return prerelease_version


def commit_version_changes(repo, files, old_version, new_version, is_dry_run):
    if not is_dry_run:
        repo.index.add(files)
    commit_message = 'Increment version from {old_version} to {new_version}'
    commit_message = commit_message.format(
        new_version=new_version, old_version=old_version)
    print(commit_message)
    if not is_dry_run:
        repo.index.commit(commit_message)


def tag_version_file_change(repo, version, is_dry_run):
    tag_message = 'Version {version}'.format(version=version)
    if not is_dry_run:
        repo.create_tag(version, message=tag_message)


def run_hook(cmd, is_dry_run):
    print(cmd)
    if not is_dry_run:
        result = subprocess.run(cmd, shell=True)
        if result.stdout:
            print(result.stdout)
        return result.returncode == 0
    return True


def bump(files,
         bump_type='patch',
         prehook=None,
         posthook=None,
         is_dry_run=False):

    try:
        repo = git.Repo('.')
    except git.exc.InvalidGitRepositoryError:
        raise error.VupErrorCurrentDirectoryIsNotAGitRepository('bump')

    # can't use a dirty repo
    if repo.is_dirty():
        raise error.VupErrorRepositoryHasUncommitedChanges('bump')

    version_files = set()
    current_version = None

    for a_file in files:
        if not is_file_in_repo(repo, os.path.abspath(a_file)):
            raise error.VupErrorFileIsNotNotUnderRevisionControl(
                'bump', a_file)
        version_file = VersionFile(a_file, is_dry_run)

        # check that all the versions match
        if current_version:
            if current_version != version_file.version:
                raise error.VupErrorFilesDontHaveMatchingVersions(
                    'bump', files)
        current_version = version_file.version
        version_files.add(version_file)

    if prehook:
        if not run_hook(prehook, is_dry_run):
            raise error.VupErrorPrehookFailed('bump', prehook)

    release_version = get_bumped_version(current_version, bump_type)
    prerelease_version = get_bumped_prerelease_version(release_version)

    if str(release_version) in repo.tags:
        raise error.VupErrorVersionTagAlreadyExists('bump',
                                                    str(release_version))

    for a_file in version_files:
        a_file.replace_version(release_version)
    commit_version_changes(repo, files, current_version, release_version,
                           is_dry_run)
    tag_version_file_change(repo, release_version, is_dry_run)

    for a_file in version_files:
        a_file.replace_version(prerelease_version)
    commit_version_changes(repo, files, release_version, prerelease_version,
                           is_dry_run)
    if posthook:
        if not run_hook(posthook, is_dry_run):
            raise error.VupErrorPosthookFailed('bump', posthook)


def is_file_in_repo(repo, a_file):
    '''
    repo is a gitPython Repo object
    a_file is the full path to the file from the repository root
    returns True if file is found in the repo at the specified path, False
            otherwise
    '''
    relative_file = os.path.relpath(a_file, repo.working_tree_dir)

    pathdir = os.path.dirname(relative_file)
    # Build up reference to desired repo path
    commit_tree = repo.head.commit.tree
    if pathdir != '':
        for path_element in pathdir.split(os.path.sep):
            try:
                commit_tree = commit_tree[path_element]
            except KeyError:
                return False
    return relative_file in commit_tree
