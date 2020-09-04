import json
import os
import pytest

with open('tests/config.test.json', 'r') as f:
    json_test_schema = json.load(f)
    for key in json_test_schema:
        os.environ[key] = str(json_test_schema[key])

from core import create_app
import models

# NOTE Admin user on tests/data.sql
TEST_USERNAME = 'test'
TEST_PASSWORD = 'qpalzm'

@pytest.fixture(name='client')
def client():
    app = create_app(config={'TESTING': True})
    with app.app_context():
        # NOTE Cleaning database
        models.db.reflect()
        models.db.drop_all()
        models.db.create_all()

        # NOTE Populationg database with test data
        with open('tests/data.sql', 'rb') as f:
            _data_sql = f.read().decode('utf8')

        models.db.engine.execute(_data_sql)

    return app.test_client()