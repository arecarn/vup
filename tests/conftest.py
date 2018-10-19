"""
Contains the fixtures used by the tests
"""

import os
import pytest
import git

VERSIONS = [
    '1.2.3-dev',
    '1.2.3',
]


@pytest.fixture(params=VERSIONS)
def a_repo(request, tmpdir):
    """
    Create a file
    """
    repo = git.Repo.init(tmpdir)
    filepath = os.path.join(tmpdir, 'version.txt')
    with open(filepath, 'a') as a_file:
        a_file.write(request.param)
        print(request.param)
        print(tmpdir)
        repo.index.add([filepath])
    repo.index.commit("Initial Commit")
    os.chdir(tmpdir)
    return filepath
