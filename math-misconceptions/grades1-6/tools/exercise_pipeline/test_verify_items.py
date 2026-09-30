"""Run from the repository root:  python -m unittest discover -s tools/exercise_pipeline"""
import copy
import json
import os
import tempfile
import unittest

import from_buggy_rules as fb
import verify_items as v

GOALS = v.load_goals()


def dump(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False)

GOOD = {
    "id": "A12.S2.08-x-001", "goal": "A12.S2.08", "level": "V", "type": "numeric_entry",
    "stem_fi": "Laske 8 + 6.", "answer": "14", "answer_expr": "8 + 6",
    "source": "generated", "status": "draft",
}


class Verifier(unittest.TestCase):
    def test_good_item_passes(self):
        self.assertEqual(v.check_item(GOOD, GOALS), [])

    def test_wrong_answer_key_is_caught(self):
        bad = dict(GOOD, answer="15")
        self.assertTrue(any("does not equal" in e for e in v.check_item(bad, GOALS)))

    def test_decimal_comma_arithmetic(self):
        it = dict(GOOD, goal="A36.S2.14", level="T", stem_fi="Laske 0,5 + 0,25.", answer="0,75", answer_expr="0.5 + 0.25")
        self.assertEqual(v.check_item(it, GOALS), [])

    def test_decimal_point_in_stem_is_caught(self):
        it = dict(GOOD, goal="A36.S2.14", level="T", stem_fi="Laske 0.5 + 0.25.", answer="0,75", answer_expr="0.5 + 0.25")
        self.assertTrue(any("decimal comma" in e for e in v.check_item(it, GOALS)))

    def test_unknown_goal_and_level(self):
        self.assertTrue(any("not in the OPS_1-6" in e for e in v.check_item(dict(GOOD, goal="A36.S9.99"), GOALS)))
        self.assertTrue(any("level" in e for e in v.check_item(dict(GOOD, level="K"), GOALS)))

    def test_reviewed_status_is_blocked(self):
        self.assertTrue(any("draft" in e for e in v.check_item(dict(GOOD, status="reviewed"), GOALS)))
        self.assertEqual(v.check_item(dict(GOOD, status="reviewed"), GOALS, allow_reviewed=True), [])

    def test_pupil_data_is_blocked(self):
        self.assertTrue(any("unknown fields" in e for e in v.check_item(dict(GOOD, pupil_name="Aino"), GOALS)))
        self.assertTrue(any("email" in e for e in v.check_item(dict(GOOD, notes="mail aino@koulu.fi"), GOALS)))
        self.assertTrue(any("identity code" in e for e in v.check_item(dict(GOOD, notes="010107A123B"), GOALS)))

    def test_code_in_expression_is_rejected(self):
        for expr in ("__import__('os').system('echo x')", "open('f')", "[1][0]", "2**99999", "1/0"):
            with self.assertRaises(ValueError, msg=expr):
                v.eval_expr(expr)

    def test_misconception_answer_must_differ(self):
        it = dict(GOOD, misconceptions={"NUM-99a": {"answer": "14"}})
        self.assertTrue(any("equals the correct" in e for e in v.check_item(it, GOALS)))

    def test_choice_item(self):
        it = {"id": "c1", "goal": "A36.S2.11", "level": "P", "type": "choice", "stem_fi": "Kumpi on suurempi?",
              "options": ["1/4", "1/8"], "answer": "1/4", "source": "template", "status": "draft",
              "misconceptions": {"NUM-12": {"answer": "1/8"}}}
        self.assertEqual(v.check_item(it, GOALS), [])
        it["answer"] = "1/3"
        self.assertTrue(v.check_item(it, GOALS))

    def test_duplicates_across_files(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = os.path.join(d, "a.json"), os.path.join(d, "b.json")
            dump([GOOD], a)
            dump([copy.deepcopy(GOOD)], b)
            self.assertTrue(v.check_files([a, b], GOALS))
            self.assertEqual(v.check_files([a], GOALS), {})


class GeneratedBatch(unittest.TestCase):
    def test_batch_from_templates_passes_verifier(self):
        batch = fb.make_batch(30, 12345, "t")
        self.assertEqual(len(batch), 30)
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "batch.json")
            dump(batch, path)
            self.assertEqual(v.check_files([path], GOALS), {})

    def test_new_batch_avoids_existing_stems(self):
        first = fb.make_batch(30, 7, "a")
        stems = {" ".join(i["stem_fi"].split()).lower() for i in first}
        second = fb.make_batch(30, 8, "b", stems)
        self.assertFalse(stems & {" ".join(i["stem_fi"].split()).lower() for i in second})

    def test_tampered_batch_fails(self):
        batch = fb.make_batch(6, 1, "t")
        batch[0]["answer"] = "0"
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "batch.json")
            dump(batch, path)
            self.assertTrue(v.check_files([path], GOALS))


if __name__ == "__main__":
    unittest.main()
