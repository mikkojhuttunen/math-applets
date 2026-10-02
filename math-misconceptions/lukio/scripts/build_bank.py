#!/usr/bin/env python3
"""Build the files a Telegram bot, mobile app or practice page reads (lukio).

Copied from ../../scripts/build_bank.py (7-9) and adapted. Reads
exercises/<Topic>/<Type>.json and writes:
  build/bank.json   all served items, sorted by id, with delivery flags added
  build/index.json  item ids grouped by LOPS goal, module, syllabus,
                    misconception, type, level, tools, G-goal and topic

By default only items with status "approved" are served.
Use --include-draft for beta testing with unreviewed items.
"retired" items are never served.
The output is deterministic (no timestamps), so re-running does not create noisy diffs.

Usage (from math-misconceptions/lukio/):
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
    sys.exit(f"Missing dependency: {exc}. Run: pip install -r ../requirements.txt")

SCHEMA_VERSION = "lukio-1.0"
INDEX_KEYS = ("by_lops", "by_module", "by_syllabus", "by_misconception", "by_type",
              "by_level", "by_tools", "by_g", "by_topic")


def module(goal_id):
    """MAA6.06 -> MAA6, MAY1.03 -> MAY1."""
    return goal_id.split(".")[0]


def topic(item_id):
    """LU-LDER-02-ES-001 -> LDER-02."""
    return item_id[len("LU-"):].rsplit("-", 2)[0]


def delivery_flags(item):
    """Flags that tell a client how the item can be shown."""
    flags = {
        "text_only": not item["prompt"].get("latex") and not item["prompt"].get("figure"),
        "needs_figure": bool(item["prompt"].get("figure")),
        "telegram_poll": False,
        "needs_cas": item["curriculum"]["tools"] == "cas",
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

    index = {k: defaultdict(list) for k in INDEX_KEYS}
    for it in items:
        c, iid = it["curriculum"], it["id"]
        for g in c["lops"]:
            index["by_lops"][g].append(iid)
        for m in sorted({module(g) for g in c["lops"]}):
            index["by_module"][m].append(iid)
        index["by_syllabus"][c["syllabus"]].append(iid)
        for m in it["misconceptions"]:
            index["by_misconception"][m].append(iid)
        index["by_type"][it["type"]].append(iid)
        index["by_level"][c["level"]].append(iid)
        index["by_tools"][c["tools"]].append(iid)
        for g in c["g"]:
            index["by_g"][g].append(iid)
        index["by_topic"][topic(iid)].append(iid)
    index = {k: {key: sorted(v[key]) for key in sorted(v)} for k, v in index.items()}

    bank = {
        "schema_version": SCHEMA_VERSION,
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
