# STATUS

## What was built

`reading-list-cli` — a local-first Python CLI (stdlib only, no dependencies)
that tracks books and articles to read and generates one-sentence AI
summaries from a configurable OpenAI-compatible endpoint (default Ollama at
`http://localhost:11434/v1`).

Files:
- `reading_list/__init__.py` — package marker, version 0.1.0
- `reading_list/__main__.py` — `python -m reading_list` entry point
- `reading_list/cli.py` — argparse CLI: add, list, summary, done, todo, remove, config
- `reading_list/config.py` — config at `~/.config/reading-list/config.json`, env overrides `READING_LIST_ENDPOINT` / `READING_LIST_MODEL`
- `reading_list/storage.py` — atomic JSON storage at `~/.local/share/reading-list/reading_list.json`
- `reading_list/summarizer.py` — `urllib` client POSTing to `{endpoint}/chat/completions`; returns None offline so the CLI stays usable without AI
- `tests/test_storage.py`, `tests/test_summarizer.py`, `tests/test_cli.py` — 16 tests, no network
- `conftest.py`, `pyproject.toml` (with `[project.scripts] reading-list` entry point)
- `LICENSE` — MIT, `Copyright (c) 2026 Asdale Dynamics, LLC`
- `README.md` — credits Asdale Dynamics, LLC

Built for Dylan Asdale / Asdale Dynamics, LLC (Indiana, formed Oct 2026):
beginner-friendly AI education tool, plain English, local-first, no keys, no
personal data.

## How to run

```bash
# install
pip install .          # or pip install -e .

# or run directly
python -m reading_list --help

# examples
reading-list add "The Massive AI Manual" --type book --author "Dylan Asdale"
reading-list add "Understanding MCP Servers" --type article
reading-list list
reading-list summary <id>
reading-list done <id>
reading-list config --endpoint http://localhost:11434/v1 --model llama3.2
```

AI summaries are optional: if the endpoint is unreachable, `summary` reports an
error but the entry is still saved. No API keys are ever stored or sent.

## Verification results

- `pytest -q`: 16 passed (storage, summarizer with faked responses, CLI)
- `python -m py_compile reading_list/*.py tests/*.py`: OK
- End-to-end smoke test: `add`, `list`, help all work with a temp data dir
- No network required for tests or core CLI behavior
- No `.github/workflows` files; no secrets, API keys, or personal data in any file

## Known gaps

- No PyPI packaging/CI (`pyproject.toml` defines the entry point but no release workflow; none requested)
- Summarizer has no retries or timeout configurability (fixed 30s timeout)
- Summary regeneration requires `--force`; existing summaries are not overwritten
- Data location defaults to `~/.local/share/reading-list/`; override via `READING_LIST_DATA_DIR`
- Ollama must be running locally for AI summaries; endpoint is fully configurable
