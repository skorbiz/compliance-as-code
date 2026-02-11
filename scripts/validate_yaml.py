#!/usr/bin/env python3
"""
Validate YAML files against Pydantic schemas.

Usage:
    python3 scripts/validate_yaml.py                    # Validate all files
    python3 scripts/validate_yaml.py --risk             # Validate risk assessment
    python3 scripts/validate_yaml.py --sbom             # Validate SBOM
    python3 scripts/validate_yaml.py --verbose          # Show detailed output
"""

import argparse
import sys
from pathlib import Path

from compliance_tools import validate_yaml_file
from schemas.risk_assessment import RiskModel, RiskRegister
from schemas.sbom import SBOMGenerated, SBOMManual


def main():
    parser = argparse.ArgumentParser(
        description="Validate YAML files against Pydantic schemas"
    )
    parser.add_argument(
        "--risk",
        action="store_true",
        help="Validate risk assessment files only"
    )
    parser.add_argument(
        "--sbom",
        action="store_true",
        help="Validate SBOM files only"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed validation output"
    )
    
    args = parser.parse_args()
    
    # Determine which files to validate
    validate_risk = args.risk or (not args.risk and not args.sbom)
    validate_sbom = args.sbom or (not args.risk and not args.sbom)
    
    print("YAML Schema Validation")
    print("=" * 50)
    print()
    
    results = []
    
    # Validate risk assessment files
    if validate_risk:
        print("Risk Assessment:")
        print("-" * 50)
        results.append(validate_yaml_file(
            Path("risk-assessment/model.yaml"),
            RiskModel,
            args.verbose
        ))
        results.append(validate_yaml_file(
            Path("risk-assessment/risks.yaml"),
            RiskRegister,
            args.verbose
        ))
        print()
    
    # Validate SBOM files
    if validate_sbom:
        print("Software Bill of Materials:")
        print("-" * 50)
        results.append(validate_yaml_file(
            Path("software-bill-of-materials/sbom_manual.yaml"),
            SBOMManual,
            args.verbose
        ))
        results.append(validate_yaml_file(
            Path("software-bill-of-materials/sbom_generated.yaml"),
            SBOMGenerated,
            args.verbose
        ))
        print()
    
    # Summary
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✓ All {total} files validated successfully")
        return 0
    else:
        failed = total - passed
        print(f"✗ {failed}/{total} files failed validation")
        return 1


if __name__ == "__main__":
    sys.exit(main())
