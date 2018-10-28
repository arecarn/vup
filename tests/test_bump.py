import vup
import pytest


def test_bump(a_repo):
    vup.bump(a_repo, 'major')


def test_dirty_bump(a_dirty_repo):
    with pytest.raises(Exception):
        vup.bump(a_dirty_repo, 'major')
