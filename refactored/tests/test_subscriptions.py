from __future__ import annotations

import copy

import pytest

from legacy.subscriptions import handle_subscriptions as legacy_subscriptions_handle

SUBSCRIPTION_CASES = [
    pytest.param(
        "basic_plan_with_overage",
        [
            {
                "type": "plan",
                "seats": 5,
                "price_per_seat": 10,
                "active_users": 6,
                "overage_charge": 4,
            },
            {"type": "coupon", "amount": 5},
        ],
        id="basic_plan_with_overage",
    ),
    pytest.param(
        "plan_addons_coupon",
        [
            {
                "type": "plan",
                "seats": 3,
                "price_per_seat": 8,
                "active_users": 3,
            },
            {"type": "addon", "monthly_cost": 6.5},
            {"type": "coupon", "amount": 2},
        ],
        id="plan_addons_coupon",
    ),
    pytest.param(
        "zero_floor_and_base_fee",
        [
            {"type": "coupon", "amount": 99},
        ],
        id="zero_floor_and_base_fee",
    ),
    pytest.param(
        "unknown_records_are_ignored",
        [
            {
                "type": "plan",
                "seats": 2,
                "price_per_seat": 9,
                "active_users": 2,
            },
            {"type": "mystery", "note": "ignore me"},
        ],
        id="unknown_records_are_ignored",
    ),
]


@pytest.mark.parametrize(("scenario_name", "items"), SUBSCRIPTION_CASES)
def test_subscription_totals_match_legacy(subscriptions_entry_points, scenario_name, items):
    expected_total = legacy_subscriptions_handle(copy.deepcopy(items))

    legacy_total = subscriptions_entry_points["legacy"](items)
    refactored_total = subscriptions_entry_points["refactored"](items)

    assert legacy_total == pytest.approx(expected_total), scenario_name
    assert refactored_total == pytest.approx(expected_total), scenario_name


def test_subscription_overage_delta_matches_legacy(subscriptions_entry_points):
    base_plan = [
        {
            "type": "plan",
            "seats": 5,
            "price_per_seat": 10,
            "active_users": 5,
            "overage_charge": 4,
        }
    ]
    overage_plan = [
        {
            "type": "plan",
            "seats": 5,
            "price_per_seat": 10,
            "active_users": 7,
            "overage_charge": 4,
        }
    ]

    base_total = legacy_subscriptions_handle(copy.deepcopy(base_plan))
    overage_total = legacy_subscriptions_handle(copy.deepcopy(overage_plan))
    expected_delta = overage_total - base_total
    assert expected_delta > 0

    legacy_delta = (
        subscriptions_entry_points["legacy"](overage_plan)
        - subscriptions_entry_points["legacy"](base_plan)
    )
    refactored_delta = (
        subscriptions_entry_points["refactored"](overage_plan)
        - subscriptions_entry_points["refactored"](base_plan)
    )

    assert legacy_delta == pytest.approx(expected_delta)
    assert refactored_delta == pytest.approx(expected_delta)


def test_subscription_coupon_flooring(subscriptions_entry_points):
    payload = [
        {
            "type": "plan",
            "seats": 1,
            "price_per_seat": 12,
            "active_users": 1,
        },
        {"type": "coupon", "amount": 999},
    ]

    expected_total = legacy_subscriptions_handle(copy.deepcopy(payload))
    assert expected_total >= 0

    assert subscriptions_entry_points["legacy"](payload) == pytest.approx(expected_total)
    assert subscriptions_entry_points["refactored"](payload) == pytest.approx(expected_total)
