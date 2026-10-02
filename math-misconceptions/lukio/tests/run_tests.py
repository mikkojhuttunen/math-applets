#!/usr/bin/env python3
"""Self-test for the lukio verify.py and build_bank.py.  Run from anywhere:
    python tests/run_tests.py
Copied from ../../tests/run_tests.py (7-9) and adapted. Exit code 0 means
every check behaved as expected.

Fixtures:
  tests/fixtures/good/  the seed items (provenance.template "seed", one per
                        phase 0-2 type, logged as Seed in BACKLOG_LUKIO.md)
                        and extra items for the lukio answer kinds
  tests/fixtures/bad/   one folder per check; each must fail with the
                        message listed in EXPECT
The fixtures were written by hand; they are not generator output."""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIX = ROOT / "tests" / "fixtures"
BACKLOG = "BACKLOG_LUKIO.md"
GOOD_ITEMS = 13
SEED_TYPES = ["MC", "NE", "ES", "SO", "FS", "ME", "RP"]
sys.path.insert(0, str(ROOT / "scripts"))
import verify  # noqa: E402

failures = []


def run(*args, cwd=ROOT, script="verify.py"):
    return subprocess.run([sys.executable, str(cwd / "scripts" / script), *args], capture_output=True, text=True, cwd=cwd)


def check(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + ("" if ok else f"  -> {detail}"))
    if not ok:
        failures.append(name)


# 0. the kit is complete
req = ROOT.parent / "requirements.txt"
check("../requirements.txt exists", req.exists())
if req.exists():
    text = req.read_text(encoding="utf-8").lower()
    for pkg in ("sympy", "jsonschema"):
        check(f"requirements.txt lists {pkg}", pkg in text)
for rel in ("schema/item.schema.json", "scripts/verify.py", "scripts/build_bank.py", "README.md", BACKLOG):
    check(f"file present: {rel}", (ROOT / rel).exists())

# 1. good fixtures pass
r = run("--exercises", str(FIX / "good"))
check("good fixtures verify OK", r.returncode == 0 and f"VERIFY OK: {GOOD_ITEMS} item(s)" in r.stdout, r.stdout[-400:])

# 2. every bad fixture fails with its expected message
EXPECT = {
    # carried over from 7-9
    "es_no_error": "no error was injected",
    "so_bad_line": "not equivalent to line 1",
    "fs_bad_solutions": "answer.solutions does not match",
    "me_flag_wrong": "equivalent flag",
    "rp_bad_valid": "does not behave as valid",
    "mc_no_tag": "no wrong option is tagged",
    "unverified": "verified is false",
    "duplicate_id": "duplicate id",
    # answer kind rational
    "rational_not_lowest": "not in lowest terms",
    "rational_wrong_equal": "equals the correct value",
    # answer kind antiderivative
    "anti_bad_reference": "derivative of the reference is not the integrand",
    "anti_no_constant": "does not contain the constant",
    "anti_wrong_is_right": "is a correct antiderivative with the constant",
    "anti_undefined_sample": "undefined at sample",
    # answer kind periodic
    "periodic_missing_base": "base solutions miss",
    "periodic_bad_base": "does not satisfy the equation",
    "periodic_bad_period": "is not a period of the equation",
    # answer kind interval
    "interval_mismatch": "intervals do not match the solution set",
    "interval_order": "overlap or are out of order",
    "interval_wrong_is_right": "has the correct solution set",
    # curriculum links
    "syllabus_goal_mismatch": "belongs to the other syllabus",
    "syllabus_not_allowed": "is not listed for topic",
    "retired_goal": "is retired in the LOPS file",
    "missing_main_goal": "must include the main goal",
    "goal_not_linked": "is not linked to topic",
    "g_not_linked": "G-goal G7 is not linked",
    "unknown_misconception": "unknown misconception id LZZZ-01",
    # schema and wrapper
    "schema_e_variable": "schema: payload/answer",
    "schema_old_id": "schema: id",
    "schema_old_curriculum": "schema: curriculum",
    "wrapper_version": "wrapper values do not match",
}
for case, needle in EXPECT.items():
    r = run("--exercises", str(FIX / "bad" / case))
    check(f"bad fixture '{case}' is rejected", r.returncode == 1 and needle in r.stdout, r.stdout[-400:])
on_disk = {p.name for p in (FIX / "bad").iterdir()}
check("every bad fixture has an expectation", on_disk == set(EXPECT), str(on_disk ^ set(EXPECT)))

# 3. the LOPS file and the catalogue are really read
lops_text = (ROOT / verify.LOPS_FILE).read_text(encoding="utf-8")
with tempfile.TemporaryDirectory() as tmp:
    lops = Path(tmp) / "lops.md"
    lops.write_text(re.sub(r"^\| MAB5\.06 \|.*\n", "", lops_text, flags=re.M), encoding="utf-8")
    r = run("--exercises", str(FIX / "good"), "--lops", str(lops))
    check("goal missing from the LOPS file is rejected", r.returncode == 1 and "MAB5.06 is not in the LOPS file" in r.stdout, r.stdout[-400:])

    retired = re.sub(r"^\| (MAA8\.04) \| ", r"| \1 | *poistettu* ", lops_text, count=1, flags=re.M)
    lops.write_text(retired, encoding="utf-8")
    r = run("--exercises", str(FIX / "good"), "--lops", str(lops))
    check("backlog topic linked to a retired goal is rejected", r.returncode == 1 and "goal MAA8.04 is retired in the LOPS file" in r.stdout, r.stdout[-400:])

    cat = Path(tmp) / "catalogue.md"
    cat.write_text("no rows\n", encoding="utf-8")
    r = run("--exercises", str(FIX / "good"), "--catalogue", str(cat))
    check("catalogue-only tag ALG-11 needs the catalogue", r.returncode == 1 and "unknown misconception id ALG-11" in r.stdout, r.stdout[-400:])

# 4. backlog cross-check on a copy whose matrix has no X cells
raw = (ROOT / BACKLOG).read_text(encoding="utf-8")
codes, rows = verify.parse_matrix(raw)
have = {(p.parent.name, p.stem) for p in (FIX / "good").glob("*/*.json")}


def with_cells(mark):
    out, in_m = [], False
    for line in raw.splitlines():
        if line.startswith("| ID | MC |"):
            in_m = True
        elif in_m and not line.startswith("|"):
            in_m = False
        if in_m and line.split("|")[1].strip() in rows:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            for i, code in enumerate(codes):
                if cells[i + 1] == "X":
                    cells[i + 1] = "o"
                if (cells[0], code) in have:
                    cells[i + 1] = mark
            line = "| " + " | ".join(cells) + " |"
        out.append(line)
    return "\n".join(out) + "\n"


with tempfile.TemporaryDirectory() as tmp:
    bl = Path(tmp) / "bl.md"
    bl.write_text(with_cells("o"), encoding="utf-8")
    r = run("--exercises", str(FIX / "good"), "--check-backlog", "--backlog", str(bl))
    check("backlog check rejects files whose cell is not X", r.returncode == 1 and "expected X" in r.stdout, r.stdout[-400:])
    bl.write_text(with_cells("X"), encoding="utf-8")
    r = run("--exercises", str(FIX / "good"), "--check-backlog", "--backlog", str(bl))
    check("backlog check passes when cells are X", r.returncode == 0, r.stdout[-400:])
    bl.write_text(with_cells("X").replace("| LFUN-02 | o |", "| LFUN-02 | X |", 1), encoding="utf-8")
    r = run("--exercises", str(FIX / "good"), "--check-backlog", "--backlog", str(bl))
    check("backlog check rejects X without files", r.returncode == 1 and "no items exist" in r.stdout, r.stdout[-400:])

# 5. the real bank and backlog agree
r = run("--check-backlog")
check("real bank verifies with --check-backlog", r.returncode == 0 and "VERIFY OK" in r.stdout, r.stdout[-400:])

# 6. seeds: one per phase 0-2 type, cell 's' and a Seed log row for each
seeds = {}
for p in (FIX / "good").glob("*/*.json"):
    for it in json.loads(p.read_text(encoding="utf-8"))["items"]:
        if it["provenance"]["template"] == "seed":
            seeds.setdefault(it["type"], []).append((p.parent.name, it["id"]))
check("one seed item per phase 0-2 type", sorted(seeds) == sorted(SEED_TYPES) and all(len(v) == 1 for v in seeds.values()), str(seeds))
for code, [(tid, iid)] in sorted(seeds.items()):
    check(f"seed {iid}: matrix cell is 's'", rows.get(tid, {}).get(code) == "s", str(rows.get(tid, {}).get(code)))
    check(f"seed {iid}: Seed row in the log", re.search(rf"^\| [0-9-]+ \| {tid} \| {code} \| {iid} \|.*\| Seed \|", raw, re.M) is not None)

# 7. build_bank: drafts are hidden by default and served with --include-draft
with tempfile.TemporaryDirectory() as tmp:
    out = Path(tmp)
    build = lambda *a: run("--exercises", str(FIX / "good"), "--out", tmp, *a, script="build_bank.py")
    r = build()
    bank = json.loads((out / "bank.json").read_text(encoding="utf-8"))
    check("build_bank serves no drafts by default", r.returncode == 0 and bank["counts"]["items"] == 0
          and bank["counts"]["skipped_by_status"] == {"draft": GOOD_ITEMS}, r.stdout + r.stderr)
    r = build("--include-draft")
    bank = json.loads((out / "bank.json").read_text(encoding="utf-8"))
    index = json.loads((out / "index.json").read_text(encoding="utf-8"))
    ids = [i["id"] for i in bank["items"]]
    check(f"build_bank --include-draft serves {GOOD_ITEMS} items sorted by id", bank["counts"]["items"] == GOOD_ITEMS and ids == sorted(ids), str(ids))
    check("bank schema_version is lukio-1.0", bank["schema_version"] == "lukio-1.0", bank["schema_version"])
    check("index has the lukio groups", {"by_lops", "by_module", "by_syllabus", "by_misconception", "by_type"} <= set(index), str(sorted(index)))
    check("index groups by LOPS goal", index["by_lops"].get("MAA2.05") == ["LU-LEQU-01-ES-001", "LU-LEQU-01-RP-001", "LU-LEQU-02-SO-001"], str(index["by_lops"].get("MAA2.05")))
    check("index groups by module", index["by_module"].get("MAB4") == ["LU-LEXP-04-FS-001"] and len(index["by_module"].get("MAA2", [])) == 5, str(index["by_module"]))
    check("index groups by syllabus", index["by_syllabus"].get("MAB") == ["LU-LEXP-04-FS-001", "LU-LPRB-01-MC-001"], str(index["by_syllabus"]))
    check("index groups by misconception, secondary tags too", index["by_misconception"].get("ALG-11") == ["LU-LINT-01-NE-001"], str(index["by_misconception"].get("ALG-11")))
    check("index groups by type", len(index["by_type"].get("NE", [])) == 7, str(index["by_type"]))
    check("index groups by topic without the LU- prefix", "LTRI-01" in index["by_topic"], str(sorted(index["by_topic"])))
    mc = next(i for i in bank["items"] if i["type"] == "MC")
    check("MC item gets telegram_poll flag", mc["flags"]["telegram_poll"] is True and mc["flags"]["needs_cas"] is False, str(mc["flags"]))
    first = (out / "bank.json").read_text(encoding="utf-8")
    build("--include-draft")
    check("build_bank output is deterministic", first == (out / "bank.json").read_text(encoding="utf-8"))
    r = run("--exercises", str(FIX / "bad" / "schema_old_curriculum"), "--out", tmp, "--include-draft", script="build_bank.py")
    check("build_bank refuses an item that fails the schema", r.returncode != 0 and "fails the schema" in r.stderr, r.stderr[-300:])

# 8. --base: existing items are immutable, new items must be draft (needs git)
if shutil.which("git"):
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "lukio"
        shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns("__pycache__", "build", ".git", "exercises"))
        shutil.copytree(FIX / "good", work / "exercises")
        g = lambda *a: subprocess.run(["git", *a], cwd=work, capture_output=True, text=True)
        g("init", "-q")
        g("config", "user.email", "test@example.com")
        g("config", "user.name", "test")
        g("add", "-A")
        g("commit", "-qm", "base")
        r = run("--base", "HEAD", cwd=work)
        check("--base: unchanged bank passes", r.returncode == 0, r.stdout[-400:])

        p = work / "exercises" / "LEQU-01" / "ES.json"
        doc = json.loads(p.read_text(encoding="utf-8"))
        doc["items"][0]["prompt"]["text"] = "Muutettu teksti."
        p.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        r = run("--base", "HEAD", cwd=work)
        check("--base: modified existing item is rejected", r.returncode == 1 and "was modified" in r.stdout, r.stdout[-400:])
        g("checkout", "--", "exercises")

        doc = json.loads(p.read_text(encoding="utf-8"))
        new = json.loads(json.dumps(doc["items"][0]))
        new["id"] = "LU-LEQU-01-ES-002"
        new["prompt"]["text"] = "Napauta rivi, jossa on virhe."
        new["payload"]["lines"] = ["x² = 5x", "x = 5", "x − 5 = 0"]
        new["status"] = "approved"
        doc["items"].append(new)
        p.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        r = run("--base", "HEAD", cwd=work)
        check("--base: new item with status approved is rejected", r.returncode == 1 and "must be draft" in r.stdout, r.stdout[-400:])
        new["status"] = "draft"
        p.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        r = run("--base", "HEAD", cwd=work)
        check("--base: new draft item passes", r.returncode == 0 and f"{GOOD_ITEMS + 1} item(s)" in r.stdout, r.stdout[-400:])
else:
    print("SKIP  git not available: --base tests skipped")

print()
if failures:
    print(f"{len(failures)} test(s) FAILED")
    sys.exit(1)
print("All tests passed")
