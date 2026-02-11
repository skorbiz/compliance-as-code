#!/usr/bin/env python3
"""
Export JSON Schemas from Pydantic models.

This script generates JSON Schema files from the Pydantic models for use
in documentation, IDE validation, and other tooling.
"""

import sys

from compliance_tools import export_all_schemas


def main():
    """Export all schemas."""
    success = export_all_schemas()
    
    if success:
        print("You can use these JSON Schemas with:")
        print("  - VS Code YAML extension for auto-completion")
        print("  - Other validation tools")
        print("  - API documentation")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
