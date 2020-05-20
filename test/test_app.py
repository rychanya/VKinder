import pytest
from vkinder import app


@pytest.fixture
def token():
    return '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'

@pytest.fixture
def t_app(token):
    return app.APP(token, 'rychanya')

