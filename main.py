#!/usr/bin/env python3
"""
Compliance as Code - Document Build Tool

This tool wraps Typst compilation commands to provide a familiar
Python-based workflow for building compliance documents.

Workflow:
1. Validate YAML files against schemas
2. Export JSON Schemas for tooling
3. Generate SBOM data from dependencies
4. Build PDF documents
"""

import argparse
import subprocess
import sys
from pathlib import Path

from compliance_tools import validate_all_yaml, export_all_schemas


def run_typst(source_file: Path, output_file: Path | None = None, watch: bool = False) -> int:
    """
    Run Typst to compile a document.
    
    Args:
        source_file: Path to the .typ source file
        output_file: Optional output PDF path (defaults to same name as source)
        watch: If True, watch for changes and recompile automatically
        
    Returns:
        Exit code from Typst command
    """
    if not source_file.exists():
        print(f"Error: Source file not found: {source_file}", file=sys.stderr)
        return 1
    
    cmd = ["typst"]
    
    if watch:
        cmd.append("watch")
    else:
        cmd.append("compile")
    
    cmd.append(str(source_file))
    
    if output_file:
        cmd.append(str(output_file))
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd)
        return result.returncode
    except FileNotFoundError:
        print("Error: Typst not found. Please ensure Typst is installed.", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nBuild interrupted by user")
        return 130


def build_ce_declaration(watch: bool = False) -> int:
    """Build the CE declaration document."""
    source = Path("ce-declaration/ce.typ")
    output = Path("ce-declaration/ce.pdf")
    return run_typst(source, output, watch=watch)


def build_manual(watch: bool = False) -> int:
    """Build the user manual document."""
    source = Path("manual/manual.typ")
    output = Path("manual/manual.pdf")
    return run_typst(source, output, watch=watch)


def build_sbom(watch: bool = False, generate: bool = True) -> int:
    """Build the Software Bill of Materials document."""
    if generate:
        print("Generating SBOM data from dependencies...")
        result = subprocess.run([
            sys.executable,
            "software-bill-of-materials/scripts/generate_sbom.py"
        ])
        if result.returncode != 0:
            print("Warning: SBOM generation failed, continuing with existing data", file=sys.stderr)
    
    source = Path("software-bill-of-materials/sbom.typ")
    output = Path("software-bill-of-materials/sbom.pdf")
    return run_typst(source, output, watch=watch)


def build_risk_assessment(watch: bool = False) -> int:
    """Build the risk assessment document."""
    source = Path("risk-assessment/risk-assessment.typ")
    output = Path("risk-assessment/risk-assessment.pdf")
    return run_typst(source, output, watch=watch)


def build_all(watch: bool = False, skip_validation: bool = False, skip_export: bool = False) -> int:
    """Build all compliance documents with full workflow."""
    documents = [
        ("ce-declaration/ce.typ", "ce-declaration/ce.pdf"),
        ("manual/manual.typ", "manual/manual.pdf"),
        ("software-bill-of-materials/sbom.typ", "software-bill-of-materials/sbom.pdf"),
        ("risk-assessment/risk-assessment.typ", "risk-assessment/risk-assessment.pdf"),
    ]
    
    if watch:
        print("Watch mode only supports one document at a time.")
        print("Building CE declaration in watch mode...")
        return build_ce_declaration(watch=True)
    
    # Step 1: Validate YAML files
    if not skip_validation:
        if not validate_all_yaml():
            print("\n⚠️  YAML validation failed. Fix errors before building documents.", file=sys.stderr)
            return 1
    
    # Step 2: Export JSON Schemas
    if not skip_export:
        if not export_all_schemas():
            print("\n⚠️  Schema export failed. Continuing with build...", file=sys.stderr)
    
    # Step 3: Generate SBOM data
    print("="*60)
    print("Generating SBOM Data")
    print("="*60)
    subprocess.run([sys.executable, "software-bill-of-materials/scripts/generate_sbom.py"])
    print()
    
    # Step 4: Build all documents
    print("="*60)
    print("Building Documents")
    print("="*60 + "\n")
    
    exit_codes = []
    for source, output in documents:
        source_path = Path(source)
        if source_path.exists():
            print(f"Building {source}...")
            code = run_typst(source_path, Path(output), watch=False)
            exit_codes.append(code)
            print()
        else:
            print(f"Skipping {source} (not found)")
    
    # Summary
    print("="*60)
    if exit_codes and max(exit_codes) == 0:
        print("✓ All documents built successfully")
    else:
        print("✗ Some documents failed to build", file=sys.stderr)
    print("="*60)
    
    return max(exit_codes) if exit_codes else 0


def main():
    parser = argparse.ArgumentParser(
        description="Build compliance documents using Typst with YAML validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Workflow (with --all):
  1. Validate YAML files against schemas
  2. Export JSON Schemas for tooling
  3. Generate SBOM data from dependencies
  4. Build PDF documents

Examples:
  %(prog)s --all              Full workflow: validate, export, generate, build
  %(prog)s --validate-only    Only validate YAML files
  %(prog)s --export-schemas   Only export JSON schemas
  %(prog)s --all --skip-validation   Build without validation (not recommended)
  
  %(prog)s --ce               Build CE declaration only
  %(prog)s --manual           Build user manual only
  %(prog)s --sbom             Build Software Bill of Materials
  %(prog)s --risk             Build risk assessment
  
  %(prog)s --ce --watch       Build CE declaration and watch for changes
  %(prog)s ce-declaration/ce.typ  Build specific file directly
        """
    )
    
    parser.add_argument(
        "source",
        nargs="?",
        type=Path,
        help="Path to .typ source file to compile"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output PDF file path"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Build all compliance documents"
    )
    
    parser.add_argument(
        "--ce",
        action="store_true",
        help="Build CE declaration"
    )
    
    parser.add_argument(
        "--manual",
        action="store_true",
        help="Build user manual"
    )
    
    parser.add_argument(
        "--sbom",
        action="store_true",
        help="Build Software Bill of Materials"
    )
    
    parser.add_argument(
        "--risk",
        action="store_true",
        help="Build risk assessment"
    )
    
    parser.add_argument(
        "--no-generate",
        action="store_true",
        help="Skip SBOM data generation (use existing data)"
    )
    
    parser.add_argument(
        "-w", "--watch",
        action="store_true",
        help="Watch for changes and rebuild automatically"
    )
    
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip YAML schema validation (not recommended)"
    )
    
    parser.add_argument(
        "--skip-export",
        action="store_true",
        help="Skip JSON schema export"
    )
    
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate YAML files, don't build"
    )
    
    parser.add_argument(
        "--export-schemas",
        action="store_true",
        help="Only export JSON schemas, don't build"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed validation output"
    )
    
    args = parser.parse_args()
    
    # Handle validation-only mode
    if args.validate_only:
        return 0 if validate_all_yaml(verbose=args.verbose) else 1
    
    # Handle export-only mode
    if args.export_schemas:
        return 0 if export_all_schemas() else 1
    
    # Determine what to build
    if args.all:
        return build_all(
            watch=args.watch,
            skip_validation=args.skip_validation,
            skip_export=args.skip_export
        )
    elif args.ce:
        return build_ce_declaration(watch=args.watch)
    elif args.manual:
        return build_manual(watch=args.watch)
    elif args.sbom:
        return build_sbom(watch=args.watch, generate=not args.no_generate)
    elif args.risk:
        return build_risk_assessment(watch=args.watch)
    elif args.source:
        return run_typst(args.source, args.output, watch=args.watch)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
