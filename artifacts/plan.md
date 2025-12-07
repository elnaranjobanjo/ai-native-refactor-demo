# Billing Module Refactor Plan

## Objectives
- Mirror legacy `legacy/billing.py` behavior while modularizing responsibilities per `specs/billing_refactor.yaml`.
- Introduce explicit type hints and clear data contracts for each component.
- Centralize configuration for shipping thresholds/fees and tax rate to eliminate hidden constants.

## Domain Model
- **LineItem**: dict-like payload coming from legacy API, containing `type` plus relevant fields.
- **Money**: floats representing currency values; callers remain consistent with legacy expectations.
- **PricingContext**: captured settings (shipping thresholds, fees, tax rate), passed to submodules to avoid globals.

## Module Responsibilities
1. **pricing.py**
   - Provide `calculate_merchandise_total(items: Sequence[Mapping[str, Any]]) -> float`.
   - Iterate over `product` and `service` entries; ignore unknowns to maintain parity.
   - Uses helper functions `price_product` and `price_service` to encapsulate per-type math and future validations.
   - Emits subtotal before discounts.

2. **discounts.py**
   - Provide `apply_discounts(total: float, items: Sequence[Mapping[str, Any]]) -> float` and `total_discounts` helper.
   - Sum every `discount` entry’s `value` field (defaulting to 0 if missing) and subtract from running total.
   - Ignores unknown item types/per legacy behavior.

3. **shipping.py**
   - Provide `calculate_shipping(total_after_discounts: float, policy: ShippingPolicy) -> float`.
   - Encapsulates threshold comparison via `ShippingPolicy` dataclass holding threshold plus both fees.
   - Keeps logic parity with legacy 5/15 structure while enabling future policy swaps.

4. **taxes.py**
   - Provide `apply_tax(amount: float, rate: float) -> float`.
   - Validate rate input and centralize rounding concerns (return precise float for final rounding in orchestrator).

5. **compute.py**
   - Orchestrator exposing `compute_bill(items: Sequence[Mapping[str, Any]], config: Optional[BillingConfig] = None) -> float`.
   - Compose pricing → discounts → shipping → taxes pipeline.
   - Defines `BillingConfig` dataclass bundling shipping policy and tax rate; supplies legacy-equivalent defaults (threshold 100, low fee 5, high fee 15, tax 0.22).
   - Performs one final `round(..., 2)` to match legacy output.

## Data Flow
1. Caller invokes `compute_bill` with raw legacy payload list.
2. `pricing.calculate_merchandise_total` produces subtotal of billable entries.
3. `discounts.apply_discounts` subtracts aggregated discounts.
4. `shipping.calculate_shipping` uses discounted total + configured `ShippingPolicy` to determine fee; fee added to running total.
5. `taxes.apply_tax` multiplies by `(1 + rate)`.
6. Final rounded total returned.

## Validation Strategy
- Maintain current test case from spec via the orchestrator; tests invoke new entry point and ensure parity.
- Add focused unit coverage for pricing/discount math if time permits (optional, not part of current scope).

## Rollout Considerations
- Legacy entry point can be replaced by thin adapter that imports `compute_bill` to maintain interface.
- Configuration structure enables future requirements (different regions, tax rates) without touching algorithms.
