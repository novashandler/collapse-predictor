"""collapse_predictor — frozen pre-collapse warning rule for wetware training runs.

The one-line rule, pre-registered and frozen BEFORE any adjudicated seed was run:

    F1  = post-A potent_max of the BCM probe (BCM-on, taken at the A->B boundary)
    PREDICT COLLAPSE  iff  F1 > THRESHOLD   (THRESHOLD = 2.6, frozen 2026-10-22)
    else predict healthy.

Realized label (frozen):
    accB_final <= 0.20  ->  collapsed
    accB_final >= 0.25  ->  healthy
    otherwise           ->  unresolved

Nothing in this package adapts its verdict to its inputs.
"""
try:  # installed / project-root layout
    from collapse_predictor.core import (
        THRESHOLD,
        Verdict,
        adjudicate,
        predict,
        realized_label,
    )
except ImportError:  # running from inside the repo (tests/, cwd=package)
    from core import (  # type: ignore
        THRESHOLD,
        Verdict,
        adjudicate,
        predict,
        realized_label,
    )

__all__ = ["THRESHOLD", "Verdict", "adjudicate", "predict", "realized_label"]
__version__ = "0.1.0"
