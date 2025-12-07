# Overview
- `BillingOrchestrator` (in `compute.py`) coordinates pricing, discounts, shipping, and taxes to keep each concern isolated.
- Dedicated modules expose typed engines with dataclass-backed policies so individual steps can be configured or tested independently.

## Module Layout
- `pricing.PricingEngine` uses `PricingConfig` to translate `product`/`service` items into a subtotal.
- `discounts.DiscountEngine` with `DiscountConfig` sums discount rows separately from earnable revenue.
- `shipping.ShippingCalculator` driven by `ShippingPolicy` decides whether the base fee or threshold fee applies.
- `taxes.TaxCalculator` with `TaxPolicy` multiplies the post-shipping amount by configurable rates.
- `compute.handle` offers the legacy-compatible entry point while delegating to `BillingOrchestrator`.

## Data Flow
1. Caller-provided iterable is copied into a list so pricing and discount engines can iterate deterministically.
2. Pricing subtotal is calculated, discount total is subtracted, and the result feeds the shipping calculator.
3. The shipping fee is added to reach `total_with_shipping`, and tax is applied last to honor legacy ordering.
4. The orchestrator rounds to two decimals to preserve final presentation parity.

## Configuration & Extension Points
- All engines accept optional config objects, allowing alternative type names or fee policies without code changes.
- Custom calculators can be injected into `BillingOrchestrator` for A/B tests or regional policies.
- Module-level helpers (`pricing.accumulate_subtotal`, etc.) provide simple functional entry points for isolated reuse.
