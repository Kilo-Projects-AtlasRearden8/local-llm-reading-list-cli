"""Configuration for the reading list CLI."""

import json
import os
from pathlib import Path

DEFAULT_ENDPOINT = "http://localhost:11434/v1"
DEFAULT_MODEL = "llama3.2"
DEFAULT_SYSTEM_PROMPT = (
    "Write a single sentence summarizing the book or article. "
    "Be plain, warm, and beginner-friendly. No spoilers."
)

CONFIG_DIR = Path(os.environ.get("READING_LIST_CONFIG_DIR", Path.home() / ".config" / "reading-list"))
DATA_DIR = Path(os.environ.get("READING_LIST_DATA_DIR", Path.home() / ".local" / "share" / "reading-list"))
CONFIG_PATH = CONFIG_DIR / "config.json"
DATA_PATH = DATA_DIR / "reading_list.json"

DEFAULTS = {
    "endpoint": DEFAULT_ENDPOINT,
    "model": DEFAULT_MODEL,
    "system_prompt": DEFAULT_SYSTEM_PROMPT,
    "temperature": 0.3,
}


def load_config():
    """Load config, falling back to defaults and environment overrides."""
    config = dict(DEFAULTS)
    if CONFIG_PATH.exists():
        try:
            with CONFIG_PATH.open("r", encoding="utf-8") as handle:
                loaded = json.load(handle)
            if isinstance(loaded, dict):
                config.update(loaded)
        except (OSError, json.JSONDecodeError):
            pass
    env_endpoint = os.environ.get("READING_LIST_ENDPOINT")
    env_model = os.environ.get("READING_LIST_MODEL")
    if env_endpoint:
        config["endpoint"] = env_endpoint.rstrip("/")
    if env_model:
        config["model"] = env_model
    return config


def save_config(config):
    """Persist config to disk."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with CONFIG_PATH.open("w", encoding="utf-8") as handle:
        json.dump(config, handle, indent=2)
        handle.write("\n")
