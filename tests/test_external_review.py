"""An external review (25.10): a description with a missing button_fully_visible, or "false" as a string, gave PASS -
only the bool False was noticed. Red on 0.1.0."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import vision_judge as vj  # noqa: E402

SPEC = {"title": "Checkout", "fields": ["Name"], "button": "Buy", "items": ["A"]}


def inv(**over):
    d = {"title": "Checkout", "labels": ["Name"], "button": "Buy", "button_fully_visible": True,
         "list_items": ["A"], "problems_seen": []}
    d.update(over)
    return {k: v for k, v in d.items() if v is not ...}


class Schema(unittest.TestCase):
    def test_a_complete_matching_description_passes(self):
        self.assertEqual(vj.judge(SPEC, inv())[0], "PASS")

    def test_a_missing_visibility_flag_is_not_a_pass(self):
        v, why = vj.judge(SPEC, inv(button_fully_visible=...))
        self.assertEqual(v, "REVIEW")
        self.assertTrue(any("button_fully_visible" in w for w in why), why)

    def test_false_as_a_string_is_not_a_pass(self):
        v, why = vj.judge(SPEC, inv(button_fully_visible="false"))
        self.assertEqual(v, "REVIEW")

    def test_wrong_types_and_missing_keys_are_review(self):
        for bad in (inv(labels="Name"), inv(list_items=...), inv(problems_seen=None), inv(title=7),
                    inv(problems_seen="none")):
            with self.subTest(bad=bad):
                self.assertEqual(vj.judge(SPEC, bad)[0], "REVIEW")

    def test_a_real_difference_still_fails(self):
        self.assertEqual(vj.judge(SPEC, inv(button="Pay"))[0], "FAIL")
        self.assertEqual(vj.judge(SPEC, inv(button_fully_visible=False))[0], "FAIL")


if __name__ == "__main__":
    unittest.main()
