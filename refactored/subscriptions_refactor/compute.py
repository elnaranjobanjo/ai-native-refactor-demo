"""Subscription billing orchestrator."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Any, Sequence

from .addons import AddonCalculator
from .coupons import CouponStack
from .plans import PlanPricingEngine


@dataclass(frozen=True)
class SubscriptionFeePolicy:
    base_fee: float = 12.5


class SubscriptionOrchestrator:
    """Coordinates plan, addon, and coupon processing."""

    def __init__(
        self,
        plans: PlanPricingEngine | None = None,
        addons: AddonCalculator | None = None,
        coupons: CouponStack | None = None,
        fee_policy: SubscriptionFeePolicy | None = None,
    ) -> None:
        self._plans = plans or PlanPricingEngine()
        self._addons = addons or AddonCalculator()
        self._coupons = coupons or CouponStack()
        self._fee_policy = fee_policy or SubscriptionFeePolicy()

    def handle(self, records: Sequence[Mapping[str, Any]]) -> float:
        plan_total = self._plans.sum_charges(records)
        addon_total = self._addons.sum_addons(records)
        coupon_total = self._coupons.sum_coupons(records)

        subtotal = plan_total + addon_total - coupon_total
        if subtotal < 0:
            subtotal = 0.0

        subtotal += self._fee_policy.base_fee
        return round(subtotal, 2)


def handle(records: Iterable[Mapping[str, Any]]) -> float:
    """Compatibility wrapper mirroring legacy `handle_subscriptions`."""

    record_list = list(records)
    orchestrator = SubscriptionOrchestrator()
    return orchestrator.handle(record_list)
