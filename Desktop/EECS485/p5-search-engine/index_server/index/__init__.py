"""Search Engine package initializer."""
import os
import flask


app = flask.Flask(__name__)

app.config.from_envvar('INSTA485_SETTINGS', silent=True)
app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")
app.config["STOPWORDS"] = set()
app.config["PAGE_RANK_DICT"] = {}
app.config["INVERTED_INDEX"] = {}

import index.api  # noqa: E402  pylint: disable=wrong-import-position

# Load inveshidrted index, stopwords, and pagerank into memory
index.api.load_index()
