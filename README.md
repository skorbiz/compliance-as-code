# Compliance as Code

Proof-of-concept for managing compliance documents as code.
Motivation and discussion of the "compliance as code" approach can be found in the [Architecture/POC write-up](./0001-compliance-documents-as-code-poc.md).
It is written in an architectural decision record (ADR) format, which we use at work.

[![Build and Test](https://github.com/skorbiz/compliance-as-code/actions/workflows/build-and-test.yml/badge.svg)](https://github.com/skorbiz/compliance-as-code/actions/workflows/build-and-test.yml?query=branch%3Amain)
[![Deploy Docs Site](https://github.com/skorbiz/compliance-as-code/actions/workflows/deploy-docs-site.yml/badge.svg)](https://github.com/skorbiz/compliance-as-code/actions/workflows/deploy-docs-site.yml?query=branch%3Amain)

## Outputs

### Compliance documents

📦 **Download Latest Documents** (automatically updated on every commit to main):

- **[CE Declaration (PDF)](https://github.com/skorbiz/compliance-as-code/releases/download/latest/ce.pdf)** - EU conformity declaration
- **[Risk Assessment (PDF)](https://github.com/skorbiz/compliance-as-code/releases/download/latest/risk-assessment.pdf)** - CRA cybersecurity risk assessment  
- **[Manual (PDF)](https://github.com/skorbiz/compliance-as-code/releases/download/latest/manual.pdf)** - User manual
- **[SBOM (PDF)](https://github.com/skorbiz/compliance-as-code/releases/download/latest/sbom.pdf)** - Software Bill of Materials (compliance document; not a replacement for CI-generated CycloneDX/SPDX SBOMs)

### Secondary Outputs

- **[Documentation Site (Docusaurus)](https://skorbiz.github.io/compliance-as-code/)** - Web companion generated from the same YAML source data
- **[JSON Schemas](https://github.com/skorbiz/compliance-as-code/tree/main/schemas-generated/json-schemas)** - JSON schemas for IDE validation (e.g., YAML autocomplete/validation of risk_model.yaml in VS Code)

## Quick Start

```bash
# Build all Typst/PDF documents
uv run main.py # or python main.py (if not using the uv package manager)

# Build single document in watch mode
uv run main.py ce
uv run main.py risk
uv run main.py manual
uv run main.py sbom

# Build static Docusaurus site (auto-generates markdown from YAML)
uv run main.py --web
uv run main.py --web-watch # (dev server + auto-generate at startup)

# Build without validation or schema export
uv run main.py --skip-validate --skip-export-schemas

# Run tests
uv run pytest tests/
```


## Project Structure

```
docs/                   # Typst document sources
model/                  # YAML data files and Pydantic schemas
model/schemas.py        # Pydantic schema definitions
website/                # Docusaurus docs site
website/scripts/        # Utility scripts (YAML -> web docs)
schemas-generated/      # JSON schemas for VS Code
main.py                 # Build tool
tests/                  # Tests
```

## Tooling / Frameworks

- **Python + Pydantic** - Build orchestration, YAML validation, and risk modeling
- **Typst** - Document compilation
- **Docusaurus** - Web documentation site
- **GitHub Pages** - Automatic docs site deployment
- **UV** - Python package management
