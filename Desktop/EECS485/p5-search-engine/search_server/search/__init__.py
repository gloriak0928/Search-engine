"""Insta485 package initializer."""
import flask

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)

# Read settings from config module (search/config.py)
app.config.from_object("search.config")

# from index_server.index import api  # noqa: E402  pylint: disable=wrong-import-position
import search.views  # noqa: E402  pylint: disable=wrong-import-position
import search.model  # noqa: E402  pylint: disable=wrong-import-position
