"""Pricing calculations for billing line items."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Any


@dataclass(frozen=True)
class PricingConfig:
    """Configurable keys for supported pricing item types."""

    product_type: str = "product"
    service_type: str = "service"


class PricingEngine:
    """Calculates totals for product and service line items."""

    def __init__(self, config: PricingConfig | None = None) -> None:
        self._config = config or PricingConfig()

    def calculate_item(self, item: Mapping[str, Any]) -> float:
        """Return the contribution for a single line item or zero if unsupported."""

        item_type = item.get("type")
        if item_type == self._config.product_type:
            return float(item["price"]) * float(item["qty"])
        if item_type == self._config.service_type:
            return float(item["hours"]) * float(item["rate"])
        return 0.0

    def accumulate_subtotal(self, items: Iterable[Mapping[str, Any]]) -> float:
        total = 0.0
        for item in items:
            total += self.calculate_item(item)
        return total


def accumulate_subtotal(items: Iterable[Mapping[str, Any]], config: PricingConfig | None = None) -> float:
    """Helper for callers that do not need to instantiate the engine explicitly."""

    engine = PricingEngine(config=config)
    return engine.accumulate_subtotal(items)
