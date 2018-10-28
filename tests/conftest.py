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
    def __init__(self, a_dir, version):
        os.chdir(a_dir)
        self.repo = git.Repo.init(a_dir)
        self.version_file = os.path.join(a_dir, 'version.txt')
        with open(self.version_file, 'a') as a_file:
            a_file.write(version)
        self.repo.index.add([self.version_file])
        self.repo.index.commit("Initial Commit")
        print(self.repo.index.diff(None))
        assert not self.repo.is_dirty()

    def append_to_version_file(self, a_str):
        with open(self.version_file, 'a') as a_file:
            a_file.write(a_str)


@pytest.fixture(params=VERSIONS)
def a_repo(request, tmpdir):
    """
    Create a file
    """
    return TestRepo(tmpdir, request.param).version_file

@pytest.fixture(params=VERSIONS)
def a_dirty_repo(request, tmpdir):
    test_repo = TestRepo(tmpdir, request.param)
    test_repo.append_to_version_file("\ndirt")
    return test_repo.version_file
