"""
Contains the fixtures used by the tests
"""

import os
import pytest
import git

class TestRepo():
    def __init__(self, a_dir, do_inital_commit=True):
        self.dir = str(a_dir)
        self.repo = git.Repo.init(self.dir)
        self.do_inital_commit = do_inital_commit

    def init(self, version):
        self.version_file = os.path.join(self.dir, 'version.txt')
        os.chdir(self.dir)

        with open(self.version_file, 'a') as a_file:
            a_file.write(version)

        if self.do_inital_commit:
            self.repo.index.add([self.version_file])
            self.repo.index.commit("Initial Commit")


    def append_to_version_file(self, a_str):
        with open(self.version_file, 'a') as a_file:
            a_file.write(a_str)


@pytest.fixture()
def a_repo(tmpdir):
    """
    Create a file
    """
    test_repo = TestRepo(tmpdir)
    return test_repo

@pytest.fixture()
def a_repo_without_version_file_commited(tmpdir):
    test_repo = TestRepo(tmpdir, do_inital_commit=False)
    return test_repo
