"""Coupon stacking logic for subscriptions."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Any


@dataclass(frozen=True)
class CouponConfig:
    coupon_type: str = "coupon"


class CouponStack:
    def __init__(self, config: CouponConfig | None = None) -> None:
        self._config = config or CouponConfig()

    def calculate(self, record: Mapping[str, Any]) -> float:
        if record.get("type") != self._config.coupon_type:
            return 0.0
        return float(record.get("amount", 0.0))

    def sum_coupons(self, records: Iterable[Mapping[str, Any]]) -> float:
        total = 0.0
        for record in records:
            total += self.calculate(record)
        return total


def sum_coupons(records: Iterable[Mapping[str, Any]], config: CouponConfig | None = None) -> float:
    stack = CouponStack(config=config)
    return stack.sum_coupons(records)
