import pytest
from api import api

@pytest.fixture
def fake_token():
    return '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'

@pytest.fixture
def fake_vk(fake_token):
    return api.VK(fake_token)

@pytest.fixture
def fake_id():
    return '3476646'

def test_get_user(fake_vk, fake_id):
    assert isinstance(fake_vk.get_user(fake_id), dict)

@pytest.mark.parametrize(
    'name, _id',
    [
        ('rychanya', 3476646),
        ('3476646', 3476646),
        ('kjjjek35043ijhkdbvdd', None)
    ]
)
def test_resolve_screen_name(fake_vk, name, _id):
    assert fake_vk.resolve_screen_name(name) == _id

def test_get_groups(fake_vk, fake_id):
    assert isinstance(fake_vk.get_groups(fake_id), list)
