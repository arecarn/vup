import vup
import pytest
import os


def test_bump(a_repo):
    os.chdir(a_repo.dir)
    vup.bump(a_repo.version_file, 'major')


def test_dirty_bump(a_dirty_repo):
    os.chdir(a_dirty_repo.dir)
    with pytest.raises(Exception):
        vup.bump(a_dirty_repo.version_file, 'major')


def test_with_a_version_file_that_isnt_under_git(a_repo_without_version_file_commited):
    os.chdir(a_repo_without_version_file_commited.dir)
    with pytest.raises(Exception):
        vup.bump(a_repo_without_version_file_commited.version_file, 'major')
