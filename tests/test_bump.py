import pytest
import vup.error
import vup
import util

# pylint: disable=invalid-name


@pytest.mark.parametrize(
    "input_version,output_version",
    [(util.DEFAULT_INPUT_VERSION, util.DEFAULT_OUTPUT_VERSION_MAJOR),
     ('1.2.3', '2.0.1-beta')])
def test_bump(a_repo, input_version, output_version):
    """

    :param a_repo: repository fixture to test with
    :param input_version: starting version
    :param output_version: version after bump

    """
    a_repo.init(input_version)
    vup.bump([a_repo.version_files[0]], 'major')

    version_file = vup.VersionFile(a_repo.version_files[0])
    assert str(version_file.version) == output_version


def test_bump_with_a_file_that_does_not_have_a_version(
        repo_with_empty_version_files):
    """
    :param a_repo: repository fixture to test with
    """
    repo_with_empty_version_files.init(util.DEFAULT_INPUT_VERSION)
    with pytest.raises(vup.error.VupErrorFileDoesNotHaveAVersionNumber):
        vup.bump([repo_with_empty_version_files.version_files[0]], 'major')


def test_bump_without_version_files(a_repo):
    """
    :param a_repo: repository fixture to test with
    """
    a_repo.init(util.DEFAULT_INPUT_VERSION)
    with pytest.raises(vup.error.VupErrorNoVersionFilesProvided):
        vup.bump([], 'major')


def test_bump_with_nonexistent_version_file(a_repo):
    """
    :param a_repo: repository fixture to test with
    """
    a_repo.init(util.DEFAULT_INPUT_VERSION)
    with pytest.raises(vup.error.VupErrorVersionFileDoesNotExist):
        vup.bump(['asdf'], 'major')


def test_dirty_bump(a_repo):
    """

    :param a_repo: fixture of a test repository

    """
    a_repo.init(util.DEFAULT_INPUT_VERSION)
    util.append_to_file(a_repo.version_files[0], 'modifications')
    with pytest.raises(vup.error.VupErrorRepositoryHasUncommitedChanges):
        vup.bump([a_repo.version_files[0]], 'major')

    version_file = vup.VersionFile(a_repo.version_files[0])
    assert (str(
        version_file.version) == util.DEFAULT_INPUT_VERSION + 'modifications')


def test_with_version_file_that_isnt_under_git(
        repo_without_version_file_commited):
    """

    :param repo_without_version_file_commited: fixture of a repository with a
    version file that isn't committed

    """
    repo_without_version_file_commited.init(util.DEFAULT_INPUT_VERSION)
    with pytest.raises(vup.error.VupErrorFileIsNotNotUnderRevisionControl):
        vup.bump([repo_without_version_file_commited.version_files[0]],
                 'major')


def test_with_repo_without_commits(repo_without_commits):
    """

    :param repo_without_commits: fixture of a repository without commits

    """
    repo_without_commits.init(util.DEFAULT_INPUT_VERSION)
    with pytest.raises(vup.error.VupErrorFileIsNotNotUnderRevisionControl):
        vup.bump([repo_without_commits.version_files[0]], 'major')


def test_pre_bump_hook(a_repo):
    """

    :param a_repo: fixture of a test repository

    """
    a_repo.init(util.DEFAULT_INPUT_VERSION)
    vup.bump([a_repo.version_files[0]], 'major', 'echo success')

    version_file = vup.VersionFile(a_repo.version_files[0])
    assert str(version_file.version) == util.DEFAULT_OUTPUT_VERSION_MAJOR


def test_failed_prehook(a_repo):
    """

    :param a_repo: fixture of a test repository

    """
    a_repo.init(util.DEFAULT_INPUT_VERSION)
    with pytest.raises(vup.error.VupErrorPrehookFailed):
        vup.bump([a_repo.version_files[0]],
                 'major',
                 prehook='not_a_real_command')

    version_file = vup.VersionFile(a_repo.version_files[0])
    assert str(version_file.version) == util.DEFAULT_INPUT_VERSION


def test_posthook(a_repo):
    """
    :param a_repo: fixture of a test repository
    """
    a_repo.init(util.DEFAULT_INPUT_VERSION)
    vup.bump([a_repo.version_files[0]], 'major', posthook='echo success')

    version_file = vup.VersionFile(a_repo.version_files[0])
    assert str(version_file.version) == util.DEFAULT_OUTPUT_VERSION_MAJOR


def test_failed_posthook(a_repo):
    """
    :param a_repo: fixture of a test repository
    """
    a_repo.init(util.DEFAULT_INPUT_VERSION)
    with pytest.raises(vup.error.VupErrorPosthookFailed):
        vup.bump([a_repo.version_files[0]],
                 'major',
                 posthook='not_a_real_command')

    version_file = vup.VersionFile(a_repo.version_files[0])
    assert str(version_file.version) == util.DEFAULT_OUTPUT_VERSION_MAJOR


def test_bump_when_not_in_a_git_repository(dir_without_repo):
    """
    :param a_repo: fixture of a test repository
    """
    dir_without_repo.init(util.DEFAULT_INPUT_VERSION)
    with pytest.raises(vup.error.VupErrorCurrentDirectoryIsNotAGitRepository):
        vup.bump([dir_without_repo.version_file], 'major')


def test_bump_where_type_is_invalid(a_repo):
    """
    :param a_repo: fixture of a test repository
    """
    a_repo.init(util.DEFAULT_INPUT_VERSION)
    with pytest.raises(vup.error.VupErrorBumpTypeIsInvalid):
        vup.bump([a_repo.version_files[0]], 'asdf')


def test_bump_where_the_version_file_contains_multiple_version_numbers(a_repo):
    """
    :param a_repo: fixture of a test repository
    """
    a_repo.init(util.DEFAULT_INPUT_VERSION)
    util.append_to_file(a_repo.version_files[0],
                        ' ' + util.DEFAULT_OUTPUT_VERSION_MAJOR)
    a_repo.repo.git.add(A=True)
    a_repo.repo.index.commit("Add additional version file")
    with pytest.raises(vup.error.VupErrorFileContainsMultipleVersionNumbers):
        vup.bump([a_repo.version_files[0]], 'major')


def test_bump_with_multiple_version_files(a_repo):
    """
    :param a_repo: fixture of a test repository
    """
    a_repo.init(util.DEFAULT_INPUT_VERSION, ('version_1.txt', 'version_2.txt'))
    vup.bump(a_repo.version_files, 'major')

    version_file_1 = vup.VersionFile(a_repo.version_files[0])
    assert str(version_file_1.version) == util.DEFAULT_OUTPUT_VERSION_MAJOR
    version_file_2 = vup.VersionFile(a_repo.version_files[1])
    assert str(version_file_2.version) == util.DEFAULT_OUTPUT_VERSION_MAJOR


def test_bump_where_version_files_dont_have_matching_versions(a_repo):
    """
    :param a_repo: fixture of a test repository
    """
    a_repo.init(util.DEFAULT_INPUT_VERSION, ('version_1.txt', 'version_2.txt'))

    with open(a_repo.version_files[0], 'w') as file_handle:
        file_handle.write(util.DEFAULT_OUTPUT_VERSION_MAJOR)

    a_repo.repo.git.add(A=True)
    a_repo.repo.index.commit("Add additional version file")

    with pytest.raises(vup.error.VupErrorFilesDontHaveMatchingVersions):
        vup.bump(a_repo.version_files, 'major')


def test_bump_where_the_repo_already_has_version_tag(a_repo):
    """
    :param a_repo: fixture of a test repository
    """
    a_repo.init(util.DEFAULT_INPUT_VERSION)
    a_repo.repo.create_tag(
        util.DEFAULT_RELEASED_VERSION_MAJOR, message='pre-existing tag')
    with pytest.raises(vup.error.VupErrorVersionTagAlreadyExists):
        vup.bump(a_repo.version_files, 'major')


# TODO test bump minor version
# TODO test bump patch version
# TODO test bump pre-release version
# TODO stdout of run_hook
# TODO run_hook passing
# TODO version file is not at the root of git repo
# TODO using a config file
# TODO test multi line files bump
# TODO test multiple version files
# TODO test multiple version files where one does not exist
# TODO test multiple version files where their version numbers don't match
