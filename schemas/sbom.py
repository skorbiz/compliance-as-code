"""
Pydantic schemas for SBOM (Software Bill of Materials) YAML files.

Defines the structure for:
- sbom_manual.yaml: Manually tracked components
- sbom_generated.yaml: Auto-generated dependencies
"""

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ComponentType(str, Enum):
    """Types of software components."""
    LIBRARY = "Library"
    FRAMEWORK = "Framework"
    RUNTIME = "Runtime"
    OPERATING_SYSTEM = "Operating System"
    DOCUMENT_COMPILER = "Document Compiler"
    PYTHON_PACKAGE = "Python Package"
    FIRMWARE = "Firmware"
    HARDWARE = "Hardware"
    TOOL = "Tool"
    APPLICATION = "Application"


class SourceType(str, Enum):
    """Source of the component."""
    REGISTRY = "registry"
    GIT = "git"
    PATH = "path"
    URL = "url"


# Manual SBOM schemas
class SBOMMetadata(BaseModel):
    """Metadata for the SBOM document."""
    product_name: str = Field(min_length=3, description="Product name")
    product_version: str = Field(
        pattern=r"^\d+\.\d+\.\d+$",
        description="Product version (semver)"
    )
    vendor: str = Field(min_length=3, description="Vendor/manufacturer name")
    release_date: date = Field(description="Release date")
    sbom_version: str = Field(
        pattern=r"^\d+\.\d+$",
        description="SBOM document version"
    )

    @field_validator("release_date")
    @classmethod
    def validate_release_date_not_future(cls, v: date) -> date:
        """Ensure release date is not in the future."""
        if v > date.today():
            raise ValueError("Release date cannot be in the future")
        return v


class ManualComponent(BaseModel):
    """Manually tracked component in SBOM."""
    name: str = Field(min_length=2, description="Component name")
    version: str = Field(min_length=1, description="Component version")
    type: str = Field(min_length=3, description="Component type")
    license: str = Field(min_length=2, description="License identifier")
    description: Optional[str] = Field(None, description="Component description")
    supplier: Optional[str] = Field(None, description="Component supplier/manufacturer")

    @field_validator("license")
    @classmethod
    def validate_license_format(cls, v: str) -> str:
        """Validate license is not 'Unknown' or empty."""
        if v.lower() in ("unknown", "n/a", ""):
            raise ValueError("License must be specified (use SPDX identifier or 'Proprietary')")
        return v


class SBOMManual(BaseModel):
    """Manual SBOM file (sbom_manual.yaml)."""
    metadata: SBOMMetadata = Field(description="SBOM metadata")
    components: list[ManualComponent] = Field(
        min_length=0,
        description="Manually tracked components"
    )

    @field_validator("components")
    @classmethod
    def validate_unique_components(cls, v: list[ManualComponent]) -> list[ManualComponent]:
        """Ensure component names are unique."""
        names = [comp.name for comp in v]
        if len(names) != len(set(names)):
            duplicates = [name for name in names if names.count(name) > 1]
            raise ValueError(f"Component names must be unique. Duplicates: {set(duplicates)}")
        return v


# Generated SBOM schemas
class GeneratedComponent(BaseModel):
    """Auto-generated component (Python dependency)."""
    name: str = Field(min_length=2, description="Package name")
    version: str = Field(min_length=1, description="Package version")
    type: str = Field(min_length=3, description="Component type")
    source: Optional[SourceType] = Field(None, description="Source type")

    @field_validator("version")
    @classmethod
    def validate_version_format(cls, v: str) -> str:
        """Validate version is specified."""
        if v.lower() in ("unknown", "unspecified", ""):
            raise ValueError("Version must be specified or use constraint (e.g., >=1.0)")
        return v


class SBOMGenerated(BaseModel):
    """Generated SBOM file (sbom_generated.yaml)."""
    components: list[GeneratedComponent] = Field(
        default_factory=list,
        description="Auto-generated components"
    )

    @field_validator("components")
    @classmethod
    def validate_unique_components(cls, v: list[GeneratedComponent]) -> list[GeneratedComponent]:
        """Ensure component names are unique."""
        if not v:  # Allow empty list
            return v
        
        names = [comp.name for comp in v]
        if len(names) != len(set(names)):
            duplicates = [name for name in names if names.count(name) > 1]
            raise ValueError(f"Component names must be unique. Duplicates: {set(duplicates)}")
        return v


# Combined SBOM for validation across both files
class CombinedSBOM(BaseModel):
    """Combined validation of manual and generated SBOMs."""
    manual: SBOMManual
    generated: SBOMGenerated

    @field_validator("manual", mode="after")
    @classmethod
    def validate_no_overlap(cls, manual: SBOMManual, info) -> SBOMManual:
        """Warn if components appear in both manual and generated."""
        if "generated" not in info.data:
            return manual
        
        generated = info.data["generated"]
        manual_names = {comp.name.lower() for comp in manual.components}
        generated_names = {comp.name.lower() for comp in generated.components}
        
        overlap = manual_names & generated_names
        if overlap:
            import warnings
            warnings.warn(
                f"Components appear in both manual and generated SBOM: {overlap}. "
                "Consider removing from manual SBOM.",
                UserWarning
            )
        
        return manual
