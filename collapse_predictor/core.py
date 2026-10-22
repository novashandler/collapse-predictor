"""Frozen adjudication rule. No training, no thresholds learned at runtime.

Provenance of the constants (each verifiable on disk):
- THRESHOLD 2.6: frozen from the 4-seed pilot (pilot collapses at F1 = 3.07 and
  3.55; healthy pilot seeds far below). Frozen BEFORE the 8-seed sweep, the
  16-seed scan2, and the 16-seed scan3 were run.
- Label rule: accB_final <= 0.20 collapsed / >= 0.25 healthy / else unresolved.
- 'correct' under the frozen rule: a seed is correct iff it is realized on a
  side (not 'unresolved') AND the prediction matched. This is the exact rule
  the sweep and scan3 harnesses used to report 7/8 and 14/16.
"""
from __future__ import annotations

from dataclasses import dataclass

THRESHOLD = 2.6  # frozen 2026-10-22; a change is a new pre-registration, not an edit


def predict(f1: float, threshold: float = THRESHOLD) -> str:
    """Frozen prediction: F1 above the threshold predicts the collapse regime."""
    return "collapsed" if f1 > threshold else "healthy"


def realized_label(acc_b: float) -> str:
    """Frozen realized-regime label from final B-phase accuracy."""
    if acc_b <= 0.20:
        return "collapsed"
    if acc_b >= 0.25:
        return "healthy"
    return "unresolved"


@dataclass(frozen=True)
class Verdict:
    seed: int
    f1: float
    acc_b: float
    predicted: str
    realized: str
    correct: bool


def adjudicate(seed: int, f1: float, acc_b: float, threshold: float = THRESHOLD) -> Verdict:
    """Apply the frozen rule to one seed's run metrics."""
    pred = predict(f1, threshold)
    real = realized_label(acc_b)
    correct = (real != "unresolved") and (pred == real)
    return Verdict(seed, f1, acc_b, pred, real, correct)
