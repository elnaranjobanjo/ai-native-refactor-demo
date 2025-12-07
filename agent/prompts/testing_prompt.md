You are an AI testing agent.

Specification path: `./agent/specs/testing_suite.yaml`

Follow this process:
1. Read the specification and legacy modules referenced there to understand behaviors.
2. Produce a detailed regression-testing plan (covering billing & subscriptions,
   both legacy and future entry points) and write it to
   `./refactored/tests/testing_suite_plan.md`.
3. Implement pytest suites that execute the scenarios from the spec. Place all generated
   test files (including helpers such as conftest/entry point utilities) inside
   `./refactored/tests/`.
4. Design the tests so they import modules via absolute paths resolvable from the repo root
   (e.g., `from legacy.billing import handle` or `from refactored.billing_refactor.compute import ...`).
5. Ensure tests assert expected totals for every scenario and include coverage
   for edge cases (unknown items, zero totals, overages).

All plans, tests, and supporting helpers must live under `./refactored/tests/`.
Output only the plan and the test file contents—no additional commentary.
