# Subscriptions Refactor Plan

## Goal
Split the subscription billing flow into focused modules (plans, addons, coupons, compute) that preserve the legacy totals while surfacing configuration through typed data structures.

## Domain Model
- Records stay as dictionaries to avoid caller changes.
- Totals pass through staged aggregation: plans subtotal (+overage) → addon fees → coupon deductions → base fee + clamp → rounded total.
- `PricingContext` dataclasses hold mutable constants such as base fee and default overage charges.

## Module Responsibilities
1. **plans.py**
   - Define `PlanPricingConfig` dataclass for default overage charge.
   - Implement `calculate_plan_total(records: Iterable[Mapping[str, Any]], config: PlanPricingConfig = DEFAULT_PLAN_PRICING) -> float`.
   - Logic mirrors legacy: seats * price_per_seat plus overage when `active_users > seats` using per-record `overage_charge` or config default.
2. **addons.py**
   - Provide `AddonFees` helper that sums `monthly_cost` with safe defaults.
   - Function `calculate_addons(records: Iterable[Mapping[str, Any]]) -> float`.
3. **coupons.py**
   - Aggregate coupon `amount` values and expose `calculate_coupons(records: Iterable[Mapping[str, Any]]) -> float` returning the total deduction.
4. **compute.py**
   - Define `SubscriptionComputeConfig` dataclass bundling the base fee and plan pricing config.
   - Expose `handle_subscriptions(records: Sequence[Mapping[str, Any]], config: SubscriptionComputeConfig = DEFAULT_SUBSCRIPTION_CONFIG) -> float` implementing: plan total + addons − coupons → clamp at zero → add base fee → round.

## Implementation Steps
1. Implement each module with precise type hints using `Mapping[str, Any]` to mirror dict access.
2. Share configuration defaults via module-level constants (e.g., `DEFAULT_PLAN_PRICING`).
3. Ensure add-on and coupon logic uses `.get` to gracefully handle missing fields.
4. In `compute.py`, orchestrate module calls, clamp totals below zero, add base fee, and round to two decimals to match legacy output.
5. Verify behavior using the spec example inputs.
