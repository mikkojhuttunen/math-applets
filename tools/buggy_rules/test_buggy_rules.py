"""Run with:  python -m unittest test_buggy_rules -v"""
import random
import unittest
from fractions import Fraction

from buggy_rules import (SUB_RULES, Tally, check_tap, classify, column_trace,
                         is_diagnostic_subtraction, make_fraction_add_error_item,
                         make_fraction_add_item, make_fraction_compare_item,
                         make_subtraction_error_item, make_subtraction_item,
                         parse_answer, subtraction_answers, trace_value)


class PublishedExamples(unittest.TestCase):
    """Worked examples printed in Vermeulen et al. (2020, Frontiers in Education 5:537531)."""

    def test_347_minus_62(self):
        correct, bugs = subtraction_answers(347, 62)
        self.assertEqual(correct, 285)
        self.assertEqual(bugs, {"NUM-10a": 325, "NUM-10b": 225, "NUM-10c": 385})

    def test_43_minus_17(self):
        correct, bugs = subtraction_answers(43, 17)
        self.assertEqual(correct, 26)
        self.assertEqual(bugs, {"NUM-10a": 34, "NUM-10b": 24, "NUM-10c": 36})

    def test_76_minus_48_smaller_from_larger_is_32(self):
        self.assertEqual(subtraction_answers(76, 48)[1]["NUM-10a"], 32)

    def test_82_minus_27_is_not_diagnostic(self):
        # regrouping gives 5 and so does reversing 7 - 2, so a bug can yield the right answer
        self.assertFalse(is_diagnostic_subtraction(82, 27))
        self.assertEqual(subtraction_answers(82, 27)[1]["NUM-10b"], 55)  # 82-27 = 55

    def test_item_bank_item(self):
        correct, bugs = subtraction_answers(453, 127)
        self.assertEqual((correct, bugs["NUM-10a"], bugs["NUM-10b"], bugs["NUM-10c"]),
                         (326, 334, 324, 336))
        self.assertTrue(is_diagnostic_subtraction(453, 127))

    def test_old_item_302_minus_148(self):
        correct, bugs = subtraction_answers(302, 148)
        self.assertEqual((correct, bugs["NUM-10a"]), (154, 246))
        self.assertFalse(is_diagnostic_subtraction(302, 148))  # subtrahend ends in 8


class SubtractionProperties(unittest.TestCase):
    def test_impossible_sizes_are_rejected(self):
        with self.assertRaises(ValueError):
            make_subtraction_item(random.Random(0), 2, 3)

    def test_correct_trace_always_equals_python_subtraction(self):
        rng = random.Random(1)
        for _ in range(3000):
            m = rng.randint(11, 9999)
            s = rng.randint(1, m - 1)
            self.assertEqual(trace_value(column_trace(m, s)), m - s)

    def test_generated_items_meet_constraints(self):
        rng = random.Random(2)
        for nm, ns in [(2, 2), (3, 2), (3, 3), (4, 3)]:
            for _ in range(200):
                it = make_subtraction_item(rng, nm, ns)
                m, s = it["params"]["minuend"], it["params"]["subtrahend"]
                self.assertTrue(is_diagnostic_subtraction(m, s))
                answers = [it["answer"]] + [v["answer"] for v in it["misconceptions"].values()]
                self.assertEqual(len(set(answers)), 4)

    def test_classifier_recovers_the_injected_rule(self):
        rng = random.Random(3)
        for _ in range(500):
            it = make_subtraction_item(rng, *rng.choice([(2, 2), (3, 2), (3, 3)]))
            m, s = it["params"]["minuend"], it["params"]["subtrahend"]
            if m <= s:
                continue
            for r in SUB_RULES:
                res = classify(it, str(trace_value(column_trace(m, s, r))))
                self.assertEqual(res, {"status": "matched", "rules": [r]})
            self.assertEqual(classify(it, it["answer"])["status"], "correct")
            self.assertEqual(classify(it, "1")["status"], "unexplained")

    def test_error_spotting_lines(self):
        rng = random.Random(4)
        for _ in range(300):
            it = make_subtraction_item(rng, 3, 3)
            m, s = it["params"]["minuend"], it["params"]["subtrahend"]
            for r in SUB_RULES:
                e = make_subtraction_error_item(m, s, r)
                self.assertEqual(len(e["lines_fi"]), len(e["solution_lines_fi"]))
                i = e["faulty_line"]
                self.assertNotEqual(e["lines_fi"][i], e["solution_lines_fi"][i])
                self.assertEqual(e["lines_fi"][:i], e["solution_lines_fi"][:i])
                self.assertLess(i, len(e["lines_fi"]) - 1)  # never only the answer line

    def test_tap_feedback(self):
        e = make_subtraction_error_item(453, 127, "NUM-10c")
        self.assertEqual(e["faulty_line"], 1)   # the tens line uses the unreduced 5
        self.assertTrue(check_tap(e, 1)["correct"])
        self.assertEqual(check_tap(e, 3), {"correct": False, "missed_error_tag": "NUM-10c",
                                           "tap_kind": "after_error"})


class Fractions(unittest.TestCase):
    def test_published_example_1_4_plus_1_3(self):
        # Van Hoof et al. (2025) abstract gives 1/4 + 1/3 = 2/7 as the natural-number-bias answer
        self.assertEqual(Fraction(1, 4) + Fraction(1, 3), Fraction(7, 12))
        self.assertEqual(Fraction(1 + 1, 4 + 3), Fraction(2, 7))

    def test_generated_addition_items(self):
        rng = random.Random(5)
        for _ in range(300):
            it = make_fraction_add_item(rng)
            p = it["params"]
            bug = Fraction(p["a"] + p["c"], p["b"] + p["d"])
            self.assertNotEqual(bug, Fraction(it["answer"]))
            self.assertEqual(classify(it, str(bug)), {"status": "matched", "rules": ["NUM-03"]})
            # equivalent unsimplified form is still the same rule
            self.assertEqual(classify(it, f"{bug.numerator * 2}/{bug.denominator * 2}")["rules"], ["NUM-03"])
            self.assertEqual(classify(it, it["answer"])["status"], "correct")

    def test_fraction_error_spotting(self):
        e = make_fraction_add_error_item(random.Random(6))
        self.assertEqual(e["faulty_line"], 1)
        self.assertNotEqual(e["lines_fi"][1], e["solution_lines_fi"][1])

    def test_compare_item(self):
        rng = random.Random(7)
        for _ in range(100):
            it = make_fraction_compare_item(rng)
            b, d = it["params"]["b"], it["params"]["d"]
            self.assertEqual(it["answer"], f"1/{min(b, d)}")
            self.assertIn(f"1/{b}", it["stem_fi"])  # the stem names both fractions, so stems are unique
            self.assertEqual(classify(it, f"1/{max(b, d)}"), {"status": "matched", "rules": ["NUM-12"]})


class Parsing(unittest.TestCase):
    def test_forms(self):
        self.assertEqual(parse_answer("0,5"), Fraction(1, 2))
        self.assertEqual(parse_answer("1 1/6"), Fraction(7, 6))
        self.assertEqual(parse_answer("10/12"), Fraction(5, 6))
        self.assertIsNone(parse_answer("kolme"))
        self.assertIsNone(parse_answer("1/0"))


class TallyGuard(unittest.TestCase):
    def test_needs_two_different_items(self):
        t = Tally(min_items=2)
        t.add("i1", {"status": "matched", "rules": ["NUM-10a"]})
        t.add("i1", {"status": "matched", "rules": ["NUM-10a"]})  # same item twice
        self.assertEqual(t.flags(), [])
        t.add("i2", {"status": "matched", "rules": ["NUM-10a"]})
        self.assertEqual(t.flags(), ["NUM-10a"])


if __name__ == "__main__":
    unittest.main()
