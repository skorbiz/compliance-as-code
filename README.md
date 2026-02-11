# Compliance as Code

Proof-of-concept for managing compliance documents as code.

## Documents

- **CE Declaration** - EU conformity declaration
- **Risk Assessment** - CRA cybersecurity risk assessment  
- **Manual** - User manual
- **SBOM** - Software Bill of Materials

## Quick Start

```bash
# Setup
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"

# Validate YAML files
python main.py --validate

# Build all documents
python main.py --all

# Build single document
python main.py ce
python main.py risk
python main.py manual
python main.py sbom

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
- **Python + Pydantic** - YAML validation
- **UV** - Python package management
