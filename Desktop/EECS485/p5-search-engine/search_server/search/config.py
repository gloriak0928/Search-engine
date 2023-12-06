"""Insta485 development configuration."""

import pathlib

SEARCH_INDEX_SEGMENT_API_URLS = [
    "http://localhost:9000/api/v1/hits/",
    "http://localhost:9001/api/v1/hits/",
    "http://localhost:9002/api/v1/hits/",
]
APPLICATION_ROOT = "/"

SEARCH_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
DATABASE_FILENAME = SEARCH_ROOT/"var"/"search.sqlite3"


# File Upload to var/uploads/
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024