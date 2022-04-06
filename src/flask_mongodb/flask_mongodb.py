"""Flask extension to connect to MongoDB"""
from typing import Optional

from flask import current_app, _app_ctx_stack
from flask.app import Flask
from pymongo import MongoClient


class MongoDB:
    """Connects Flask app to MongoDB backend"""

    def __init__(self, app: Flask = None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """
        Initialize flask app with mongodb config
        :param app: flask app
        """
        app.config.setdefault("MONGODB_HOST", "localhost")
        app.config.setdefault("MONGODB_PORT", 27017)
        app.config.setdefault("MONGODB_USERNAME", "")
        app.config.setdefault("MONGODB_PASSWORD", "")
        app.teardown_appcontext(self.teardown)

    @staticmethod
    def connect() -> MongoClient:
        """
        Create MongoClient connection
        :rtype: MongoClient
        """
        host = current_app.config["MONGODB_HOST"]
        port = current_app.config["MONGODB_PORT"]
        username = current_app.config["MONGODB_USERNAME"]
        password = current_app.config["MONGODB_PASSWORD"]
        return MongoClient(host, port, username=username, password=password)

    @staticmethod
    # pylint: disable=unused-argument
    def teardown(exception: Optional[BaseException]) -> None:
        """
        Close connection on teardown
        """
        ctx = _app_ctx_stack.top
        if hasattr(ctx, "mongodb_client"):
            ctx.mongodb_client.close()

    @property
    def connection(self) -> Optional[MongoClient]:
        """
        Creates new connection on first call or provides previously opened connection
        :rtype: MongoClient
        """
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, "mongodb_client"):
                ctx.mongodb_client = self.connect()
            return ctx.mongodb_client
        return None
