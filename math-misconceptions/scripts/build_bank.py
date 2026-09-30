#!/usr/bin/env python3
"""Build the files a Telegram bot or mobile app reads.

Reads exercises/<Topic>/<Type>.json and writes:
  build/bank.json   all served items, sorted by id, with delivery flags added
  build/index.json  item ids grouped by OPS goal, T-goal, level, grade,
                    misconception, type and topic

By default only items with status "approved" are served.
Use --include-draft for beta testing with unreviewed items.
"retired" items are never served.
The output is deterministic (no timestamps), so re-running does not create noisy diffs.

Usage (from math-misconceptions/):
  python scripts/build_bank.py                  # approved only
  python scripts/build_bank.py --include-draft  # beta
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    sys.exit(f"Missing dependency: {exc}. Run: pip install -r requirements.txt")


def delivery_flags(item):
    """Flags that tell a client how the item can be shown."""
    flags = {
        "text_only": not item["prompt"].get("latex") and not item["prompt"].get("figure"),
        "needs_figure": bool(item["prompt"].get("figure")),
        "telegram_poll": False,
    }
    if item["type"] == "MC":
        opts = item["payload"]["options"]
        flags["telegram_poll"] = (
            flags["text_only"]
            and len(item["prompt"]["text"]) <= 300
            and 2 <= len(opts) <= 10
            and all(len(o["text"]) <= 100 for o in opts)
            and len(item["feedback"]["correct"]) <= 200
        )
    return flags


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--exercises", default=str(ROOT / "exercises"))
    ap.add_argument("--out", default=str(ROOT / "build"))
    ap.add_argument("--include-draft", action="store_true")
    args = ap.parse_args()

    schema = json.loads((ROOT / "schema" / "item.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    served = {"approved", "draft"} if args.include_draft else {"approved"}

    items, skipped = [], defaultdict(int)
    for path in sorted(Path(args.exercises).glob("*/*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        for item in doc["items"]:
            problems = list(validator.iter_errors(item))
            if problems:
                sys.exit(f"{path}: {item.get('id', '?')} fails the schema ({problems[0].message[:120]}). Run verify.py first.")
            if item["status"] in served:
                out = dict(item)
                out["flags"] = delivery_flags(item)
                items.append(out)
            else:
                skipped[item["status"]] += 1
    items.sort(key=lambda i: i["id"])

    index = {k: defaultdict(list) for k in ("by_ops", "by_t", "by_level", "by_grade", "by_misconception", "by_type", "by_topic")}
    for it in items:
        c = it["curriculum"]
        for s in c["ops"]:
            index["by_ops"][s].append(it["id"])
        for t in c["t"]:
            index["by_t"][t].append(it["id"])
        index["by_level"][c["level"]].append(it["id"])
        index["by_grade"][str(c["grade"])].append(it["id"])
        for m in it["misconceptions"]:
            index["by_misconception"][m].append(it["id"])
        index["by_type"][it["type"]].append(it["id"])
        index["by_topic"][it["id"].rsplit("-", 2)[0]].append(it["id"])
    index = {k: {key: sorted(v[key]) for key in sorted(v)} for k, v in index.items()}

    bank = {
        "schema_version": "1.0",
        "bank_version": max((i["provenance"]["generated"] for i in items), default="0000-00-00"),
        "served_statuses": sorted(served),
        "counts": {"items": len(items), "skipped_by_status": dict(skipped)},
        "items": items,
    }
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, data in (("bank.json", bank), ("index.json", index)):
        (out_dir / name).write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {len(items)} item(s) to {out_dir}/bank.json and index.json "
          f"(served: {', '.join(sorted(served))}; skipped: {dict(skipped) or 'none'})")


if __name__ == "__main__":
    main()
