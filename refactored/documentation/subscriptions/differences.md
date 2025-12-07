# Parity Guarantees
- Maintains legacy ordering: `(plans + addons - coupons)` is clamped at zero before applying the 12.5 base fee.
- Default type names (`plan`, `addon`, `coupon`) and default overage charge (3) remain unchanged.
- Public API still exposes a `handle(records)` entry with rounding to two decimals.

# Improvements
- Dedicated plan/addon/coupon modules isolate responsibilities and make each pathway testable.
- `PlanCharge` dataclass removes duplicated math and captures the overage constraint explicitly.
- Policy dataclasses document configuration knobs for base fees and type keys, enabling declarative overrides.
- Future behaviors (e.g., coupon caps, addon tiers) can plug into the orchestrator without editing unrelated code.

# Remaining Risks / Follow-ups
- Unknown record types are still ignored silently; consider validation or logging to catch data corruption.
- Clamp logic is hardcoded; introducing configurable minimums/maximums might be required for enterprise customers.
