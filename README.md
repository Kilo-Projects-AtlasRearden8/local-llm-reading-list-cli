# reading-list-cli

Local-first CLI that tracks books and articles to read, with AI-generated
one-sentence summaries from a configurable OpenAI-compatible endpoint
(default Ollama). No API keys, no accounts, no cloud. Built and maintained
by Asdale Dynamics, LLC.

## Who this is for

Dylan Asdale is a registered nurse turned AI author and founder of Asdale
Dynamics, LLC (Indiana, formed Oct 2026). His book *The Massive AI Manual*
and hub site dylanasdale.github.io explain AI "like a friend would": plain
English, step by step, never condescending. This tool is part of the LLC's
open-source, local-first AI utilities for beginners.

## Install

```bash
pip install .
```

or run directly:

```bash
python -m reading_list --help
```

## Usage

Add a book:

```bash
reading-list add "The Massive AI Manual" --type book --author "Dylan Asdale"
```

Add an article:

```bash
reading-list add "Understanding MCP Servers" --type article --url https://example.com/article
```

List what's to read:

```bash
reading-list list
```

Generate a one-sentence AI summary (hits your local endpoint, default Ollama at `http://localhost:11434/v1`):

```bash
reading-list summary <id>
```

Mark progress:

```bash
reading-list done <id>
reading-list todo <id>
```

Remove an entry:

```bash
reading-list remove <id>
```

## Configure the AI endpoint

```bash
reading-list config --endpoint http://localhost:11434/v1 --model llama3.2
reading-list config --show
```

Override with environment variables:

```bash
export READING_LIST_ENDPOINT=http://localhost:11434/v1
export READING_LIST_MODEL=llama3.2
```

Data lives locally in `~/.local/share/reading-list/reading_list.json`; config
in `~/.config/reading-list/config.json`. Everything is plain JSON you can
back up or move yourself.

## Tests

```bash
pytest
```

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC.

## Credit

Built by Asdale Dynamics, LLC — beginner-friendly AI education, books and
guides, and practical local-first tools.
