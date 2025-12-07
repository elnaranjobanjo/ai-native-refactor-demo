from __future__ import annotations

import copy
import pathlib
import sys
from typing import Callable, Iterable, Mapping, Sequence

import pytest

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from legacy.billing import handle as legacy_billing_handle
from legacy.subscriptions import handle_subscriptions as legacy_subscriptions_handle
from refactored.billing_refactor import compute as billing_compute_module
from refactored.subscriptions_refactor import compute as subscriptions_compute_module

ItemPayload = Sequence[Mapping[str, object]]
Runner = Callable[[ItemPayload], float]


def _clone_items(items: Iterable[Mapping[str, object]]) -> list[dict[str, object]]:
    return [copy.deepcopy(item) for item in items]


def _wrap_runner(fn: Runner) -> Runner:
    def _runner(items: ItemPayload) -> float:
        return fn(_clone_items(items))

    return _runner


@pytest.fixture(scope="session")
def billing_entry_points() -> dict[str, Runner]:
    compute_bill = getattr(billing_compute_module, "compute_bill", None)
    billing_future = compute_bill or billing_compute_module.handle

    return {
        "legacy": _wrap_runner(legacy_billing_handle),
        "refactored": _wrap_runner(billing_future),
    }


@pytest.fixture(scope="session")
def subscriptions_entry_points() -> dict[str, Runner]:
    compute_total = getattr(subscriptions_compute_module, "compute_total", None)
    subscriptions_future = compute_total or subscriptions_compute_module.handle

    return {
        "legacy": _wrap_runner(legacy_subscriptions_handle),
        "refactored": _wrap_runner(subscriptions_future),
    }
