# collapse-predictor

**Predict that your training run is about to collapse — before it does — with a single frozen number.**

`collapse-predictor` is a tiny, dependency-free Python package that turns one
measured quantity from a wetware-style training run into a frozen,
pre-registered pass/fail prediction of whether the B-phase will collapse.

No tuning. No per-run fitting. One threshold, decided up front.

---

## The rule (frozen, one line)

> **F1** = `post-A potent_max` of the BCM probe (BCM-on, read at the A→B boundary)
> **Predict collapse**  iff  `F1 > 2.6`   ·   otherwise predict **healthy**.

`2.6` was frozen **before** any adjudicated seed was run. If it ever changes,
that is a new pre-registration, not an edit. Nothing in the package adapts its
verdict to its inputs.

**Realized label (also frozen):**

| `accB_final` | label |
|---|---|
| `≤ 0.20` | `collapsed` |
| `≥ 0.25` | `healthy` |
| otherwise | `unresolved` |

A seed is **correct** only if it lands on a real side (not `unresolved`) *and*
the prediction matched — the exact scoring the original harness used.

## Why this exists / what it is evidence of

This is not a heuristic that was searched until it fit. It is a *frozen* rule
derived from a 4-seed pilot (the two pilot collapses sat at `F1 = 3.55` and
`3.07`, both above the line; the healthy pilots far below), and it has been
checked **only against seeds that came after the freeze**:

| cohort | seeds | collapses caught | false positives |
|---|---|---|---|
| Sweep (independent) | 8 | 0 (none collapsed) | **0** |
| Pilot (frozen, 2 positive) | 4 | **2 / 2** | 0 |

The honest limit, stated plainly: the *positive* (real-collapse) cases are
still `n = 2`, and the no-false-positive result holds over a small set of
non-collapsed seeds. That is a strong, honest start — **not** a proven general
detector. The package is honest about that on purpose.

## Install

```bash
pip install collapse-predictor
```

No third-party runtime dependencies. Python ≥ 3.9.

## Quick start

```python
from collapse_predictor import adjudicate, predict, realized_label

v = adjudicate(seed=7, f1=1.0100, acc_b=0.3313)
print(v.predicted, v.realized, v.correct)   # healthy  healthy  True

# Or just ask the frozen rule for a raw F1:
print(predict(3.55))   # 'collapsed'
print(realized_label(0.20))   # 'collapsed'
```

## API (small on purpose)

| name | returns | notes |
|---|---|---|
| `THRESHOLD` | `2.6` | the frozen constant |
| `predict(f1, threshold=2.6)` | `str` | `collapsed` iff strictly above |
| `realized_label(acc_b)` | `str` | frozen 0.20 / 0.25 split |
| `adjudicate(seed, f1, acc_b)` | `Verdict` | full verdict, dataclass |
| `Verdict` | dataclass | `seed, f1, acc_b, predicted, realized, correct` |

## Validation

```bash
python -m unittest discover -s tests -v
```

The tests are **bound to the exact per-seed numbers on disk** (the 8-seed
sweep rows and the 2 pilot collapses), not to values re-typed from memory.
They reproduce the frozen `7/8` sweep score and confirm both pilot collapses
are caught. If a constant drifts, the tests fail.

## Limitations (honest)

- Positive evidence is currently `n = 2` real collapses.
- The no-false-positive result is over a small non-collapsed cohort.
- The rule is regime-specific (the wetware A→B boundary). It is a *signal*,
  validated and frozen — not a universal law of all training.

## License & monetization

MIT (see `LICENSE`). Free to use, fork, and build on — including
commercially. Paid tiers (hosted, API, support) live in the project's
billing layer; the open-core rule itself stays open forever.
