ai-native-refactor-demo/
│
├── legacy/
│   └── billing.py                 # original messy code
│
├── refactored/                    # AI-generated output goes here
│   └── (populated by agent)
│
├── specs/
│   └── billing_refactor.yaml      # architecture + requirements
│
├── tests/
│   └── test_billing.py            # defines expected behavior
│
├── artifacts/
│   ├── diff.md                    # before/after output
│   ├── plan.md                    # AI-generated architecture plan
│   └── test_results.txt
│
├── visualize_diff.py              # generates markdown diff
│
├── agent.md                       # short doc explaining the agentic workflow
│
└── README.md                      # project overview
