import pytest
import vup.error
import vup

# pylint: disable=invalid-name

DEFAULT_INPUT_VERSION = '1.2.3-beta'
DEFAULT_OUTPUT_VERSION_MAJOR = '2.0.1-beta'
DEFAULT_OUTPUT_VERSION_MINOR = '1.3.1-beta'
DEFAULT_OUTPUT_VERSION_PATCH = '1.2.4-beta'


@pytest.mark.parametrize(
    "input_version,output_version",
    [(DEFAULT_INPUT_VERSION, DEFAULT_OUTPUT_VERSION_MAJOR),
     ('1.2.3', '2.0.1-beta')])
def test_bump(a_repo, input_version, output_version):
    """

    :param a_repo: repository fixture to test with
    :param input_version: starting version
    :param output_version: version after bump

    """
    a_repo.init(input_version)
    vup.bump([a_repo.version_file], 'major')

    version_file = vup.VersionFile(a_repo.version_file)
    assert str(version_file.version) == output_version


def test_dirty_bump(a_repo):
    """

    :param a_repo: fixture of a test repository

    """
    a_repo.init(DEFAULT_INPUT_VERSION)
    a_repo.append_to_version_file('modifications')
    with pytest.raises(vup.error.VupErrorRepositoryHasUncommitedChanges):
        vup.bump([a_repo.version_file], 'major')

    version_file = vup.VersionFile(a_repo.version_file)
    assert str(version_file.version) == DEFAULT_INPUT_VERSION + 'modifications'


def test_with_version_file_that_isnt_under_git(
        repo_without_version_file_commited):
    """

    :param repo_without_version_file_commited: fixture of a repository with a
    version file that isn't committed

    """
    repo_without_version_file_commited.init(DEFAULT_INPUT_VERSION)
    with pytest.raises(vup.error.VupErrorFileIsNotNotUnderRevisionControl):
        vup.bump([repo_without_version_file_commited.version_file], 'major')


def test_with_repo_without_commits(repo_without_commits):
    """

    :param repo_without_commits: fixture of a repository without commits

    """
    repo_without_commits.init(DEFAULT_INPUT_VERSION)
    with pytest.raises(vup.error.VupErrorFileIsNotNotUnderRevisionControl):
        vup.bump([repo_without_commits.version_file], 'major')


def test_pre_bump_hook(a_repo):
    """

    :param a_repo: fixture of a test repository

    """
    a_repo.init(DEFAULT_INPUT_VERSION)
    vup.bump([a_repo.version_file], 'major', 'echo success')

    version_file = vup.VersionFile(a_repo.version_file)
    assert str(version_file.version) == DEFAULT_OUTPUT_VERSION_MAJOR


def test_failed_prehook(a_repo):
    """

    :param a_repo: fixture of a test repository

    """
    a_repo.init(DEFAULT_INPUT_VERSION)
    with pytest.raises(vup.error.VupErrorPrehookFailed):
        vup.bump([a_repo.version_file], 'major', prehook='not_a_real_command')

    version_file = vup.VersionFile(a_repo.version_file)
    assert str(version_file.version) == DEFAULT_INPUT_VERSION


def test_posthook(a_repo):
    """

    :param a_repo: fixture of a test repository

    """
    a_repo.init(DEFAULT_INPUT_VERSION)
    vup.bump([a_repo.version_file], 'major', posthook='echo success')

    version_file = vup.VersionFile(a_repo.version_file)
    assert str(version_file.version) == DEFAULT_OUTPUT_VERSION_MAJOR


def test_failed_posthook(a_repo):
    """

    :param a_repo: fixture of a test repository

    """
    a_repo.init(DEFAULT_INPUT_VERSION)
    with pytest.raises(vup.error.VupErrorPosthookFailed):
        vup.bump([a_repo.version_file], 'major', posthook='not_a_real_command')

    version_file = vup.VersionFile(a_repo.version_file)
    assert str(version_file.version) == DEFAULT_OUTPUT_VERSION_MAJOR


# TODO test not in a git repository

# TODO test multi line files bump

# TODO test multiple version files

# TODO test multiple version files where one does not exist

# TODO test multiple version files where their version numbers don't match

# TODO test multiple version files where their version numbers don't match

# TODO test passing in empty list of version files

# TODO test passing in empty list of version files
