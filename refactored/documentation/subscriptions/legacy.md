# Overview
- `handle_subscriptions` cascades all subscription pricing logic (plans, addon fees, coupon credits, base fee) through a single mutable accumulator.
- Hardcoded assumptions about record structure plus clamped totals make the behavior difficult to reason about or extend.

## Responsibilities
- For `plan` rows, calculate `seats * price_per_seat` and optionally charge an overage when `active_users > seats` using a per-record `overage_charge` or default of 3.
- Aggregate addon spend by summing the `monthly_cost` on `addon` rows, and subtract coupons via their `amount`.
- Apply a base platform fee of 12.5 and clamp negative totals to zero before adding the fee.

## Pain Points
- Branch duplication for `plan` type leads to maintenance risk and inflated totals when bugs slip through.
- Lack of separation between plan, addon, and coupon logic prevents reuse and hinders targeted testing.
- Silent `pass` on unknown types hides data issues and hampers telemetry.
- Magic numbers (base fee, overage default) are scattered constants with no documented source.

## Hidden Constraints
- Order sensitivity: total derived as `(plans + addons - coupons)` with clamp to zero **before** adding the base fee.
- Coupon stacking is purely additive—no caps or prioritization are enforced.
- Rounding occurs only at the very end, matching the billing presentation layer.
