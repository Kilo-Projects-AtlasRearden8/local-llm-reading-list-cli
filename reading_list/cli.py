"""Command-line interface for the reading list."""

import argparse
import sys

from .config import DEFAULTS, load_config, save_config
from .storage import Storage, STATUSES, TYPES
from .summarizer import generate_summary


def _format_entry(entry, show_summary=False):
    status_mark = {"to_read": "[]", "reading": "[>]", "done": "[x]"}
    mark = status_mark.get(entry["status"], "[]")
    line = f'{mark} {entry["id"]}  {entry["title"]}  ({entry["type"]})'
    if entry.get("author"):
        line += f"  by {entry['author']}"
    if show_summary and entry.get("summary"):
        line += f"\n      summary: {entry['summary']}"
    return line


def cmd_add(args):
    storage = Storage()
    if args.type not in TYPES:
        print(f"error: type must be one of {', '.join(TYPES)}", file=sys.stderr)
        return 1
    entry = storage.add(args.title, args.type, author=args.author, url=args.url)
    print(f"added {entry['id']}: {entry['title']}")
    return 0


def cmd_list(args):
    storage = Storage()
    entries = storage.filter(status=args.status, entry_type=args.type)
    if not entries:
        print("no entries found")
        return 0
    for entry in entries:
        print(_format_entry(entry, show_summary=args.summary))
    return 0


def cmd_summary(args):
    storage = Storage()
    entry = storage.get(args.id)
    if not entry:
        print(f"error: no entry with id {args.id}", file=sys.stderr)
        return 1
    if entry.get("summary") and not args.force:
        print(f"{entry['id']}: {entry['summary']}")
        return 0
    summary = generate_summary(entry["title"], entry["type"], entry.get("author", ""))
    if summary is None:
        print(
            f"error: AI endpoint unavailable (set READING_LIST_ENDPOINT or start Ollama)",
            file=sys.stderr,
        )
        return 1
    storage.set_summary(args.id, summary)
    print(f"{entry['id']}: {summary}")
    return 0


def cmd_done(args):
    storage = Storage()
    entry = storage.update_status(args.id, "done")
    if not entry:
        print(f"error: no entry with id {args.id}", file=sys.stderr)
        return 1
    print(f"marked {entry['id']} done: {entry['title']}")
    return 0


def cmd_todo(args):
    storage = Storage()
    entry = storage.update_status(args.id, "to_read")
    if not entry:
        print(f"error: no entry with id {args.id}", file=sys.stderr)
        return 1
    print(f"marked {entry['id']} to_read: {entry['title']}")
    return 0


def cmd_config(args):
    if args.endpoint or args.model:
        config = load_config()
        if args.endpoint:
            config["endpoint"] = args.endpoint.rstrip("/")
        if args.model:
            config["model"] = args.model
        save_config(config)
        print("config saved")
    config = load_config()
    print(f"endpoint: {config.get('endpoint', DEFAULTS['endpoint'])}")
    print(f"model: {config.get('model', DEFAULTS['model'])}")
    return 0


def cmd_remove(args):
    storage = Storage()
    if storage.remove(args.id):
        print(f"removed {args.id}")
        return 0
    print(f"error: no entry with id {args.id}", file=sys.stderr)
    return 1


def build_parser():
    parser = argparse.ArgumentParser(
        prog="reading-list",
        description="Track books and articles to read, with local AI summaries.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="add a book or article")
    p_add.add_argument("title")
    p_add.add_argument("--type", choices=TYPES, default="book")
    p_add.add_argument("--author", default="")
    p_add.add_argument("--url", default="")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="list entries")
    p_list.add_argument("--status", choices=STATUSES)
    p_list.add_argument("--type", choices=TYPES)
    p_list.add_argument("--summary", action="store_true")
    p_list.set_defaults(func=cmd_list)

    p_sum = sub.add_parser("summary", help="generate a one-sentence AI summary")
    p_sum.add_argument("id")
    p_sum.add_argument("--force", action="store_true")
    p_sum.set_defaults(func=cmd_summary)

    p_done = sub.add_parser("done", help="mark an entry done")
    p_done.add_argument("id")
    p_done.set_defaults(func=cmd_done)

    p_todo = sub.add_parser("todo", help="mark an entry to_read")
    p_todo.add_argument("id")
    p_todo.set_defaults(func=cmd_todo)

    p_cfg = sub.add_parser("config", help="show or save config")
    p_cfg.add_argument("--endpoint")
    p_cfg.add_argument("--model")
    p_cfg.set_defaults(func=cmd_config)

    p_rm = sub.add_parser("remove", help="remove an entry")
    p_rm.add_argument("id")
    p_rm.set_defaults(func=cmd_remove)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
