from src.flask_mongodb import __version__
from src.flask_mongodb import MongoDB

from pymongo import MongoClient

from flask import Flask
import pytest


def test_version():
    assert __version__ == "0.1.0"


@pytest.fixture
def cleanup():
    yield
    with MongoClient("localhost", 27017) as client:
        client.drop_database("test_db")


def test_flask_mongodb(cleanup):
    app = Flask(__name__)
    db = MongoDB(app)
    assert db.connection is None
    with app.app_context():
        db.connection.test_db.test_collection.insert_one({"test": "success"})
        result = db.connection.test_db.test_collection.find_one()
    assert result["test"] == "success"
