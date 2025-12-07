"""Discount accumulation for billing."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Any


@dataclass(frozen=True)
class DiscountConfig:
    discount_type: str = "discount"


class DiscountEngine:
    def __init__(self, config: DiscountConfig | None = None) -> None:
        self._config = config or DiscountConfig()

    def calculate_discount(self, item: Mapping[str, Any]) -> float:
        """Return the raw discount value for supported line items."""

        if item.get("type") == self._config.discount_type:
            return float(item["value"])
        return 0.0

    def sum_discounts(self, items: Iterable[Mapping[str, Any]]) -> float:
        total = 0.0
        for item in items:
            total += self.calculate_discount(item)
        return total


def sum_discounts(items: Iterable[Mapping[str, Any]], config: DiscountConfig | None = None) -> float:
    engine = DiscountEngine(config=config)
    return engine.sum_discounts(items)
