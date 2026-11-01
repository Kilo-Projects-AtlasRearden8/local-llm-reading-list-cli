"""Tests for the AI summarizer (offline-safe, no network)."""

import json
from unittest import mock

from reading_list.summarizer import generate_summary


class _FakeResponse:
    def __init__(self, payload, status=200):
        self._payload = payload
        self.status = status

    def read(self):
        return json.dumps(self._payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def _patch_urlopen(monkeypatch, response):
    monkeypatch.setattr(
        "reading_list.summarizer.urllib.request.urlopen",
        lambda request, timeout=None: response,
    )


def test_generate_summary_returns_content(monkeypatch):
    response = _FakeResponse(
        {"choices": [{"message": {"content": "  A one sentence summary.  "}}]}
    )
    _patch_urlopen(monkeypatch, response)
    config = {"endpoint": "http://localhost:11434/v1", "model": "llama3.2"}
    summary = generate_summary("Some Book", "book", author="Author", config=config)
    assert summary == "A one sentence summary."


def test_generate_summary_handles_missing_choices(monkeypatch):
    response = _FakeResponse({})
    _patch_urlopen(monkeypatch, response)
    assert generate_summary("Some Book", "book") is None


def test_generate_summary_unavailable_returns_none(monkeypatch):
    import urllib.error

    def boom(request, timeout=None):
        raise urllib.error.URLError("connection refused")

    monkeypatch.setattr(
        "reading_list.summarizer.urllib.request.urlopen", boom
    )
    assert generate_summary("Some Book", "book") is None


def test_generate_summary_sends_expected_payload(monkeypatch):
    captured = {}

    class _FakeRequest:
        def __init__(self, url, data=None, headers=None, method=None):
            captured["url"] = url
            captured["data"] = data
            captured["headers"] = headers
            captured["method"] = method

    def fake_urlopen(request, timeout=None):
        captured["request"] = request
        return _FakeResponse(
            {"choices": [{"message": {"content": "Summary sentence."}}]}
        )

    monkeypatch.setattr(
        "reading_list.summarizer.urllib.request.Request", _FakeRequest
    )
    monkeypatch.setattr(
        "reading_list.summarizer.urllib.request.urlopen", fake_urlopen
    )
    config = {"endpoint": "http://localhost:11434/v1/", "model": "mistral"}
    summary = generate_summary("Title", "article", author="Author", config=config)
    assert summary == "Summary sentence."
    assert captured["url"] == "http://localhost:11434/v1/chat/completions"
    assert captured["method"] == "POST"
    payload = json.loads(captured["data"])
    assert payload["model"] == "mistral"
    assert payload["stream"] is False
    assert payload["messages"][0]["role"] == "system"
    assert "Title" in payload["messages"][1]["content"]
    assert "Author" in payload["messages"][1]["content"]
