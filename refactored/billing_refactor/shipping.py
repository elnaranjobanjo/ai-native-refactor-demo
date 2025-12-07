"""Shipping fee policy for billing totals."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ShippingPolicy:
    threshold: float = 100.0
    over_threshold_fee: float = 5.0
    base_fee: float = 15.0


class ShippingCalculator:
    def __init__(self, policy: ShippingPolicy | None = None) -> None:
        self._policy = policy or ShippingPolicy()

    def calculate(self, subtotal: float) -> float:
        """Return the shipping fee applied to the given subtotal."""

        if subtotal > self._policy.threshold:
            return self._policy.over_threshold_fee
        return self._policy.base_fee


def calculate_shipping(subtotal: float, policy: ShippingPolicy | None = None) -> float:
    calculator = ShippingCalculator(policy=policy)
    return calculator.calculate(subtotal)
