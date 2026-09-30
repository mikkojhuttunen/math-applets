"""Run from the pipeline root:  python -m unittest discover -s tools/buggy_rules"""
import random
import unittest
from fractions import Fraction

import buggy_rules as br


class Subtraction(unittest.TestCase):
    def test_453_minus_127(self):
        correct, bugs = br.subtraction_answers(453, 127)
        self.assertEqual(correct, 326)
        self.assertEqual(bugs, {"NUM-10a": 334, "NUM-10b": 324, "NUM-10c": 336})

    def test_minuend_must_be_larger(self):
        with self.assertRaises(ValueError):
            br.column_trace(127, 453)

    def test_diagnostic_filter(self):
        self.assertTrue(br.is_diagnostic_subtraction(453, 127))
        self.assertFalse(br.is_diagnostic_subtraction(302, 148), "subtrahend ends in 8")
        self.assertFalse(br.is_diagnostic_subtraction(76, 49), "subtrahend ends in 9")
        self.assertFalse(br.is_diagnostic_subtraction(456, 123), "no regrouping")
        self.assertFalse(br.is_diagnostic_subtraction(132, 125), "difference not over 10")
        self.assertFalse(br.is_diagnostic_subtraction(82, 27), "a bug gives the correct answer")

    def test_generated_items_are_diagnostic(self):
        rng = random.Random(20260930)
        for _ in range(200):
            item = br.make_subtraction_item(rng)
            m, s = item["params"]["minuend"], item["params"]["subtrahend"]
            self.assertTrue(br.is_diagnostic_subtraction(m, s))
            self.assertEqual(item["answer"], str(m - s))
            self.assertEqual(set(item["misconceptions"]), set(br.SUB_RULES))


class Fractions(unittest.TestCase):
    def test_generated_addition_items(self):
        rng = random.Random(1)
        for _ in range(200):
            item = br.make_fraction_add_item(rng)
            a, b, c, d = (item["params"][k] for k in "abcd")
            self.assertEqual(Fraction(item["answer"]), Fraction(a, b) + Fraction(c, d))
            self.assertEqual(Fraction(item["misconceptions"]["NUM-03"]["answer"]), Fraction(a + c, b + d))
            self.assertNotEqual(item["answer"], item["misconceptions"]["NUM-03"]["answer"])


class ParseAnswer(unittest.TestCase):
    def test_accepted_forms(self):
        cases = {"7": 7, "5/6": Fraction(5, 6), "10/12": Fraction(5, 6), "1 1/6": Fraction(7, 6),
                 "0,5": Fraction(1, 2), "0.5": Fraction(1, 2), " 326 ": 326,
                 "−3": -3, "−1 1/2": Fraction(-3, 2)}
        for text, value in cases.items():
            self.assertEqual(br.parse_answer(text), value, text)

    def test_unreadable_is_none(self):
        for text in ("", "abc", "1/0", "3,5,1", "1/2/3"):
            self.assertIsNone(br.parse_answer(text), text)


class Classify(unittest.TestCase):
    SUB = br.make_subtraction_item(random.Random(0))

    def setUp(self):
        self.item = dict(self.SUB, answer="326",
                         misconceptions={"NUM-10a": {"answer": "334"}, "NUM-10b": {"answer": "324"},
                                         "NUM-10c": {"answer": "336"}})

    def test_numeric(self):
        self.assertEqual(br.classify(self.item, "326"), {"status": "correct", "rules": []})
        self.assertEqual(br.classify(self.item, "334"), {"status": "matched", "rules": ["NUM-10a"]})
        self.assertEqual(br.classify(self.item, "336"), {"status": "matched", "rules": ["NUM-10c"]})
        self.assertEqual(br.classify(self.item, "999"), {"status": "unexplained", "rules": []})
        self.assertEqual(br.classify(self.item, "kolme"), {"status": "unparsed", "rules": []})

    def test_ambiguous(self):
        item = dict(self.item, misconceptions={"NUM-10a": {"answer": "334"}, "NUM-10b": {"answer": "334"}})
        self.assertEqual(br.classify(item, "334")["status"], "ambiguous")

    def test_equivalent_fraction_is_correct(self):
        item = {"type": "numeric_entry", "answer": "5/6", "misconceptions": {"NUM-03": {"answer": "2/5"}}}
        self.assertEqual(br.classify(item, "10/12")["status"], "correct")
        self.assertEqual(br.classify(item, "2/5"), {"status": "matched", "rules": ["NUM-03"]})

    def test_choice(self):
        item = {"type": "choice", "options": ["1/4", "1/8"], "answer": "1/4",
                "misconceptions": {"NUM-12": {"answer": "1/8"}}}
        self.assertEqual(br.classify(item, "1/4")["status"], "correct")
        self.assertEqual(br.classify(item, "1/8"), {"status": "matched", "rules": ["NUM-12"]})


if __name__ == "__main__":
    unittest.main()
