"""
Contains the fixtures used by the tests
"""

import os
import pytest
import git

# pylint: disable=invalid-name


class TestRepo():
    """Creates a repository to use for testing"""

    def __init__(self, a_dir, do_inital_commit=True, do_version_commit=True):
        self.dir = str(a_dir)
        self.repo = git.Repo.init(self.dir)
        self.do_inital_commit = do_inital_commit
        self.do_version_commit = do_version_commit
        self.version_file = None
        self.other_file = None

    def init(self, version):
        """

        :param version: version string to initialize the version string to

        """
        self.version_file = os.path.join(self.dir, 'version.txt')
        self.other_file = os.path.join(self.dir, 'other.txt')
        os.chdir(self.dir)

        with open(self.version_file, 'a') as a_file:
            a_file.write(version)

        with open(self.other_file, 'a') as a_file:
            a_file.write('other')

        if self.do_inital_commit:
            self.repo.index.add([self.other_file])
            self.repo.index.commit("Initial Commit")

            if self.do_version_commit:
                self.repo.index.add([self.version_file])
                self.repo.index.commit("Version Commit")

    def append_to_version_file(self, a_str):
        """

        :param a_str: a string to append to the version file

        """
        with open(self.version_file, 'a') as a_file:
            a_file.write(a_str)


# pylint: disable=too-few-public-methods
class NoRepo():
    def __init__(self, a_dir):
        self.dir = str(a_dir)
        self.version_file = None

    def init(self, version):
        os.chdir(self.dir)
        self.version_file = os.path.join(self.dir, 'version.txt')
        with open(self.version_file, 'a') as a_file:
            a_file.write(version)


@pytest.fixture()
def a_repo(tmpdir):
    """Fixture that with a test repository in a temporary directory

    :param tmpdir: temporary directory unique to the test invocation

    """
    test_repo = TestRepo(tmpdir)
    return test_repo


@pytest.fixture()
def repo_without_version_file_commited(tmpdir):
    """

    :param tmpdir: temporary directory unique to the test invocation

    """
    test_repo = TestRepo(tmpdir, do_version_commit=False)
    return test_repo


@pytest.fixture()
def repo_without_commits(tmpdir):
    """

    :param tmpdir: temporary directory unique to the test invocation

    """
    test_repo = TestRepo(tmpdir, do_inital_commit=False)
    return test_repo


@pytest.fixture()
def dir_without_repo(tmpdir):
    """
    :param tmpdir: temporary directory unique to the test invocation
    """
    no_repo = NoRepo(tmpdir)
    return no_repo
