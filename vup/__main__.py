import semantic_version
import re

regex = '(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patchlevel>\d+)-?(?P<special>\w+)?'


def main(filename, version_to_bump='patch'):

    # TODO handle file not found
    with open(filename, 'r') as file:
        filedata = file.read()

    version_from_file = re.search(regex, filedata).group(0)
    version = semantic_version.Version(version_from_file)

    if version_to_bump == 'major':
        bumped_version = version.next_major()
    elif version_to_bump == 'minor':
        bumped_version = version.next_minor()
    elif version_to_bump == 'patch':
        bumped_version = version.next_patch()
    else:
        assert('version_to_bump is invalid')

    filedata_to_write = re.sub(regex,
                               str(bumped_version),
                               version_from_file,
                               count=1)

    with open(filename, 'w') as file:
        file.write(filedata_to_write)


FILENAME = 'version.txt'


if __name__ == '__main__':
    main(FILENAME, version_to_bump='minor')
