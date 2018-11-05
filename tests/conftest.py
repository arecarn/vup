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

class TestRepo():
    def __init__(self, a_dir, version, do_inital_commit=True):
        self.dir = str(a_dir)
        self.repo = git.Repo.init(self.dir)
        self.version_file = os.path.join(self.dir, 'version.txt')

        with open(self.version_file, 'a') as a_file:
            a_file.write(version)

        if do_inital_commit:
            self.repo.index.add([self.version_file])
            self.repo.index.commit("Initial Commit")

    def append_to_version_file(self, a_str):
        with open(self.version_file, 'a') as a_file:
            a_file.write(a_str)


@pytest.fixture(params=VERSIONS)
def a_repo(request, tmpdir):
    """
    Create a file
    """
    test_repo = TestRepo(tmpdir, request.param)
    return test_repo


@pytest.fixture(params=VERSIONS)
def a_dirty_repo(request, tmpdir):
    test_repo = TestRepo(tmpdir, request.param)
    test_repo.append_to_version_file("\ndirt")
    return test_repo

@pytest.fixture(params=VERSIONS)
def a_repo_without_version_file_commited(request, tmpdir):
    test_repo = TestRepo(tmpdir, request.param, do_inital_commit=False)
    return test_repo
