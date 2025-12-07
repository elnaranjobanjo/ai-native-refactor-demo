from __future__ import annotations

import copy

import pytest

from legacy.billing import handle as legacy_billing_handle

BILLING_CASES = [
    pytest.param(
        "product_with_discount",
        [
            {"type": "product", "price": 20, "qty": 2},
            {"type": "discount", "value": 5},
        ],
        id="product_with_discount",
    ),
    pytest.param(
        "service_and_product_mix",
        [
            {"type": "product", "price": 15, "qty": 1},
            {"type": "service", "hours": 3, "rate": 40},
        ],
        id="service_and_product_mix",
    ),
    pytest.param(
        "unknown_items_ignored",
        [
            {"type": "product", "price": 5, "qty": 2},
            {"type": "mystery", "foo": 1},
        ],
        id="unknown_items_ignored",
    ),
    pytest.param(
        "zero_subtotal_still_taxed",
        [
            {"type": "product", "price": 10, "qty": 1},
            {"type": "discount", "value": 10},
        ],
        id="zero_subtotal_still_taxed",
    ),
]


@pytest.mark.parametrize(("scenario_name", "items"), BILLING_CASES)
def test_billing_totals_match_legacy(billing_entry_points, scenario_name, items):
    expected_total = legacy_billing_handle(copy.deepcopy(items))

    legacy_total = billing_entry_points["legacy"](items)
    refactored_total = billing_entry_points["refactored"](items)

    assert legacy_total == pytest.approx(expected_total), scenario_name
    assert refactored_total == pytest.approx(expected_total), scenario_name


def test_billing_unknown_items_do_not_affect_totals(billing_entry_points):
    base_items = [
        {"type": "product", "price": 12, "qty": 1},
        {"type": "discount", "value": 2},
    ]
    noisy_items = base_items + [{"type": "not-real", "value": 999}]

    baseline = legacy_billing_handle(copy.deepcopy(base_items))
    with_noise = legacy_billing_handle(copy.deepcopy(noisy_items))
    assert with_noise == pytest.approx(baseline)

    assert billing_entry_points["legacy"](noisy_items) == pytest.approx(baseline)
    assert billing_entry_points["refactored"](noisy_items) == pytest.approx(baseline)
