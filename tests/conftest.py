"""
Contains the fixtures used by the tests
"""

import os
import pytest
import git

# pylint: disable=invalid-name


# pylint: disable=too-few-public-methods
class TestRepo():
    """Creates a repository to use for testing"""

    def __init__(self,
                 a_dir,
                 do_commits=True,
                 do_version_commit=True,
                 do_write_version=True):
        self.dir = str(a_dir)
        self.repo = git.Repo.init(self.dir)
        self.do_commits = do_commits
        self.do_version_commit = do_version_commit
        self.do_write_version = do_write_version
        self.version_files = []
        self.other_file = None

    def init(self, version, version_files=('version.txt', )):
        """

        :param version: version string to initialize the version string to
        :param version_files: version files to add to the repo

        """
        self.other_file = os.path.join(self.dir, 'other.txt')
        with open(self.other_file, 'a') as file_handle:
            file_handle.write('other')

        for a_file in version_files:
            self.version_files.append(os.path.join(self.dir, a_file))
            os.chdir(self.dir)
            with open(a_file, 'a') as file_handle:
                if self.do_write_version:
                    file_handle.write(version)

        if self.do_commits:
            self.repo.index.add([self.other_file])
            self.repo.index.commit("Initial Commit")

        if self.do_version_commit and self.do_commits:
            self.repo.index.add(self.version_files)
            self.repo.index.commit("Version Commit")


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
def repo_with_empty_version_files(tmpdir):
    """Fixture that with a test repository in a temporary directory

    :param tmpdir: temporary directory unique to the test invocation

    """
    test_repo = TestRepo(tmpdir, do_write_version=False)
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
    test_repo = TestRepo(tmpdir, do_commits=False)
    return test_repo


@pytest.fixture()
def dir_without_repo(tmpdir):
    """
    :param tmpdir: temporary directory unique to the test invocation
    """
    no_repo = NoRepo(tmpdir)
    return no_repo
