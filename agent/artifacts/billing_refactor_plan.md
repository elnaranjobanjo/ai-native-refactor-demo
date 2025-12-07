# Billing Refactor Plan

## Goal
Modularize the billing pipeline so pricing, discounts, shipping, and taxes are isolated components while maintaining the legacy `handle` behavior and rounding.

## Domain Model
- Input items keep their legacy dictionary structure (`type`, `price`, etc.) to avoid breaking callers.
- Intermediate totals move through a deterministic pipeline: pricing subtotal → discounts → shipping → tax → rounded total.
- Configuration objects hold the numeric constants (shipping thresholds, tax rate) so no values are hardcoded inside logic.

## Module Responsibilities
1. **pricing.py**
   - Provide `PriceCalculator` with `add_product`, `add_service`, and `total` methods.
   - Handles multiplication behavior (`price * qty`, `hours * rate`) and ignores unknown types.
   - Exposes `compute_subtotal(items: Iterable[Dict[str, Any]]) -> float` for the pipeline.
2. **discounts.py**
   - Define `DiscountAggregator` to sum discount values.
   - Provide `apply_discounts(subtotal: float, items: Iterable[Dict[str, Any]]) -> float`.
3. **shipping.py**
   - Capture shipping thresholds in `ShippingConfig` dataclass.
   - Implement `calculate_shipping(subtotal: float, config: ShippingConfig = DEFAULT_SHIPPING) -> float` returning the surcharge.
4. **taxes.py**
   - Hold tax rate in `TaxConfig` dataclass.
  - Offer `apply_tax(amount: float, config: TaxConfig = DEFAULT_TAX) -> float`.
5. **compute.py**
   - Expose `handle(items: Sequence[Dict[str, Any]]) -> float` matching legacy API.
   - Orchestrate: subtotal = pricing → discounted = discounts → +shipping → taxed = taxes → final rounding.

## Implementation Steps
1. Implement pricing module with reusable helpers and defensive lookups (`get`) while mirroring legacy math.
2. Implement discounts aggregation using the same rules as legacy (subtract `value`).
3. Encode shipping logic via config dataclass to replace hardcoded literals.
4. Encode tax logic with configurable rate, applying the same multiplication and rounding precision.
5. Build compute orchestrator importing the modules to process a list of items in order.
6. Update package exports if needed (none currently) and ensure `handle` resides in `compute.py`.
7. Confirm pipeline with spec test case and ensure `round(..., 2)` is applied once at the end.
