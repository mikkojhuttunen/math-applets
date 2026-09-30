#!/usr/bin/env python3
"""Self-test for verify.py and build_bank.py.  Run from anywhere:
    python tests/run_tests.py
Exit code 0 means every check behaved as expected."""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIX = ROOT / "tests" / "fixtures"
BACKLOG = "math-misconceptions-7-9grades-backlog.md"
sys.path.insert(0, str(ROOT / "scripts"))
import verify  # noqa: E402

failures = []


def run(script, *args, cwd=ROOT):
    return subprocess.run([sys.executable, str(cwd / "scripts" / script), *args], capture_output=True, text=True, cwd=cwd)


def check(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + ("" if ok else f"  -> {detail}"))
    if not ok:
        failures.append(name)


# 0. the kit is complete: requirements.txt exists and names every third-party import
req = ROOT / "requirements.txt"
check("requirements.txt exists", req.exists())
if req.exists():
    text = req.read_text(encoding="utf-8").lower()
    for pkg in ("sympy", "jsonschema"):
        check(f"requirements.txt lists {pkg}", pkg in text)
for rel in ("schema/item.schema.json", "scripts/verify.py", "scripts/build_bank.py", "README.md", "ROUTINE_PROMPT.md", BACKLOG):
    check(f"file present: {rel}", (ROOT / rel).exists())

# 1. good fixtures pass
r = run("verify.py", "--exercises", str(FIX / "good"))
check("good fixtures verify OK", r.returncode == 0 and "VERIFY OK: 9 item(s)" in r.stdout, r.stdout[-300:])

# 2. every bad fixture fails with its expected message
EXPECT = {
    "es_no_error": "no error was injected",
    "ne_wrong_is_right": "actually equivalent",
    "me_flag_wrong": "equivalent flag",
    "so_bad_line": "not equivalent to line 1",
    "bad_curriculum": "not linked to topic",
    "bad_schema": "schema:",
    "mc_no_tag": "no wrong option is tagged",
    "rp_bad_valid": "does not behave as valid",
    "duplicate_id": "duplicate id",
    "unverified": "verified is false",
    "fs_bad_solutions": "answer.solutions does not match",
}
for case, needle in EXPECT.items():
    r = run("verify.py", "--exercises", str(FIX / "bad" / case))
    check(f"bad fixture '{case}' is rejected", r.returncode == 1 and needle in r.stdout, r.stdout[-300:])
on_disk = {p.name for p in (FIX / "bad").iterdir()}
check("every bad fixture has an expectation", on_disk == set(EXPECT), str(on_disk ^ set(EXPECT)))

# 2b. S-IDs are checked against the OPS file when one is available
with tempfile.TemporaryDirectory() as tmp:
    ops = Path(tmp) / "ops.md"
    ops.write_text("| S3.05 | test | 7 | T14 |\n", encoding="utf-8")
    r = run("verify.py", "--exercises", str(FIX / "good"), "--ops", str(ops))
    check("S-ID missing from the OPS file is rejected", r.returncode == 1 and "does not exist in the OPS file" in r.stdout, r.stdout[-300:])

# 3. backlog cross-check: cells 'o' with files present must fail, cells 'X' must pass
text = (ROOT / BACKLOG).read_text(encoding="utf-8")
r = run("verify.py", "--exercises", str(FIX / "good"), "--check-backlog")
check("backlog check rejects files whose cell is not X", r.returncode == 1 and "expected X" in r.stdout, r.stdout[-300:])

codes, rows = verify.parse_matrix(text)
lines = text.splitlines()
have = {(p.parent.name, p.stem) for p in (FIX / "good").glob("*/*.json")}
out, in_matrix = [], False
for line in lines:
    if line.startswith("| ID | MC |"):
        in_matrix = True
    elif in_matrix and not line.startswith("|"):
        in_matrix = False
    if in_matrix and line.split("|")[1].strip() in rows:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        for i, code in enumerate(codes):
            if (cells[0], code) in have:
                cells[i + 1] = "X"
        line = "| " + " | ".join(cells) + " |"
    out.append(line)
with tempfile.TemporaryDirectory() as tmp:
    bl = Path(tmp) / "bl.md"
    bl.write_text("\n".join(out) + "\n", encoding="utf-8")
    r = run("verify.py", "--exercises", str(FIX / "good"), "--check-backlog", "--backlog", str(bl))
    check("backlog check passes when cells are X", r.returncode == 0, r.stdout[-300:])
    # an X without files must fail
    bl2 = Path(tmp) / "bl2.md"
    bl2.write_text("\n".join(out).replace("| ALG-01 | o |", "| ALG-01 | X |", 1) + "\n", encoding="utf-8")
    r = run("verify.py", "--exercises", str(FIX / "good"), "--check-backlog", "--backlog", str(bl2))
    check("backlog check rejects X without files", r.returncode == 1 and "no items exist" in r.stdout, r.stdout[-300:])

# 4. build_bank: drafts are hidden by default and served with --include-draft
with tempfile.TemporaryDirectory() as tmp:
    r = run("build_bank.py", "--exercises", str(FIX / "good"), "--out", tmp)
    bank = json.loads((Path(tmp) / "bank.json").read_text(encoding="utf-8"))
    check("build_bank serves no drafts by default", r.returncode == 0 and bank["counts"]["items"] == 0 and bank["counts"]["skipped_by_status"] == {"draft": 9}, r.stdout)
    r = run("build_bank.py", "--exercises", str(FIX / "good"), "--out", tmp, "--include-draft")
    bank = json.loads((Path(tmp) / "bank.json").read_text(encoding="utf-8"))
    index = json.loads((Path(tmp) / "index.json").read_text(encoding="utf-8"))
    ids = [i["id"] for i in bank["items"]]
    check("build_bank --include-draft serves 9 items sorted by id", bank["counts"]["items"] == 9 and ids == sorted(ids), str(ids))
    mc = next(i for i in bank["items"] if i["type"] == "MC")
    check("MC item gets telegram_poll flag", mc["flags"]["telegram_poll"] is True, str(mc["flags"]))
    check("index groups by OPS goal", index["by_ops"]["S3.05"] == ["ALG-07-ES-001", "ALG-07-FS-001", "ALG-07-RP-001"], str(index["by_ops"].get("S3.05")))
    first = (Path(tmp) / "bank.json").read_text(encoding="utf-8")
    run("build_bank.py", "--exercises", str(FIX / "good"), "--out", tmp, "--include-draft")
    check("build_bank output is deterministic", first == (Path(tmp) / "bank.json").read_text(encoding="utf-8"))

# 5. --base: existing items are immutable, new items must be draft (needs git)
if shutil.which("git"):
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "math-misconceptions"
        shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns("__pycache__", "build", ".git"))
        shutil.rmtree(work / "exercises")
        shutil.copytree(FIX / "good", work / "exercises")
        g = lambda *a: subprocess.run(["git", *a], cwd=work, capture_output=True, text=True)
        g("init", "-q")
        g("config", "user.email", "test@example.com")
        g("config", "user.name", "test")
        g("add", "-A")
        g("commit", "-qm", "base")
        ok = run("verify.py", "--base", "HEAD", cwd=work)
        check("--base: unchanged bank passes", ok.returncode == 0, ok.stdout[-300:])

        p = work / "exercises" / "ALG-07" / "ES.json"
        doc = json.loads(p.read_text(encoding="utf-8"))
        doc["items"][0]["prompt"]["text"] = "Muutettu teksti."
        p.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        r = run("verify.py", "--base", "HEAD", cwd=work)
        check("--base: modified existing item is rejected", r.returncode == 1 and "was modified" in r.stdout, r.stdout[-300:])
        g("checkout", "--", "exercises")

        new = json.loads(json.dumps(doc["items"][0]))
        new["id"] = "ALG-07-ES-002"
        new["prompt"]["text"] = "Napauta virheellinen rivi."
        new["payload"]["lines"] = ["7 − 3x = 10", "−3x = 10 − 7", "−3x = 3", "x = 1"]
        new["status"] = "approved"
        doc = json.loads(p.read_text(encoding="utf-8"))
        doc["items"].append(new)
        p.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        r = run("verify.py", "--base", "HEAD", cwd=work)
        check("--base: new item with status approved is rejected", r.returncode == 1 and "must be draft" in r.stdout, r.stdout[-300:])
        new["status"] = "draft"
        p.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        r = run("verify.py", "--base", "HEAD", cwd=work)
        check("--base: new draft item passes", r.returncode == 0 and "10 item(s)" in r.stdout, r.stdout[-300:])
else:
    print("SKIP  git not available: --base tests skipped")

# 6. the reference generator produces items that pass verification
with tempfile.TemporaryDirectory() as tmp:
    gen = subprocess.run([sys.executable, str(ROOT / "generators" / "example_alg08_ne.py")], capture_output=True, text=True)
    items = json.loads(gen.stdout)
    d = Path(tmp) / "ALG-08"
    d.mkdir()
    (d / "NE.json").write_text(json.dumps({"schema_version": "1.0", "topic": "ALG-08", "type": "NE", "items": items}, ensure_ascii=False), encoding="utf-8")
    r = run("verify.py", "--exercises", tmp)
    check("reference generator output verifies", gen.returncode == 0 and r.returncode == 0 and "5 item(s)" in r.stdout, r.stdout[-300:])

print()
if failures:
    print(f"{len(failures)} test(s) FAILED")
    sys.exit(1)
print("All tests passed")
