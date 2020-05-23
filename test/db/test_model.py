import pytest
from db import model

@pytest.fixture
def fake_db_name(monkeypatch):
    monkeypatch.setattr(model.DB, 'DB_NAME', 'vki_test')

@pytest.fixture
def fake_db(fake_db_name):
    db = model.DB('fake')
    yield db
    db.connection.drop_database(db.DB_NAME)
    db.connection.close()

def test_save(fake_db):
    def count_docs():
        return fake_db.connection[fake_db.DB_NAME][fake_db.user_id].count_documents({'id': 1})
    assert count_docs() == 0
    fake_db.save({'id': 1})
    assert count_docs() == 1
    fake_db.save({'id': 1, 'some': 'field'})
    assert count_docs() == 1

def test_set_skip(fake_db):
    fake_db.save({'id': 5})
    assert fake_db.is_db_empty() == False
    fake_db.set_skip(5)
    assert fake_db.is_db_empty() == True

def test_load_and_save_settings(fake_db):
    fake_db.save_settings_to_db({'some': 'settings'})
    assert fake_db.user_id == fake_db.load_settings_from_db()['id']

    
    