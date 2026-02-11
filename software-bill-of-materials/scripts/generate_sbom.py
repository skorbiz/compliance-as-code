#!/usr/bin/env python3
"""
Generate Software Bill of Materials (SBOM) from Python dependencies.

This script extracts dependency information from pyproject.toml and uv.lock
and generates a YAML file for inclusion in the SBOM document.
"""

import sys
import tomllib
from pathlib import Path
from datetime import datetime


def extract_dependencies_from_pyproject(pyproject_path: Path) -> dict:
    """Extract dependencies from pyproject.toml."""
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)
    
    project = data.get("project", {})
    dependencies = project.get("dependencies", [])
    
    # Parse dependencies (simple version, doesn't handle complex constraints)
    parsed_deps = []
    for dep in dependencies:
        # Handle different formats: "package", "package>=1.0", "package==1.0.0"
        name = dep.split(">")[0].split("=")[0].split("<")[0].split("!")[0].strip()
        
        # Try to extract version if specified
        version = "unspecified"
        if "==" in dep:
            version = dep.split("==")[1].split(",")[0].strip()
        elif ">=" in dep:
            version = ">=" + dep.split(">=")[1].split(",")[0].strip()
        
        parsed_deps.append({
            "name": name,
            "version": version,
            "type": "Python Package"
        })
    
    return parsed_deps


def extract_dependencies_from_lock(lock_path: Path) -> dict:
    """Extract dependencies from uv.lock file."""
    if not lock_path.exists():
        return []
    
    with open(lock_path, "rb") as f:
        data = tomllib.load(f)
    
    packages = data.get("package", [])
    
    parsed_deps = []
    for pkg in packages:
        name = pkg.get("name", "unknown")
        version = pkg.get("version", "unknown")
        source = pkg.get("source", {})
        
        # Determine source type
        if isinstance(source, dict):
            source_type = source.get("type", "registry")
        else:
            source_type = "registry"
        
        parsed_deps.append({
            "name": name,
            "version": version,
            "type": "Python Package",
            "source": source_type
        })
    
    return parsed_deps


def generate_sbom_yaml(output_path: Path, project_root: Path):
    """Generate SBOM YAML file."""
    pyproject_path = project_root / "pyproject.toml"
    lock_path = project_root / "uv.lock"
    
    # Try to get dependencies from lock file first (more accurate), fallback to pyproject
    if lock_path.exists():
        print(f"Reading dependencies from {lock_path}")
        dependencies = extract_dependencies_from_lock(lock_path)
    elif pyproject_path.exists():
        print(f"Reading dependencies from {pyproject_path}")
        dependencies = extract_dependencies_from_pyproject(pyproject_path)
    else:
        print("No pyproject.toml or uv.lock found!", file=sys.stderr)
        dependencies = []
    
    # Generate YAML content
    yaml_content = f"""# Auto-generated SBOM data
# Generated on: {datetime.now().isoformat()}

components:
"""
    
    if dependencies:
        for dep in dependencies:
            yaml_content += f"""  - name: "{dep['name']}"
    version: "{dep['version']}"
    type: "{dep['type']}"
"""
            if "source" in dep:
                yaml_content += f"""    source: "{dep['source']}"
"""
            yaml_content += "\n"
    else:
        yaml_content += "  # No dependencies found\n"
    
    # Write YAML file
    with open(output_path, "w") as f:
        f.write(yaml_content)
    
    print(f"Generated SBOM data: {output_path}")
    print(f"Found {len(dependencies)} dependencies")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate SBOM from Python dependencies")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("software-bill-of-materials/sbom_generated.yaml"),
        help="Output YAML file path"
    )
    parser.add_argument(
        "-r", "--root",
        type=Path,
        default=Path("."),
        help="Project root directory"
    )
    
    args = parser.parse_args()
    
    generate_sbom_yaml(args.output, args.root)


if __name__ == "__main__":
    main()
