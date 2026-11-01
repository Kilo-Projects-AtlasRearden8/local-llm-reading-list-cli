"""Tests for local JSON storage."""

import json
import os
import tempfile

from reading_list.storage import Storage, STATUSES, TYPES


def _make_storage():
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    os.remove(path)
    return Storage(path=path)


def test_add_and_get():
    storage = _make_storage()
    entry = storage.add("The Massive AI Manual", "book", author="Dylan Asdale", url="https://example.com")
    assert entry["id"]
    assert entry["title"] == "The Massive AI Manual"
    assert entry["type"] == "book"
    assert entry["author"] == "Dylan Asdale"
    assert entry["url"] == "https://example.com"
    assert entry["status"] == "to_read"
    assert entry["summary"] == ""
    assert entry["added_at"]

    fetched = storage.get(entry["id"])
    assert fetched["title"] == "The Massive AI Manual"


def test_all_and_filter():
    storage = _make_storage()
    storage.add("Book One", "book")
    storage.add("Article One", "article")
    storage.add("Book Two", "book")

    assert len(storage.all()) == 3
    assert len(storage.filter(status="to_read")) == 3
    assert len(storage.filter(entry_type="book")) == 2
    assert len(storage.filter(entry_type="article")) == 1

    storage.update_status(storage.all()[0]["id"], "done")
    assert len(storage.filter(status="done")) == 1
    assert len(storage.filter(status="to_read")) == 2


def test_update_status_unknown_returns_none():
    storage = _make_storage()
    assert storage.update_status("nope", "done") is None


def test_set_summary():
    storage = _make_storage()
    entry = storage.add("Some Book", "book")
    updated = storage.set_summary(entry["id"], "A short one-sentence summary.")
    assert updated["summary"] == "A short one-sentence summary."
    assert updated["summary_at"]
    fetched = storage.get(entry["id"])
    assert fetched["summary"] == "A short one-sentence summary."


def test_set_summary_unknown_returns_none():
    storage = _make_storage()
    assert storage.set_summary("nope", "summary") is None


def test_remove():
    storage = _make_storage()
    entry = storage.add("To Remove", "book")
    assert storage.remove(entry["id"]) is True
    assert storage.get(entry["id"]) is None
    assert storage.remove(entry["id"]) is False


def test_types_and_statuses_constants():
    assert "book" in TYPES and "article" in TYPES
    assert "to_read" in STATUSES and "reading" in STATUSES and "done" in STATUSES
