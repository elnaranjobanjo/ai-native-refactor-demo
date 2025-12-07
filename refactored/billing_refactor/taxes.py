"""Tax calculations for billing."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TaxPolicy:
    rate: float = 0.22  # 22% tax


class TaxCalculator:
    def __init__(self, policy: TaxPolicy | None = None) -> None:
        self._policy = policy or TaxPolicy()

    def apply(self, amount: float) -> float:
        """Apply tax to the provided amount."""

        return amount * (1.0 + self._policy.rate)


def apply_tax(amount: float, policy: TaxPolicy | None = None) -> float:
    calculator = TaxCalculator(policy=policy)
    return calculator.apply(amount)
