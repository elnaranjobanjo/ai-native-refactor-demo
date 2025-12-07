# Billing Refactor Plan

## Goals
- Reproduce `legacy/billing.handle` outputs exactly while untangling pricing, discounts, shipping, and tax responsibilities.
- Remove inline constants (shipping thresholds/fees and tax multiplier) by surfacing configuration dataclasses per component.
- Provide typed, easily testable modules that own a single responsibility but still allow the orchestrator to remain a thin shell.

## Module Breakdown
1. **pricing.py**
   - Define `PricingConfig` to describe allowed item types (`product`, `service`).
   - Implement `PricingEngine.calculate_item(item: Mapping[str, Any]) -> float` that understands `price/qty` for products and `hours/rate` for services. Unknown types return `0` without mutating totals.
   - Provide `accumulate_subtotal(items)` helper that iterates the list once and sums only product/service results to avoid duplication in `compute.py`.
2. **discounts.py**
   - Introduce `DiscountConfig` controlling the entry type string (`discount`).
   - `DiscountEngine.calculate_discount(item)` returns raw negative contribution while using direct key access so missing fields raise the same errors as the legacy code.
   - `sum_discounts(items)` helper mirrors the pricing accumulator.
3. **shipping.py**
   - `ShippingPolicy` dataclass with `threshold`, `high_fee`, `low_fee` (defaults `100`, `5`, `15`).
   - `ShippingCalculator.calculate(subtotal)` returns one of the configured fees based on the subtotal *before shipping and tax*.
4. **taxes.py**
   - `TaxPolicy` dataclass storing `rate` (0.22).
   - `TaxCalculator.apply(amount)` multiplies by `(1 + rate)` to mirror legacy behavior (shipping already included).
5. **compute.py**
   - Export `handle(items)` entry point used by tests.
   - Flow: use `PricingEngine` and `DiscountEngine` to derive subtotal, add shipping fee, pass through `TaxCalculator`, round to two decimals, return `float`.
   - Unknown line types stay ignored because no engine consumes them.

## Implementation Steps
1. Implement pricing and discounts modules with shared helper functions and type hints; cover legacy logic (products/services, discounts) exactly.
2. Build configurable shipping and tax calculators using dataclasses to hold hardcoded legacy values.
3. Wire everything in `compute.py` with a `BillingOrchestrator` (function or small class) that sequences subtotal -> shipping -> tax -> rounding.
4. Keep module-level factory functions for default configs so future tests can inject variants while defaults reproduce legacy values.
