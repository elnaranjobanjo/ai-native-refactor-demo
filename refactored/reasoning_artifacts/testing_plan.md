## Regression Testing Plan: Billing & Subscriptions

### Objectives
- Validate that `legacy.billing.handle` and `legacy.subscriptions.handle_subscriptions` remain ground truth.
- Prove behavioral parity with `refactored.billing_refactor.compute.compute_bill` and `refactored.subscriptions_refactor.compute.compute_total`.
- Capture regressions around tax/shipping rules, coupon handling, overage billing, and zero-clamp logic.

### Assumptions
- Legacy behavior (including quirks like duplicated conditionals and silent ignores) is authoritative.
- Refactored entry points expose deterministic, side-effect-free computations returning numeric totals.
- Unknown record types must be ignored without raising errors in both domains.
- Shipping fee (billing) and base fee (subscriptions) always apply even if subtotal is zero.

### Test Harness Strategy
- Build reusable helpers to invoke both legacy and refactored entry points with the same payload.
- Parameterize pytest cases per scenario and assert parity by comparing totals (legacy result as expected).
- Add explicit assertions for critical post-processing steps: tax (22%), shipping tiers (>100 → 5 else 15), base fee inclusion, coupon deductions, overage calculations, and zero-flooring.
- Edge cases validated via dedicated scenarios: unknown billing items, coupons exceeding totals, zero-only subscription payloads.
- Any new scenarios derived from spec must cover both modules so regressions in one implementation surface immediately.

### Scenario Mapping
- **Billing**
  - `product_with_discount`: validates stacked line items, discount subtraction before fees, and tax application.
  - `service_and_product_mix`: ensures service hours blend with product pricing, triggers high shipping path.
  - `unknown_items_ignored`: confirms mysterious types do not alter totals.
  - Edge extensions: explicit check for zero totals after discounts and that shipping + tax still apply.
- **Subscriptions**
  - `basic_plan_with_overage`: exercises overage math plus coupon deduction and base fee.
  - `plan_addons_coupon`: covers addon accumulation and promo stacking.
  - `zero_floor_and_base_fee`: validates clamp at zero prior to adding base fee.
  - Edge extensions: unknown record ignored, coupon larger than subtotal, addon-only flows.

### Test Artifacts
- `refactored/tests/conftest.py`: shared fixtures providing legacy/refactored callables and helper to run both.
- `refactored/tests/test_billing.py`: parametrized billing scenarios with data-driven payloads and parity asserts.
- `refactored/tests/test_subscriptions.py`: parametrized subscription scenarios plus dedicated zero/unknown edge cases.

### Coverage Validation
- Totals derived from legacy calls; refactored results must match rounding behavior (`round(..., 2)` as per legacy).
- Each scenario asserts:
  1. Legacy total equals computed expectation (documented via comments if special rules involved).
  2. Refactored total matches legacy total exactly.
  3. Additional invariants (non-negative totals post clamp, shipping fee thresholds, etc.) verified when relevant.
- Edge cases ensure regression visibility for: excessive coupons, empty inputs, overage default charges, and additive shipping/tax interplay.
