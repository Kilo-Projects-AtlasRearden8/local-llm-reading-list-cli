"""AI summary client for OpenAI-compatible endpoints (default Ollama)."""

import json
import urllib.error
import urllib.request

from .config import load_config


def generate_summary(title, entry_type, author="", config=None):
    """Generate a one-sentence summary via a local OpenAI-compatible endpoint.

    Returns the summary string, or None if the endpoint is unavailable so the
    CLI stays usable offline (local-first).
    """
    if config is None:
        config = load_config()
    endpoint = config.get("endpoint", "http://localhost:11434/v1")
    model = config.get("model", "llama3.2")
    system_prompt = config.get(
        "system_prompt",
        "Write a single sentence summarizing the book or article.",
    )
    temperature = config.get("temperature", 0.3)

    label = entry_type or "book"
    byline = f" by {author}" if author else ""
    user_prompt = (
        f"Summarize the {label} \"{title}\"{byline} in exactly one sentence."
    )

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "stream": False,
    }

    url = endpoint.rstrip("/") + "/chat/completions"
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read()
    except (urllib.error.URLError, OSError):
        return None

    try:
        parsed = json.loads(body)
    except json.JSONDecodeError:
        return None

    if not isinstance(parsed, dict):
        return None
    choices = parsed.get("choices")
    if not choices:
        return None
    message = choices[0].get("message", {})
    content = message.get("content", "")
    content = " ".join(content.split())
    return content or None
