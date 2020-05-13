import pytest
from vkinder import app


@pytest.fixture
def fake_input(monkeypatch, request):
    def _input(*args, **kwargs):
        return 'faked'
    monkeypatch.setattr('builtins.input', _input)


