"""Public entry point for billing calculations."""
from __future__ import annotations

from typing import Iterable, Mapping, Any, Sequence

from .discounts import DiscountEngine
from .pricing import PricingEngine
from .shipping import ShippingCalculator
from .taxes import TaxCalculator


class BillingOrchestrator:
    """Coordinates pricing, discounts, shipping, and tax steps."""

    def __init__(
        self,
        pricing: PricingEngine | None = None,
        discounts: DiscountEngine | None = None,
        shipping: ShippingCalculator | None = None,
        taxes: TaxCalculator | None = None,
    ) -> None:
        self._pricing = pricing or PricingEngine()
        self._discounts = discounts or DiscountEngine()
        self._shipping = shipping or ShippingCalculator()
        self._taxes = taxes or TaxCalculator()

    def handle(self, items: Sequence[Mapping[str, Any]]) -> float:
        subtotal = self._pricing.accumulate_subtotal(items)
        discount_total = self._discounts.sum_discounts(items)
        subtotal -= discount_total

        shipping_fee = self._shipping.calculate(subtotal)
        total_with_shipping = subtotal + shipping_fee

        taxed_total = self._taxes.apply(total_with_shipping)
        return round(taxed_total, 2)


def handle(items: Iterable[Mapping[str, Any]]) -> float:
    """Compatibility wrapper mirroring the legacy billing entry point."""

    item_list = list(items)
    orchestrator = BillingOrchestrator()
    return orchestrator.handle(item_list)
