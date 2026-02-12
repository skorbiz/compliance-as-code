#!/usr/bin/env python3
"""
Compliance as Code - Build Tool

Simple wrapper around Typst for building compliance documents.
"""

import argparse
import subprocess
import sys
from pathlib import Path

import yaml
from pydantic import ValidationError

from schemas import RiskModel, RiskRegister, SBOMGenerated


DOCS = {
    "ce": "docs/ce.typ",
    "manual": "docs/manual.typ",
    "sbom": "docs/sbom.typ",
    "risk": "docs/risk-assessment.typ",
}

YAML_FILES = [
    ("data/model.yaml", RiskModel),
    ("data/risks.yaml", RiskRegister),
    ("data/sbom.yaml", SBOMGenerated),
]


def validate_yaml() -> bool:
    """Validate all YAML files against schemas."""
    print("Validating YAML files...")
    all_valid = True
    
    for path, schema in YAML_FILES:
        try:
            with open(path) as f:
                data = yaml.safe_load(f)
            schema.model_validate(data)
            print(f"  ✓ {path}")
        except FileNotFoundError:
            print(f"  ✗ {path} - not found")
            all_valid = False
        except ValidationError as e:
            print(f"  ✗ {path} - validation failed")
            for err in e.errors():
                loc = " → ".join(str(x) for x in err["loc"])
                print(f"      {loc}: {err['msg']}")
            all_valid = False
    
    return all_valid


def build_doc(name: str, watch: bool = False) -> int:
    """Build a single document."""
    source = Path(DOCS[name])
    if not source.exists():
        print(f"Error: {source} not found")
        return 1
    
    output = source.with_suffix(".pdf")
    mode = "watch" if watch else "compile"
    cmd = ["typst", mode, "--root", ".", str(source), str(output)]
    
    if watch:
        print(f"Watching {source} for changes... (Ctrl+C to stop)")
    else:
        print(f"Building {source}...")
    
    return subprocess.run(cmd).returncode


def export_schemas() -> None:
    """Export JSON schemas for VS Code."""
    import json
    out_dir = Path("schemas-generated/json-schemas")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    schemas_to_export = [
        (RiskModel, "risk-model"),
        (RiskRegister, "risk-register"),
        (SBOMGenerated, "sbom-generated"),
    ]
    
    for model, name in schemas_to_export:
        schema = model.model_json_schema()
        with open(out_dir / f"{name}.schema.json", "w") as f:
            json.dump(schema, f, indent=2)
    print(f"Exported schemas to {out_dir}")


def main():
    parser = argparse.ArgumentParser(description="Build compliance documents")
    parser.add_argument("--all", action="store_true", help="Build all documents")
    parser.add_argument("--skip-validate", action="store_true", help="Skip YAML validation")
    parser.add_argument("--skip-export-schemas", action="store_true", help="Skip exporting JSON schemas")
    parser.add_argument("doc", nargs="?", choices=list(DOCS.keys()), help="Document to build")
    
    args = parser.parse_args()
    
    # Validate YAML files (unless skipped)
    if not args.skip_validate:
        if not validate_yaml():
            print("\n⚠️  Fix YAML errors before building.")
            return 1
    
    # Export schemas (unless skipped)
    if not args.skip_export_schemas:
        export_schemas()
    
    if args.all:
        codes = [build_doc(name) for name in DOCS]
        return max(codes) if codes else 0
    
    if args.doc:
        return build_doc(args.doc, watch=True)
    
    # If no build target specified, just validation and export were done
    if not args.all and not args.doc:
        print("\nNo build target specified. Use --all or specify a document.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
