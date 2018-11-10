import re
import os
import git
import semantic_version
import subprocess

REGEX = r'(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patchlevel>\d+)-?(?P<special>\w+)?'


class VersionFile():
    def __init__(self, filename):
        self.filename = filename
        self.version = None
        self._get_version()

    def replace_version(self, new_version):
        filedata_to_write = re.sub(
            REGEX, str(new_version), self.filedata, count=1)
        with open(self.filename, 'w') as a_file:
            a_file.write(filedata_to_write)
        self._get_version()

    def _get_version(self):
        # TODO assert file has a version number
        # TODO assert regex only is only found once in a file
        with open(self.filename, 'r') as a_file:
            self.filedata = a_file.read()
        found_version = re.search(REGEX, self.filedata).group(0)
        self.version = semantic_version.Version(found_version)


def get_bumped_version(version, type_to_bump):
    bumped_version = None
    if type_to_bump == 'major':
        bumped_version = version.next_major()
    elif type_to_bump == 'minor':
        bumped_version = version.next_minor()
    elif type_to_bump == 'patch':
        if not version.prerelease:
            bumped_version = version.next_patch()
    else:
        assert False  # 'type_to_bump is invalid'
    bumped_version.prerelease = None
    return bumped_version


def get_bumped_prerelease_version(version):
    prerelease_version = version.next_patch()
    prerelease_version.prerelease = ('beta', )
    return prerelease_version


def commit_version_file_change(repo, filename, old_version, new_version):
    repo.index.add([filename])
    commit_message = 'Increment version from {old_version} to {new_version}'
    commit_message = commit_message.format(
        new_version=new_version, old_version=old_version)
    print(commit_message)
    repo.index.commit(commit_message)


def tag_version_file_change(repo, version):
    tag_message = 'Version {version}'.format(version=version)
    repo.create_tag(version, message=tag_message)


def run_hook(cmd):
    result = subprocess.run(cmd, shell=True)
    if result.stdout:
        print(result.stdout)
    return result.returncode == 0


def bump(filename,
         type_to_bump='patch',
         pre_bump_hook=None,
         post_bump_hook=None):

    # TODO handle exceptions if git repo doesn't exist / has issues
    repo = git.Repo('.')

    # can't use a dirty repo
    assert not repo.is_dirty()

    # can't use a file outside of the repo (TODO need a test for this)
    assert is_file_in_repo(repo, os.path.abspath(filename))


    if pre_bump_hook:
        assert run_hook(pre_bump_hook)  # pre_bump hook failed

    version_file = VersionFile(filename)

    starting_version = version_file.version
    release_version = get_bumped_version(version_file.version, type_to_bump)
    prerelease_version = get_bumped_prerelease_version(release_version)

    # TODO test tag already exists
    assert str(release_version) not in repo.tags

    version_file.replace_version(release_version)
    commit_version_file_change(repo, filename, starting_version,
                               release_version)
    tag_version_file_change(repo, version_file.version)

    version_file.replace_version(prerelease_version)
    commit_version_file_change(repo, filename, release_version,
                               prerelease_version)
    if post_bump_hook:
        assert run_hook(post_bump_hook)  # pre_bump hook failed


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
