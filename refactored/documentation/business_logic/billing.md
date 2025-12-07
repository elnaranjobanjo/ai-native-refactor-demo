# Billing Module Business Logic

## High-Level Workflow
- `BillingOrchestrator` (in `refactored/billing_refactor/compute.py`) copies the caller-provided iterable and coordinates the four calculation stages: pricing, discounts, shipping, and taxes.
- `PricingEngine` tallies revenue lines by multiplying `price * qty` for `product` entries and `hours * rate` for `service` entries.
- `DiscountEngine` subtracts the raw `value` of every `discount` entry so incentives never pass through the pricing math.
- `ShippingCalculator` then evaluates the discounted subtotal to determine whether the preferred or base fee should apply before tax.
- `TaxCalculator` multiplies the shipping-inclusive amount by `1.22`, and the orchestrator rounds only the final number to preserve float precision in intermediate steps.

## Core Rules & Thresholds
- **Line type filtering:** Supported line types are provided by `PricingConfig` (`product`/`service`) and `DiscountConfig` (`discount`). Unknown types contribute `0` without raising.
- **Products:** `price * qty` is added to the subtotal, casting inputs to float for consistent math.
- **Services:** `hours * rate` is added to the subtotal, also cast to floats. There are no overtime or clamping rules.
- **Discounts:** Every discount entry subtracts its positive `value` from the subtotal; negative totals are allowed until shipping applies.
- **Shipping:** `ShippingPolicy` keeps the legacy threshold: if the discounted subtotal is greater than `100`, add `5`, otherwise add `15`.
- **Tax:** `TaxPolicy` sets a `0.22` rate, so the post-shipping amount is multiplied by `1.22`.
- **Rounding:** Only the final orchestrator result is rounded to two decimals, mirroring the legacy billing output.

## Data Flow & Helper Usage
- Engines expose helper functions (`pricing.accumulate_subtotal`, `discounts.sum_discounts`, etc.) but the orchestrator owns the production workflow.
- The caller can inject custom engines/policies for experiments; default engines are instantiated automatically when none are provided.
- Subtotal → discount deduction → shipping fee → tax application is the enforced order of operations, guaranteeing compatibility with the legacy billing totals.

## Extension Points & Risks
- **Configurability:** Dataclass configs document the allowable knobs (line-type names, shipping thresholds, tax rates) so product teams can tune pricing without touching orchestrator logic.
- **Calculator injection:** Alternative pricing, discount, or tax models can be passed into `BillingOrchestrator` for region-specific rules or experimentation.
- **Validation & observability:** Unknown line types silently drop out today; a future enhancement could emit structured warnings or raise to detect schema drift.
- **Currency safety:** The refactor still uses floats for backwards compatibility; if strict currency precision becomes a requirement, the engines should migrate to `Decimal` and explicit rounding strategies.
