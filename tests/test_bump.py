import pytest
import vup

DEFAULT_VERSION = '1.2.3-dev'


@pytest.mark.parametrize("versions", [
    DEFAULT_VERSION,
    '1.2.3',
])
def test_bump(a_repo, versions):
    a_repo.init(versions)
    vup.bump(a_repo.version_file, 'major')


def test_dirty_bump(a_repo):
    a_repo.init(DEFAULT_VERSION)
    a_repo.append_to_version_file('modifications')
    with pytest.raises(Exception):
        vup.bump(a_repo.version_file, 'major')


def test_with_a_version_file_that_isnt_under_git(
        a_repo_without_version_file_commited):
    a_repo_without_version_file_commited.init(DEFAULT_VERSION)
    with pytest.raises(Exception):
        vup.bump(a_repo_without_version_file_commited.version_file, 'major')


def test_pre_bump_hook(a_repo):
    a_repo.init(DEFAULT_VERSION)
    vup.bump(a_repo.version_file, 'major', 'echo success')


def test_failed_pre_bump_hook(a_repo):
    a_repo.init(DEFAULT_VERSION)
    with pytest.raises(Exception):
        vup.bump(a_repo.version_file, 'major', 'not_a_real_command')


def test_post_bump_hook(a_repo):
    a_repo.init(DEFAULT_VERSION)
    vup.bump(a_repo.version_file, 'major', post_bump_hook='echo success')


def test_failed_post_bump_hook(a_repo):
    a_repo.init(DEFAULT_VERSION)
    with pytest.raises(Exception):
        vup.bump(
            a_repo.version_file, 'major', post_bump_hook='not_a_real_command')


# TODO test multi line files bump
