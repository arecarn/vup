import git
import semantic_version
import re

regex = '(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patchlevel>\d+)-?(?P<special>\w+)?'

def main(filename, version_to_bump='patch'):

    repo = git.Repo('.')
    if repo.is_dirty():
        assert("can't use a dirty repo")

    with open(filename, 'r') as file:
        filedata = file.read()

    version_from_file = re.search(regex, filedata).group(0)
    version = semantic_version.Version(version_from_file)

    if version_to_bump == 'major':
        bumped_version = version.next_major()
    elif version_to_bump == 'minor':
        bumped_version = version.next_minor()
    elif version_to_bump == 'patch':
        bumped_version = version
        bumped_version.prerelease = None
    else:
        assert('version_to_bump is invalid')

    print(bumped_version)

    filedata_to_write = re.sub(regex,
                               str(bumped_version),
                               version_from_file,
                               count=1)

    with open(filename, 'w') as file:
        file.write(filedata_to_write)

    # commit
    repo.index.add([filename])
    commit_message = "Increment version from {old_version} number to {version}".format(version=bumped_version, old_version=version_from_file)
    print(commit_message)
    repo.index.commit(commit_message)

    # create tag
    tag_message = "Version {version}".format(version=bumped_version, old_version=version_from_file)
    repo.create_tag(bumped_version, message=tag_message)

    prerelease_version = bumped_version.next_patch()
    prerelease_version.prerelease = ('beta',)

    filedata_to_write = re.sub(regex,
                               str(prerelease_version),
                               str(bumped_version),
                               count=1)

    with open(filename, 'w') as file:
        file.write(filedata_to_write)

    repo.index.add([filename])
    commit_message = "Increment version from {old_version} number to {version}".format(version=prerelease_version, old_version=bumped_version)
    print(commit_message)
    repo.index.commit(commit_message)

FILENAME = 'version.txt'

if __name__ == '__main__':
    main(FILENAME, version_to_bump='patch')
