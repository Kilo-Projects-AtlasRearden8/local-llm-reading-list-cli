"""Local JSON storage for reading list entries."""

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .config import DATA_PATH

STATUSES = ("to_read", "reading", "done")
TYPES = ("book", "article")


def _now():
    return datetime.now(timezone.utc).isoformat()


class Storage:
    def __init__(self, path=None):
        self.path = Path(path) if path else DATA_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write([])

    def _read(self):
        with self.path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _write(self, entries):
        tmp = self.path.with_suffix(".json.tmp")
        with tmp.open("w", encoding="utf-8") as handle:
            json.dump(entries, handle, indent=2)
            handle.write("\n")
        os.replace(tmp, self.path)

    def all(self):
        return list(self._read())

    def add(self, title, entry_type, author=None, url=None):
        entries = self._read()
        entry = {
            "id": str(uuid.uuid4())[:8],
            "title": title,
            "type": entry_type,
            "author": author or "",
            "url": url or "",
            "status": "to_read",
            "added_at": _now(),
            "summary": "",
            "summary_at": "",
        }
        entries.append(entry)
        self._write(entries)
        return entry

    def get(self, entry_id):
        for entry in self._read():
            if entry["id"] == entry_id:
                return entry
        return None

    def update_status(self, entry_id, status):
        entries = self._read()
        for entry in entries:
            if entry["id"] == entry_id:
                entry["status"] = status
                self._write(entries)
                return entry
        return None

    def set_summary(self, entry_id, summary):
        entries = self._read()
        for entry in entries:
            if entry["id"] == entry_id:
                entry["summary"] = summary
                entry["summary_at"] = _now()
                self._write(entries)
                return entry
        return None

    def remove(self, entry_id):
        entries = self._read()
        kept = [e for e in entries if e["id"] != entry_id]
        if len(kept) == len(entries):
            return False
        self._write(kept)
        return True

    def filter(self, status=None, entry_type=None):
        entries = self._read()
        if status:
            entries = [e for e in entries if e["status"] == status]
        if entry_type:
            entries = [e for e in entries if e["type"] == entry_type]
        return entries
