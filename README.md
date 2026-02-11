The project is a proof-of-concept about about keeping compliance documents as code, that includes
- CE declaration
- Cyber security risk assessment
- Manual 
- Software bill of materials.

In this POC the content is less important. Its manly about getting the flow right.

# Tooling and frameworks

- Typst: Documents are compiled into pdfs using typst.
- Python and UV is used to wrap Typst compile commands to make the flow familiar to developers unfamiliar with typst
- Python: is used as a scripting language where needed. E.g. might be needed to fetch inputs to the SBOM
- YAML: The risk assesment inputs 
- VS code devcontainer: A devcontainer that installs the nessesary typst and python tools.


# Getting Started

## Setup

1. **Install Dependencies** (required once):
   ```bash
   # Create and activate virtual environment
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
   # Install Python packages
   uv pip install -e ".[dev]"
   ```

## Schema Validation

YAML validation is **automatically run** when building documents:

```bash
# Full workflow includes validation
python3 main.py --all

# Validate only (no build)
python3 main.py --validate-only

# Verbose validation output
python3 main.py --validate-only --verbose

# Export JSON Schemas
python3 main.py --export-schemas

# Run pytest test suite
pytest tests/ -v
```

**What's validated:**
- ✅ YAML structure matches expected schema
- ✅ Required fields are present
- ✅ Data types are correct (dates, versions, enums)
- ✅ Unique IDs and names
- ✅ Cross-references between files (e.g., risk categories exist in model)
- ✅ Business rules (e.g., review date after assessment date)
- ✅ Format validation (semver, risk IDs, hex colors)

**Export JSON Schemas** for use in other tools:
```bash
python3 scripts/export_schemas.py
```

This generates JSON Schema files in `schemas/generated-json-schemas/` for:
- VS Code YAML extension auto-completion
- CI/CD validation
- API documentation

## Building Documents

The project uses an integrated Python build tool that:
1. **Validates** YAML files against schemas
2. **Exports** JSON Schemas for tooling
3. **Generates** SBOM data from dependencies
4. **Builds** PDF documents with Typst

```bash
# Complete workflow: validate → export → generate → build
python3 main.py --all

# Quick validation and single document builds
python3 main.py --validate-only           # Only validate YAML
python3 main.py --export-schemas          # Only export schemas
python3 main.py --validate-only --verbose # Detailed validation output

# Build specific documents (still validates first)
python3 main.py --ce          # CE declaration
python3 main.py --manual      # User manual
python3 main.py --sbom        # Software Bill of Materials
python3 main.py --risk        # Risk assessment (CRA compliance)

# Advanced options
python3 main.py --all --skip-validation  # Skip validation (not recommended)
python3 main.py --all --skip-export      # Skip schema export

# Watch mode - auto-rebuild on file changes
python3 main.py --ce --watch

# Build a specific file directly
python3 main.py ce-declaration/ce.typ -o output.pdf
```

## Using Typst Directly

You can also use Typst commands directly:

```bash
# Compile a document
typst compile ce-declaration/ce.typ ce-declaration/ce.pdf

# Watch mode
typst watch ce-declaration/ce.typ ce-declaration/ce.pdf
```

## First Time Setup

1. Open this project in the VS Code devcontainer
2. Typst and Python are pre-installed in the devcontainer
3. Run `python3 main.py --ce` to build your first document


# File structure

```
/compliance_as_code/
  ce-declaration/
    ce.typ
  manual/
    manual.typ
  risk-assesment/
    model.yaml          # severity/probability definitions
    risks.yaml          # the actual risk register
    templates/
      risk_table.typ.template
      risk_matrix.typ.template
    scripts/
       render_risk_typst.py   # python script: read YAML -> produce .typ -> compile
  software-bill-of-materials/
    scripts/
      collect_and_gennerate.py
    sbom_gennerated.ymal
    sbom_manual.yaml
      templates/
        sbom.typ.template
  typst.bin
  uv.lock
  pyproject.toml
  main.py
  readme.md
```


# Document descriptions
## CE declaration
Plain 1 page document. 

✅ CE Declaration Document
ce.typ - Complete EU Declaration of Conformity with:
Manufacturer information section
Product details
Applicable EU directives (EMC, LVD, RoHS, WEEE)
Harmonized standards references
Signature fields
Professional formatting


## Manual
Simple manual that follows the CE declrations rules. Does not need any special inputs for now. Its main job is to be compliant and direct to our webpage for for an updated manual.

✅ User Manual Document
Created a complete manual.typ with:

Professional layout with headers/footers
Table of contents
Safety information section
Introduction and product overview
Detailed specifications table
Installation instructions
Operation guide with LED indicators
Maintenance procedures
Comprehensive troubleshooting table
Regulatory information (CE, FCC, WEEE)
Warranty and support information
Appendix with glossary and revision history
Placeholder images for company logo and WEEE symbol


## Cyber security risk assesment
Risk assesments are offten written in Excel.
The document needs to mimic this format and gennerate a risk assesment that will look familiar to what people are usually working with.

The risk assessment uses Typst's native YAML support to read risk data:
- `model.yaml` - Risk framework (severity/probability scales, risk levels, categories)
- `risks.yaml` - Risk register with all identified risks, controls, and CRA mappings

Features:
- Risk matrix (5×5 heat map)
- Detailed risk register with initial and residual risk ratings
- Control tracking (planned, in-progress, completed)
- CRA requirement mapping (Article 13, Article 14)
- Action items and review schedule
- Covers: Data security, access control, network security, software integrity, supply chain, availability, compliance, incident response

To update risks: Edit `risks.yaml` and rebuild with `python3 main.py --risk`

## SBOM
Python is used to extract dependencies for now. The script can be a dummy file of sorts. Maybe just pass the pyproject file or something as an example. I will need to connect to a larger repository at some point.
The typst template needs to handle both the auto-gennerated file but some things can also typed manually.

The SBOM uses Typst's native YAML support - no Jinja needed! The template reads from two YAML files:
- `sbom_generated.yaml` - Auto-extracted Python dependencies
- `sbom_manual.yaml` - Manually tracked components (OS, tools, firmware, etc.)

To update dependencies:
```bash
python3 software-bill-of-materials/scripts/generate_sbom.py
```

# Uncertainties and unknown

- Can the typst template be enough in of itself to pass the yaml input files. Or will we need something like jinja to gennerate the typst files. I would prefer just use typst if posible.