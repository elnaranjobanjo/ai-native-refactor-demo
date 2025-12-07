# Subscriptions Module Business Logic

## High-Level Workflow
- `legacy/subscriptions.py` aggregates plan usage records, addon charges, and coupons to produce a monthly invoice total.
- Each record in the input list is classified by its `type` and processed in a single pass: plan rows add seat charges and potential overages, addon rows contribute recurring fees, coupon rows reduce the running total, and unknown rows are skipped.
- After processing all entries, the function applies a floor at zero, adds a flat base platform fee, and rounds the total to two decimals. No refactored module currently exists at `refactored/subscriptions_refactor`, so these behaviors define the baseline requirements.

## Core Rules & Interactions
- **Plan charges:** cost equals `seats * price_per_seat`. The code assumes both keys exist on every plan record.
- **Overage logic:** if `active_users > seats`, charge `(active_users - seats) * overage_charge`, defaulting to `3` when not provided. Overages are additive per record.
- **Addon accumulation:** sum `monthly_cost` (default `0`) for every addon record, then add to the plan subtotal at the end.
- **Coupons:** subtract each coupon's `amount`; negative totals are allowed temporarily until clamped.
- **Clamp:** if subtotal after addons and coupons drops below `0`, reset it to `0` before adding any fees.
- **Base fee:** always add `12.5` after clamping, meaning coupons can only offset usage, not the base platform fee.
- **Rounding:** only the final total is rounded, so intermediate floats may retain precision issues.

## Data Flow & Helper Coordination
- The module relies on one orchestrating function, `handle_subscriptions`, with inline logic for plans, addons, and coupons; there are no helper modules or shared calculators.
- Separate accumulators (`total`, `addons`, `promo`) hold intermediate state until the end, where they merge into one billable total.
- Unknown record types are silently ignored, so nothing enforces schema alignment or guarantees that addon/coupon data makes it into the invoice.

## Extension Points & Risks
- **Plan engines:** refactor should expose a hook for different plan pricing formulas (tiers, per-feature metrics) and make overage rates configurable per plan or policy.
- **Addon marketplace:** providing richer addon metadata (prorations, annual vs monthly) likely requires a dedicated module and ordering rules before coupons apply.
- **Coupon strategy:** stacking logic is currently first-come, first-served and purely amount-based; new design should clarify precedence with plan/addon fees and support percentage or duration-based promos.
- **Base fee policy:** the flat `12.5` fee is buried; future versions may need regional pricing, waived-fee promotions, or fee calculation based on plan tiers.
- **Validation:** skipping unknown record types hides data problems; consider schema validation per record and structured error reporting so upstream systems can correct malformed events.
- **Configurability:** constants (default overage `3`, clamp-to-zero rule, rounding strategy) should be surfaced in the refactor to enable per-tenant policies and integration tests.
