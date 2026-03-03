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

from model.schemas import RiskModel, RiskRegister, SBOMGenerated


DOCS = {
    "ce": "docs/ce.typ",
    "manual": "docs/manual.typ",
    "sbom": "docs/sbom.typ",
    "risk": "docs/risk-assessment.typ",
}

WEBSITE_DIR = Path("website")
DOCUSAURUS_GENERATOR = Path("website/scripts/generate_docs_from_yaml.py")

YAML_FILES = [
    ("model/risk_model.yaml", RiskModel),
    ("model/risks.yaml", RiskRegister),
    ("model/sbom.yaml", SBOMGenerated),
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


def build_website(watch: bool = False) -> int:
    """Build or watch the Docusaurus website."""
    # Generate markdown from YAML
    print("→ Generating docs from YAML...")
    result = subprocess.run([sys.executable, str(DOCUSAURUS_GENERATOR)])
    if result.returncode != 0:
        return result.returncode

    # Install/update dependencies if needed
    node_modules = WEBSITE_DIR / "node_modules"
    package_lock = WEBSITE_DIR / "package-lock.json"
    
    if not node_modules.exists():
        print("→ Installing dependencies...")
        npm_cmd = ["npm", "ci" if package_lock.exists() else "install"]
        result = subprocess.run(npm_cmd, cwd=WEBSITE_DIR)
        if result.returncode != 0:
            return result.returncode

    # Build or serve
    mode = "start" if watch else "build"
    action = "Starting dev server" if watch else "Building static site"
    print(f"→ {action}...")
    
    return subprocess.run(["npm", "run", mode], cwd=WEBSITE_DIR).returncode


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
    parser.add_argument("--web", action="store_true", help="Generate and build static Docusaurus website")
    parser.add_argument("--web-watch", action="store_true", help="Generate and run Docusaurus in watch mode")
    parser.add_argument("--skip-validate", action="store_true", help="Skip YAML validation")
    parser.add_argument("--skip-export-schemas", action="store_true", help="Skip exporting JSON schemas")
    parser.add_argument("doc", nargs="?", choices=list(DOCS.keys()), help="Typst document to build in watch mode")
    
    args = parser.parse_args()

    if args.web and args.web_watch:
        parser.error("Choose either --web or --web-watch, not both.")
    if args.doc and (args.web or args.web_watch):
        parser.error("Cannot combine a Typst watch target with website options.")
    
    # Validate YAML files (unless skipped)
    if not args.skip_validate:
        if not validate_yaml():
            print("\n⚠️  Fix YAML errors before building.")
            return 1
    
    # Export schemas (unless skipped)
    if not args.skip_export_schemas:
        export_schemas()

    # Build website
    if args.web_watch:
        return build_website(watch=True)
    if args.web:
        return build_website(watch=False)
    
    # Build documents
    if args.doc:
        # Single document in watch mode
        return build_doc(args.doc, watch=True)
    else:
        # Default: build all documents (or explicit --all)
        codes = [build_doc(name) for name in DOCS]
        return max(codes) if codes else 0


if __name__ == "__main__":
    sys.exit(main())
