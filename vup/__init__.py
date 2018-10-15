import git
import semantic_version
import re

regex = '(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patchlevel>\d+)-?(?P<special>\w+)?'


def get_version_from_file(filename):
    with open(filename, 'r') as file:
        filedata = file.read()

    version_from_file = re.search(regex, filedata).group(0)
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
        assert('type_to_bump is invalid')
    bumped_version.prerelease = None
    return bumped_version


def get_bumped_prerelease_version(version):
    prerelease_version = version.next_patch()
    prerelease_version.prerelease = ('beta',)
    return prerelease_version


def replace_version_in_file(filename, old_version, new_version):
    filedata_to_write = re.sub(regex,
                               str(new_version),
                               str(old_version),
                               count=1)

    with open(filename, 'w') as file:
        file.write(filedata_to_write)


def commit_version_file_change(repo, filename, old_version, new_version):
    repo.index.add([filename])
    commit_message = "Increment version from {old_version} to {new_version}"
    commit_message = commit_message.format(new_version=new_version,
                                           old_version=old_version)
    print(commit_message)
    repo.index.commit(commit_message)


def tag_version_file_change(repo, filename, version):
    tag_message = "Version {version}".format(version=version)
    repo.create_tag(version, message=tag_message)


def bump(filename, type_to_bump='patch'):
    repo = git.Repo('.')
    if repo.is_dirty():
        assert("can't use a dirty repo")

    version = get_version_from_file(filename)
    release_version = get_bumped_version(version, type_to_bump)
    replace_version_in_file(filename, version, release_version)
    prerelease_version = get_bumped_prerelease_version(release_version)

    commit_version_file_change(repo, filename, version, release_version)
    tag_version_file_change(repo, filename, version)

    replace_version_in_file(filename, release_version, prerelease_version)
    commit_version_file_change(repo,
                               filename,
                               release_version,
                               prerelease_version)
