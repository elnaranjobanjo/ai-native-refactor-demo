# Subscriptions Refactor Plan

## Goals
- Match `legacy/subscriptions.handle_subscriptions` outputs exactly, including silent handling of unknown record types, coupon stacking, zero clamp, and base fee.
- Replace hardcoded seat math, overage defaults, addon fees, coupon deductions, and base fee with type-hinted dataclasses.
- Encapsulate plan, addon, and coupon logic into standalone modules that the orchestrator composes deterministically.

## Module Breakdown
1. **plans.py**
   - Define `PlanPricingConfig` (`plan_type`, `default_overage_charge`).
   - Implement `PlanCharge` dataclass holding seat usage inputs for clarity.
   - `PlanPricingEngine.calculate(record)` returns seat + overage charges, raising KeyError when mandatory keys are missing to mirror legacy assumptions.
   - Provide accumulator helper `sum_plan_charges(records)` for orchestrator use.
2. **addons.py**
   - `AddonConfig` with `addon_type` ("addon").
   - `AddonCalculator.sum_addons(records)` adds `monthly_cost` with a default of `0` when the key is absent, matching `dict.get` usage in legacy code.
3. **coupons.py**
   - `CouponConfig` storing `coupon_type` ("coupon").
   - `CouponStack.sum_coupons(records)` subtracts the raw `amount` (default `0` like legacy) so negative values increase totals identically to the original branch.
4. **compute.py**
   - `SubscriptionOrchestrator` class wiring plan, addon, coupon modules + base fee config (dataclass; default 12.5).
   - Flow: sum plan charges, add addon totals, subtract coupons, clamp negative results to zero, add base fee, round to 2 decimals.
   - Export `handle(records)` convenience function to match legacy signature.

## Implementation Steps
1. Implement plan/addon/coupon modules with dataclasses, helper engines, and typed accumulation APIs that reflect each branch in the legacy loop.
2. Build `compute.py` orchestrator with injectable components/config, ensuring zero clamp and rounding order matches `handle_subscriptions`.
3. Add `__init__.py` (already created) so tests import `refactored.subscriptions_refactor.compute.handle` as the new entry point.
