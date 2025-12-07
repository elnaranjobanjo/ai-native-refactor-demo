# Overview
- Single `handle` function iterates raw dictionaries and mutates a running total for products, services, and discounts.
- Module also hides shipping, tax, and rounding rules inside the same loop, so callers cannot reuse sub-calculators or override policies.

## Responsibilities
- Price `product` rows via `price * qty` and `service` rows via `hours * rate`, updating one `total` variable.
- Fold discount rows by subtracting their `value` field directly inside the main loop.
- Apply hardcoded shipping surcharge (\$5 over \$100 otherwise \$15), then apply a 22% tax, and finally round to two decimals.

## Pain Points
- Coupled branching: duplicated `product` and `discount` branches make the rules inconsistent and difficult to maintain.
- Silent failures: unsupported `type` values are ignored without logging, so caller gets partial totals.
- Policy rigidity: shipping and tax percentages are baked into the function and require code edits to change.
- Testing difficulty: only global `handle` entrypoint exists; helper `apply_discount` is unused and incorrect.

## Hidden Constraints
- Order dependency: discounts are summed before shipping/taxes, and shipping is always added before tax.
- Implicit rounding: total is rounded only at the end, so intermediate precision must remain intact.
- Hardwired type names (`product`, `service`, `discount`) must be present in item dicts; missing keys raise `KeyError`.
- Shipping threshold (100) and tax rate (22%) act as unofficial configuration constants tied to business expectations.
