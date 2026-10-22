"""Tests bound to the EXACT per-seed data on disk (not re-derived from memory).

Sweep rows below are verbatim from the 8-seed regime sweep's own console output
(REGIME_SWEEP_99M; exit 0, 2026-10-22): seed, F1, accB, realized.
Expected frozen-rule score: 7/8 (seed 3 realized 'unresolved' counts wrong).
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))
from collapse_predictor import THRESHOLD, adjudicate, predict, realized_label  # noqa: E402

# (seed, F1, accB, realized) — verbatim from the sweep run output
SWEEP = [
    (1, 1.0442, 0.3426, "healthy"),
    (2, 1.0517, 0.3770, "healthy"),
    (3, 1.1508, 0.2136, "unresolved"),
    (4, 1.1230, 0.2725, "healthy"),
    (6, 1.0858, 0.3644, "healthy"),
    (7, 1.0100, 0.3313, "healthy"),
    (12, 1.0881, 0.3618, "healthy"),
    (13, 1.0613, 0.3690, "healthy"),
]


class TestFrozenRule(unittest.TestCase):
    def test_threshold_is_frozen(self):
        self.assertEqual(THRESHOLD, 2.6)

    def test_label_boundaries(self):
        self.assertEqual(realized_label(0.20), "collapsed")
        self.assertEqual(realized_label(0.2001), "unresolved")
        self.assertEqual(realized_label(0.2499), "unresolved")
        self.assertEqual(realized_label(0.25), "healthy")

    def test_predict_at_threshold(self):
        self.assertEqual(predict(2.6), "healthy")      # strictly above
        self.assertEqual(predict(2.6001), "collapsed")

    def test_sweep_reproduces_frozen_7_of_8(self):
        correct = 0
        for seed, f1, acc_b, realized in SWEEP:
            v = adjudicate(seed, f1, acc_b)
            self.assertEqual(v.realized, realized, f"seed {seed} realized label")
            if v.realized != "unresolved":
                self.assertEqual(v.predicted, v.realized, f"seed {seed} prediction")
            if v.correct:
                correct += 1
        self.assertEqual(correct, 7)  # seed 3 unresolved -> not correct, per frozen rule

    def test_pilot_collapses_detected(self):
        # Pilot (frozen scoreboard): both collapses flagged, F1 = 3.55 and 3.07.
        for f1, acc_b in [(3.55, 0.15), (3.07, 0.18)]:
            v = adjudicate(0, f1, acc_b)
            self.assertEqual((v.predicted, v.realized, v.correct),
                             ("collapsed", "collapsed", True))


if __name__ == "__main__":
    unittest.main()
