import vup


def test_bump_simple(a_repo):
    vup.bump(a_repo, 'major')
