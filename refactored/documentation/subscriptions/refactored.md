# Overview
- `SubscriptionOrchestrator` (in `compute.py`) delegates to focused engines for plans, addons, and coupons, then enforces clamping and fees.
- Dataclass-backed policies (`PlanPricingConfig`, `AddonConfig`, `CouponConfig`, `SubscriptionFeePolicy`) document business knobs explicitly.

## Module Layout
- `plans.PlanPricingEngine` converts qualifying plan records into `PlanCharge` dataclass instances that compute base and overage costs.
- `addons.AddonCalculator` sums `monthly_cost` for addon records, keeping type filtering in one place.
- `coupons.CouponStack` accumulates coupon credits, enabling future enhancements like caps or expiration checks.
- `compute.handle` offers backward-compatible entry while exposing orchestrator injection points for alternate policies.

## Data Flow
1. Orchestrator sums plan, addon, and coupon totals independently to keep arithmetic transparent.
2. Subtotal is `plan_total + addon_total - coupon_total`.
3. Subtotal is clamped at zero to preserve legacy behavior, then `SubscriptionFeePolicy.base_fee` is added.
4. Result is rounded to two decimals before returning.

## Configuration & Extension Points
- Each calculator accepts optional configs to change record type names, default overage charges, or coupon semantics.
- Custom calculators/policies can be injected into `SubscriptionOrchestrator` for experiments or region-specific pricing.
- `PlanCharge` encapsulates base vs overage calculations, making it easier to add tiers or seat caps.
