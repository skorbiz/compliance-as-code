"""
Tests for SBOM YAML schema validation.

Validates:
- software-bill-of-materials/sbom_manual.yaml
- software-bill-of-materials/sbom_generated.yaml
"""

from pathlib import Path

import pytest
import yaml

from schemas.sbom import CombinedSBOM, SBOMGenerated, SBOMManual


# Fixtures
@pytest.fixture
def sbom_manual_path() -> Path:
    """Path to manual SBOM YAML file."""
    return Path("software-bill-of-materials/sbom_manual.yaml")


@pytest.fixture
def sbom_generated_path() -> Path:
    """Path to generated SBOM YAML file."""
    return Path("software-bill-of-materials/sbom_generated.yaml")


@pytest.fixture
def sbom_manual_data(sbom_manual_path: Path) -> dict:
    """Load manual SBOM YAML data."""
    with open(sbom_manual_path) as f:
        return yaml.safe_load(f)


@pytest.fixture
def sbom_generated_data(sbom_generated_path: Path) -> dict:
    """Load generated SBOM YAML data."""
    with open(sbom_generated_path) as f:
        return yaml.safe_load(f)


# Manual SBOM tests
class TestSBOMManual:
    """Tests for software-bill-of-materials/sbom_manual.yaml schema."""

    def test_manual_file_exists(self, sbom_manual_path: Path):
        """Test that sbom_manual.yaml exists."""
        assert sbom_manual_path.exists(), "sbom_manual.yaml not found"

    def test_manual_is_valid_yaml(self, sbom_manual_data: dict):
        """Test that sbom_manual.yaml is valid YAML."""
        assert isinstance(sbom_manual_data, dict), "sbom_manual.yaml must be a dictionary"

    def test_manual_validates_against_schema(self, sbom_manual_data: dict):
        """Test that sbom_manual.yaml validates against Pydantic schema."""
        sbom = SBOMManual.model_validate(sbom_manual_data)
        assert sbom is not None

    def test_metadata_has_valid_product_version(self, sbom_manual_data: dict):
        """Test that metadata has valid semver version."""
        sbom = SBOMManual.model_validate(sbom_manual_data)
        assert sbom.metadata.product_version.count(".") == 2

    def test_metadata_has_valid_sbom_version(self, sbom_manual_data: dict):
        """Test that metadata has valid SBOM version."""
        sbom = SBOMManual.model_validate(sbom_manual_data)
        assert sbom.metadata.sbom_version.count(".") == 1

    def test_release_date_not_in_future(self, sbom_manual_data: dict):
        """Test that release date is not in the future."""
        from datetime import date
        sbom = SBOMManual.model_validate(sbom_manual_data)
        assert sbom.metadata.release_date <= date.today()

    def test_all_components_have_licenses(self, sbom_manual_data: dict):
        """Test that all components have valid licenses."""
        sbom = SBOMManual.model_validate(sbom_manual_data)
        for component in sbom.components:
            assert component.license
            assert component.license.lower() not in ("unknown", "n/a", "")

    def test_component_names_are_unique(self, sbom_manual_data: dict):
        """Test that component names are unique."""
        sbom = SBOMManual.model_validate(sbom_manual_data)
        names = [comp.name for comp in sbom.components]
        assert len(names) == len(set(names)), "Component names must be unique"

    def test_all_components_have_versions(self, sbom_manual_data: dict):
        """Test that all components have versions."""
        sbom = SBOMManual.model_validate(sbom_manual_data)
        for component in sbom.components:
            assert component.version
            assert len(component.version) > 0


# Generated SBOM tests
class TestSBOMGenerated:
    """Tests for software-bill-of-materials/sbom_generated.yaml schema."""

    def test_generated_file_exists(self, sbom_generated_path: Path):
        """Test that sbom_generated.yaml exists."""
        assert sbom_generated_path.exists(), "sbom_generated.yaml not found"

    def test_generated_is_valid_yaml(self, sbom_generated_data: dict):
        """Test that sbom_generated.yaml is valid YAML."""
        assert isinstance(sbom_generated_data, dict), "sbom_generated.yaml must be a dictionary"

    def test_generated_validates_against_schema(self, sbom_generated_data: dict):
        """Test that sbom_generated.yaml validates against Pydantic schema."""
        sbom = SBOMGenerated.model_validate(sbom_generated_data)
        assert sbom is not None

    def test_generated_components_can_be_empty(self, sbom_generated_data: dict):
        """Test that generated components can be empty (no dependencies)."""
        sbom = SBOMGenerated.model_validate(sbom_generated_data)
        # Should not raise error even if empty
        assert isinstance(sbom.components, list)

    def test_component_names_are_unique(self, sbom_generated_data: dict):
        """Test that component names are unique."""
        sbom = SBOMGenerated.model_validate(sbom_generated_data)
        if sbom.components:  # Only check if not empty
            names = [comp.name for comp in sbom.components]
            assert len(names) == len(set(names)), "Component names must be unique"

    def test_all_components_have_versions(self, sbom_generated_data: dict):
        """Test that all components have versions."""
        sbom = SBOMGenerated.model_validate(sbom_generated_data)
        for component in sbom.components:
            assert component.version
            assert component.version.lower() not in ("unknown", "unspecified", "")


# Cross-validation tests
class TestSBOMCrossValidation:
    """Cross-validation tests between manual and generated SBOMs."""

    def test_combined_validation(
        self,
        sbom_manual_data: dict,
        sbom_generated_data: dict
    ):
        """Test combined validation of both SBOMs."""
        combined = CombinedSBOM(
            manual=SBOMManual.model_validate(sbom_manual_data),
            generated=SBOMGenerated.model_validate(sbom_generated_data)
        )
        assert combined is not None

    def test_no_duplicate_components_across_files(
        self,
        sbom_manual_data: dict,
        sbom_generated_data: dict
    ):
        """Test that components don't appear in both manual and generated (warning)."""
        manual = SBOMManual.model_validate(sbom_manual_data)
        generated = SBOMGenerated.model_validate(sbom_generated_data)
        
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

    def test_sbom_has_components(
        self,
        sbom_manual_data: dict,
        sbom_generated_data: dict
    ):
        """Test that SBOM has at least some components defined."""
        manual = SBOMManual.model_validate(sbom_manual_data)
        generated = SBOMGenerated.model_validate(sbom_generated_data)
        
        total_components = len(manual.components) + len(generated.components)
        assert total_components > 0, "SBOM should have at least one component"

    def test_python_packages_only_in_generated(
        self,
        sbom_manual_data: dict,
        sbom_generated_data: dict
    ):
        """Test that Python packages are only in generated SBOM (recommendation)."""
        manual = SBOMManual.model_validate(sbom_manual_data)
        
        python_packages = [
            comp.name for comp in manual.components 
            if comp.type == "Python Package"
        ]
        
        if python_packages:
            import warnings
            warnings.warn(
                f"Python packages found in manual SBOM: {python_packages}. "
                "These should be auto-generated.",
                UserWarning
            )
