import pytest
from vkinder import app


@pytest.fixture
def fake_app(monkeypatch):
    def fake_init(self, token, _id):
        self.user_id = _id
        self.db = app.model.DB(self.user_id)
    monkeypatch.setattr(app.model.DB, 'DB_NAME', 'vki_test')
    monkeypatch.setattr(app.APP, '__init__', fake_init)
    test_app = app.APP(token=None, _id='fake')
    yield test_app
    test_app.db.connection.drop_database(test_app.db.DB_NAME)
