"""Tests for the CLI (no network, temp storage)."""

import os
import tempfile

from reading_list import cli
from reading_list.storage import Storage


def _runner(monkeypatch):
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    os.remove(path)
    storage = Storage(path=path)
    monkeypatch.setattr(cli, "Storage", lambda: storage)

    def run(argv):
        return cli.main(argv)

    return run, storage


def test_add_then_list(monkeypatch):
    run, storage = _runner(monkeypatch)
    assert run(["add", "Dune", "--type", "book", "--author", "Frank Herbert"]) == 0
    assert run(["list"]) == 0
    assert len(storage.all()) == 1
    assert storage.all()[0]["title"] == "Dune"


def test_list_empty(monkeypatch):
    run, _ = _runner(monkeypatch)
    assert run(["list"]) == 0


def test_done_and_todo(monkeypatch):
    run, storage = _runner(monkeypatch)
    run(["add", "X", "--type", "article"])
    entry_id = storage.all()[0]["id"]
    assert run(["done", entry_id]) == 0
    assert storage.get(entry_id)["status"] == "done"
    assert run(["todo", entry_id]) == 0
    assert storage.get(entry_id)["status"] == "to_read"


def test_remove(monkeypatch):
    run, storage = _runner(monkeypatch)
    run(["add", "Y", "--type", "book"])
    entry_id = storage.all()[0]["id"]
    assert run(["remove", entry_id]) == 0
    assert storage.get(entry_id) is None


def test_summary_without_endpoint_returns_error_code(monkeypatch):
    run, storage = _runner(monkeypatch)
    run(["add", "Z", "--type", "book"])
    entry_id = storage.all()[0]["id"]
    assert run(["summary", entry_id]) == 1
    assert storage.get(entry_id)["summary"] == ""
