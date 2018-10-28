import re
import os
import semantic_version
import git

REGEX = r'(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patchlevel>\d+)-?(?P<special>\w+)?'


def get_version_from_file(filename):
    with open(filename, 'r') as file:
        filedata = file.read()

    version_from_file = re.search(REGEX, filedata).group(0)
    version = semantic_version.Version(version_from_file)
    return version


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
        assert 'type_to_bump is invalid'
    bumped_version.prerelease = None
    return bumped_version


def get_bumped_prerelease_version(version):
    prerelease_version = version.next_patch()
    prerelease_version.prerelease = ('beta',)
    return prerelease_version


def replace_version_in_file(filename, old_version, new_version):
    filedata_to_write = re.sub(REGEX,
                               str(new_version),
                               str(old_version),
                               count=1)

    with open(filename, 'w') as file:
        file.write(filedata_to_write)


def commit_version_file_change(repo, filename, old_version, new_version):
    repo.index.add([filename])
    commit_message = 'Increment version from {old_version} to {new_version}'
    commit_message = commit_message.format(new_version=new_version,
                                           old_version=old_version)
    print(commit_message)
    repo.index.commit(commit_message)


def tag_version_file_change(repo, version):
    tag_message = 'Version {version}'.format(version=version)
    repo.create_tag(version, message=tag_message)


def bump(filename, type_to_bump='patch'):
    repo = git.Repo('.')

    # can't use a dirty repo
    assert not repo.is_dirty()

    # can't use a file outsize of the repo (TODO need a test for this)
    assert not file_in_repo(repo, filename)

    version = get_version_from_file(filename)
    release_version = get_bumped_version(version, type_to_bump)
    replace_version_in_file(filename, version, release_version)
    prerelease_version = get_bumped_prerelease_version(release_version)

    commit_version_file_change(repo, filename, version, release_version)
    tag_version_file_change(repo, version)

    replace_version_in_file(filename, release_version, prerelease_version)
    commit_version_file_change(repo,
                               filename,
                               release_version,
                               prerelease_version)


def file_in_repo(repo, a_file):
    '''
    repo is a gitPython Repo object
    a_file is the full path to the file from the repository root
    returns True if file is found in the repo at the specified path, False
            otherwise
    '''
    file_path = os.path.dirname(a_file)
    # Build up reference to desired repo path
    rsub = repo.head.commit.tree
    for path_element in file_path.split(os.path.sep):
        # If dir on file path is not in repo, neither is file.
        try:
            rsub = rsub[path_element]
        except KeyError:
            return False
    return a_file in rsub
