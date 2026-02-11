"""
Compliance as Code - Core Library

Shared validation and export functions used by CLI tools.
"""

import json
import sys
from pathlib import Path
from typing import Type

import yaml
from pydantic import BaseModel, ValidationError

from schemas.risk_assessment import RiskModel, RiskRegister
from schemas.sbom import SBOMGenerated, SBOMManual


# ============================================================================
# YAML Validation
# ============================================================================

def validate_yaml_file(
    file_path: Path,
    schema_class: Type[BaseModel],
    verbose: bool = False
) -> bool:
    """
    Validate a YAML file against a Pydantic schema.
    
    Args:
        file_path: Path to YAML file
        schema_class: Pydantic model class to validate against
        verbose: Show detailed validation output
        
    Returns:
        True if valid, False otherwise
    """
    try:
        with open(file_path) as f:
            data = yaml.safe_load(f)
        
        schema_class.model_validate(data)
        
        if verbose:
            print(f"  ✓ {file_path} - Valid")
        
        return True
        
    except FileNotFoundError:
        print(f"  ✗ {file_path} - File not found", file=sys.stderr)
        return False
        
    except yaml.YAMLError as e:
        print(f"  ✗ {file_path} - Invalid YAML", file=sys.stderr)
        if verbose:
            print(f"    Error: {e}", file=sys.stderr)
        return False
        
    except ValidationError as e:
        print(f"  ✗ {file_path} - Validation failed", file=sys.stderr)
        if verbose:
            print("    Errors:", file=sys.stderr)
            for error in e.errors():
                loc = " → ".join(str(x) for x in error["loc"])
                print(f"      {loc}: {error['msg']}", file=sys.stderr)
        else:
            print(f"    Run with --verbose for details", file=sys.stderr)
        return False


def validate_all_yaml(verbose: bool = False) -> bool:
    """
    Validate all YAML files used in compliance documents.
    
    Args:
        verbose: Show detailed validation output
        
    Returns:
        True if all files are valid, False otherwise
    """
    print("\n" + "="*60)
    print("YAML Schema Validation")
    print("="*60)
    
    files_to_validate = [
        (Path("risk-assessment/model.yaml"), RiskModel, "Risk Assessment"),
        (Path("risk-assessment/risks.yaml"), RiskRegister, "Risk Assessment"),
        (Path("software-bill-of-materials/sbom_manual.yaml"), SBOMManual, "SBOM"),
        (Path("software-bill-of-materials/sbom_generated.yaml"), SBOMGenerated, "SBOM"),
    ]
    
    # Group by category for output
    categories = {}
    for path, schema, category in files_to_validate:
        if category not in categories:
            categories[category] = []
        categories[category].append((path, schema))
    
    results = []
    for category, files in categories.items():
        print(f"\n{category}:")
        print("-" * 60)
        for path, schema in files:
            results.append(validate_yaml_file(path, schema, verbose))
    
    # Summary
    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✓ All {total} YAML files validated successfully")
        print("="*60 + "\n")
        return True
    else:
        failed = total - passed
        print(f"✗ {failed}/{total} YAML files failed validation", file=sys.stderr)
        print("="*60 + "\n")
        return False


# ============================================================================
# JSON Schema Export
# ============================================================================

def export_json_schema(
    model_class: Type[BaseModel],
    output_path: Path,
    title: str = None
) -> bool:
    """
    Export a Pydantic model as JSON Schema.
    
    Args:
        model_class: Pydantic model class
        output_path: Path to output JSON file
        title: Optional title for the schema
        
    Returns:
        True if successful, False otherwise
    """
    try:
        schema = model_class.model_json_schema()
        
        if title:
            schema["title"] = title
        
        # Add metadata
        schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
        schema["description"] = model_class.__doc__ or ""
        
        # Add auto-generated warning
        schema["$comment"] = (
            "⚠️  AUTO-GENERATED FILE - DO NOT EDIT MANUALLY\n"
            "This JSON Schema is automatically generated from Pydantic models.\n"
            "To make changes, edit the Pydantic schema in schemas/ and run: python3 main.py --export-schemas"
        )
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write with header comment
        with open(output_path, "w") as f:
            f.write("// ⚠️  AUTO-GENERATED FILE - DO NOT EDIT MANUALLY\n")
            f.write("// This JSON Schema is automatically generated from Pydantic models.\n")
            f.write("// To make changes, edit the Pydantic schema in schemas/ and run:\n")
            f.write("//   python3 main.py --export-schemas\n")
            f.write("//\n")
            json.dump(schema, f, indent=2)
        
        return True
        
    except Exception as e:
        print(f"  ✗ Failed to export {output_path}: {e}", file=sys.stderr)
        return False


def export_all_schemas() -> bool:
    """
    Export all Pydantic schemas to JSON Schema format.
    
    Returns:
        True if all exports successful, False otherwise
    """
    print("\n" + "="*60)
    print("Exporting JSON Schemas")
    print("="*60 + "\n")
    
    output_dir = Path("schemas/generated-json-schemas")
    
    schemas_to_export = [
        (RiskModel, output_dir / "risk-model.schema.json", "Risk Assessment Model"),
        (RiskRegister, output_dir / "risk-register.schema.json", "Risk Register"),
        (SBOMManual, output_dir / "sbom-manual.schema.json", "Manual SBOM"),
        (SBOMGenerated, output_dir / "sbom-generated.schema.json", "Generated SBOM"),
    ]
    
    results = []
    for model_class, output_path, title in schemas_to_export:
        success = export_json_schema(model_class, output_path, title)
        if success:
            print(f"  ✓ {output_path}")
        results.append(success)
    
    print("\n" + "="*60)
    if all(results):
        print(f"✓ All {len(results)} schemas exported successfully")
        print(f"  Output: {output_dir}/")
        print("="*60 + "\n")
        return True
    else:
        failed = len(results) - sum(results)
        print(f"✗ {failed}/{len(results)} schemas failed to export", file=sys.stderr)
        print("="*60 + "\n")
        return False
