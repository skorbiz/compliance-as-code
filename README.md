# Compliance as Code

Proof-of-concept for managing compliance documents as code.

[![Build and Test](https://github.com/skorbiz/compliance-as-code/actions/workflows/build-and-test.yml/badge.svg?branch=main)](https://github.com/skorbiz/compliance-as-code/actions/workflows/build-and-test.yml)

## Documents

📦 **Download Latest Documents** (automatically updated on every commit to main):

- **[CE Declaration (PDF)](https://github.com/skorbiz/compliance-as-code/releases/download/latest/ce.pdf)** - EU conformity declaration
- **[Risk Assessment (PDF)](https://github.com/skorbiz/compliance-as-code/releases/download/latest/risk-assessment.pdf)** - CRA cybersecurity risk assessment  
- **[Manual (PDF)](https://github.com/skorbiz/compliance-as-code/releases/download/latest/manual.pdf)** - User manual
- **[SBOM (PDF)](https://github.com/skorbiz/compliance-as-code/releases/download/latest/sbom.pdf)** - Software Bill of Materials (compliance document; not a replacement for CI-generated CycloneDX/SPDX SBOMs)

*Note: The SBOM document is a compliance artifact. For machine-readable SBOMs, generate CycloneDX/SPDX format in your CI pipeline.*

## Quick Start

```bash
# Setup
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"

# Build all documents (default - validates, exports schemas, and builds)
python main.py

# Build single document in watch mode
python main.py ce
python main.py risk
python main.py manual
python main.py sbom

# Build without validation or schema export
python main.py --skip-validate --skip-export-schemas

# Run tests
pytest tests/
```

## Project Structure

```
docs/           # Typst document sources
data/           # YAML data files (risks, sbom)
schemas/        # JSON schemas for VS Code
schemas.py      # Pydantic schema definitions
main.py         # Build tool
tests/          # Tests
```

## Tooling

- **Typst** - Document compilation
- **Python + Pydantic** - Build orchestration and YAML validation
- **UV** - Python package management
