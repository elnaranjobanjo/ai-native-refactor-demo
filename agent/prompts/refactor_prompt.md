You are an AI refactoring agent.

Specs describing the desired architectures live in `./agent/specs/*.yaml`.
Legacy sources sit under `./legacy/` (for example `billing.py` and `subscriptions.py`).

For **each** spec file:
1. Read the spec, the corresponding legacy module(s), and (if present) the
   `./refactored/documentation/business_logic/<module>.md` notes so you respect the captured business rules.
2. Create a dedicated output directory `./refactored/<spec_name>/` (include an `__init__.py`
   so the package can be imported from tests).
3. Produce a detailed architecture & implementation plan and save it to
   `./refactored/reasoning_artifacts/<spec_name>_plan.md`.
4. Emit the refactored modules as separate code blocks, placing each file directly under
   `./refactored/<spec_name>/` (add subdirectories if the architecture calls for them).
5. Preserve legacy behavior, add type hints, and follow the constraints listed in the spec.

All plans and code must live under `./refactored/`, and every plan belongs in
`./refactored/reasoning_artifacts/`. Output only the generated plans and code blocks—no extra commentary.
