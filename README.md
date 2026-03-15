# Power BI Automated Measure Testing with PBIP

A practical starting point for **automated Power BI measure validation** using PBIP (Power BI Project) files, Python, and AI-assisted tooling.

This repo shows how to treat Power BI semantic models as testable engineering artifacts — inspecting TMDL definitions, detecting risky DAX patterns, and generating validation scenarios automatically.

## Why This Matters

- **PBIP/PBIR/TMDL** files make Power BI assets source-controllable for the first time
- Measures are business logic — they deserve the same testing discipline as application code
- AI tools (GitHub Copilot, Claude, etc.) can generate draft test scenarios from model metadata
- A lightweight CSV-based validation template bridges the gap between automation and human review

## What You'll Find

| Area | Description |
|------|-------------|
| **Semantic Model** | A complete TMDL model with 7 DAX measures (sales, margins, ratios) |
| **Validation Framework** | Python tools that inspect PBIP files and auto-generate test scenarios |
| **Measure Templates** | CSV-based validation cases with status tracking (draft → reviewed → approved) |
| **Notebooks** | Guided Jupyter workflows for auth, API queries, and validation demos |
| **Python Utilities** | Reusable modules for Power BI REST API, auth, config, and metadata |
| **Sample Data** | Synthetic CSV datasets for a regional sales demo (no real data) |

## Quick Start

### 1. Clone and set up

```bash
git clone https://github.com/CharnritK/powerbi_demo_PBIPxGHCopilot.git
cd powerbi_demo_PBIPxGHCopilot

python -m venv .venv
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows

pip install -e ".[dev]"
```

### 2. Explore the semantic model (no Azure needed)

Browse the TMDL files to see how a Power BI semantic model looks in source control:

```
demo-enterprise/bi-repo/powerbi/workspaces/regional-sales-trust-demo/pbip/
└── demo_dataset.SemanticModel/definition/
    ├── model.tmdl
    ├── relationships.tmdl
    └── tables/
        ├── Fact Sales.tmdl      # 7 measures defined here
        ├── Dim Region.tmdl
        ├── Dim Product.tmdl
        ├── Dim Date.tmdl
        └── Dim Channel.tmdl
```

### 3. Run offline validation

These commands work without any Azure/Power BI connection:

```bash
# Validate Python code compiles
python -m compileall src scripts

# Run unit tests
python -m pytest -q

# Inspect the semantic model and report
python scripts/evaluate_pbip_for_testing.py

# Generate draft test scenarios from model metadata
python scripts/generate_measure_test_scenarios.py
```

### 4. (Optional) Connect to Power BI Service

To run live DAX queries against a published dataset:

```bash
cp .env.example .env
# Edit .env with your Azure AD app registration details
# See docs/operations/auth-prerequisites.md for setup guide
```

## Key Concepts

### PBIP Source Control
Power BI Desktop can now save projects as PBIP — a folder of human-readable TMDL, JSON, and metadata files. This makes semantic models diffable, reviewable, and testable.

### Measure Validation Templates
A CSV file (`tests/measure-validation/templates/measure_validation_template.csv`) acts as the source of truth for validation scenarios. Each row defines a test case with:
- The measure and its DAX expression
- A scenario type (divide_by_zero, grand_total, happy_path, regression, etc.)
- Expected behavior and comparison rules
- Review status tracking (draft → human_reviewed → approved)

### Automated Scenario Generation
Python scripts parse TMDL files to discover measures, detect risky patterns (DIVIDE, CALCULATE, time-intelligence), and generate draft test scenarios. These are suggestions — human review is always required before promotion.

### Risk Detection
The framework automatically flags measures that use:
- `DIVIDE` — potential divide-by-zero
- `CALCULATE` / `ALL` / `ALLEXCEPT` — context alteration
- `DISTINCTCOUNT` — non-additive grand-total behavior
- Time-intelligence functions — period boundary edge cases

## Repository Structure

```
.
├── demo-enterprise/
│   └── bi-repo/powerbi/.../pbip/          # PBIP + TMDL semantic model
│       └── assets/data/                    # Sample CSV data
├── src/
│   ├── auth/                               # Delegated & service principal auth
│   ├── clients/                            # Power BI REST API client
│   ├── config/                             # Config loading (env + YAML)
│   ├── validation/                         # PBIP inspection & scenario generation
│   └── semantic_model/                     # Model documentation helpers
├── scripts/
│   ├── cli/                                # CLI utilities (auth, DAX, export, etc.)
│   ├── evaluate_pbip_for_testing.py        # Inspect model + report
│   └── generate_measure_test_scenarios.py  # Generate draft test cases
├── tests/
│   ├── unit/                               # Python unit tests
│   └── measure-validation/                 # CSV templates & generated scenarios
├── notebooks/                              # Jupyter demo workflows
├── docs/                                   # Architecture, data model, operations
└── config/                                 # Config templates (.env.example, YAML examples)
```

## Validation Commands Reference

```bash
# Compile check
python -m compileall src scripts

# Unit tests
python -m pytest -q

# TMDL semantic model validation
python scripts/cli/validate_tmdl_semantic_model.py

# Inspect PBIP for testing opportunities
python scripts/evaluate_pbip_for_testing.py

# Generate draft test scenarios
python scripts/generate_measure_test_scenarios.py

# Merge scenarios into validation template
python scripts/generate_measure_validation_template.py
```

## Prerequisites (for live API features)

- Python 3.10+
- An Azure AD app registration with Power BI API permissions
- A Power BI workspace with a published dataset
- See [docs/operations/auth-prerequisites.md](docs/operations/auth-prerequisites.md) for detailed setup

## Documentation

- [Repository Architecture](docs/architecture/repo-architecture.md)
- [System Context](docs/architecture/system-context.md)
- [Semantic Model Overview](docs/data-model/semantic-model-overview.md)
- [Measure Design Guidelines](docs/data-model/measure-design-guidelines.md)
- [Measure Validation Workflow](docs/measure-validation.md)
- [Testing Strategy](docs/testing-strategy.md)
- [Local Setup](docs/operations/local-setup.md)
- [Auth Prerequisites](docs/operations/auth-prerequisites.md)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
