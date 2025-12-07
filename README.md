# AI-Native Refactor Demo

This repo showcases a one-day “AI System Architect” workflow that takes two messy legacy modules (`legacy/billing.py`, `legacy/subscriptions.py`) through spec-driven refactoring, regression test generation, documentation, and QA verification. Everything the agents produce lands under `refactored/`, giving you an auditable trail of plans, code, tests, docs, and QA reports.

---

## Quick Start

1. **Install [Task](https://taskfile.dev/)**  
   The automation uses `Taskfile.yaml`. Follow Task’s install instructions for your OS.

2. **Install Python deps**  
   ```bash
   task setup-env
   ```
   Creates `.venv/` and installs `pytest`.

3. **Run the full agentic pipeline**  
   ```bash
   task pipeline
   ```
   This sequentially runs business-logic analysis, refactoring, test generation, pytest, documentation, and QA. Outputs are written to `refactored/…` (see below).

> Individual steps (e.g., `task refactor`, `task testplan`, `task docs`) are also available if you want to iterate on a single stage.

---

## Repository Layout

```
legacy/                     # messy source modules that act as the legacy estate
agent/
  prompts/                  # instructions each agent executes (see below)
  specs/                    # structured requirements for refactors/tests/docs/qa
refactored/                 # generated plans, code, tests, docs, QA reports
Taskfile.yaml               # automation entry points
requirements.txt            # runtime deps for pytest
```

Key subfolders under `refactored/` after running the pipeline:

- `billing_refactor/`, `subscriptions_refactor/`: refactored packages (with `__init__.py`, `compute.py`, etc.).
- `tests/`: pytest suites that load both legacy and refactored entry points.
- `documentation/`: `legacy.md`, `refactored.md`, `differences.md`, plus `documentation/business_logic/*.md`.
- `reasoning_artifacts/`: plans (`*_plan.md`), regression `testing_plan.md`, `testing_results.txt`, `qa_report.md`.

---

## Agent Tasks & Prompts

| Task name | Purpose | Prompt | Spec |
|-----------|---------|--------|------|
| `biz-logic` | Captures business rules before touching code; outputs `refactored/documentation/business_logic/*.md`. | `agent/prompts/business_logic_prompt.md` | `agent/specs/business_logic.yaml` |
| `refactor` | Reads `*_refactor.yaml` specs + business-logic notes, writes plans to `refactored/reasoning_artifacts/*_plan.md` and code under `refactored/<spec>/`. | `agent/prompts/refactor_prompt.md` | `agent/specs/billing_refactor.yaml`, `agent/specs/subscriptions_refactor.yaml` |
| `testplan` | Generates regression plan + pytest suites under `refactored/tests/`. | `agent/prompts/testing_prompt.md` | `agent/specs/testing_suite.yaml` |
| `test` | Runs pytest via `.venv` and stores the log in `refactored/reasoning_artifacts/testing_results.txt`. | (shell task) | N/A |
| `docs` | Writes `legacy.md`, `refactored.md`, `differences.md` per module. | `agent/prompts/documentation_prompt.md` | `agent/specs/documentation.yaml` |
| `qa` | Reruns tests if needed, verifies docs match code, produces `qa_report.md`. | `agent/prompts/qa_prompt.md` | `agent/specs/qa.yaml` |
| `pipeline` | Runs all of the above (`biz-logic` → `refactor` → `testplan` → `test` → `docs` → `qa`). | Taskfile orchestrator | — |

Each prompt/spec pair is deliberately short so you can tweak requirements without editing code.
