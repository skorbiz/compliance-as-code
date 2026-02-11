"""
Simple tests to verify YAML files validate against schemas.
"""

from pathlib import Path
import pytest
import yaml

from schemas import RiskModel, RiskRegister, SBOMGenerated


class TestYAMLValidation:
    """Test that all YAML files validate against their schemas."""

    def test_risk_model_validates(self):
        with open("data/model.yaml") as f:
            data = yaml.safe_load(f)
        model = RiskModel.model_validate(data)
        assert len(model.severity_levels) > 0
        assert len(model.probability_levels) > 0

    def test_risk_register_validates(self):
        with open("data/risks.yaml") as f:
            data = yaml.safe_load(f)
        register = RiskRegister.model_validate(data)
        assert len(register.risks) > 0

    def test_sbom_validates(self):
        with open("data/sbom.yaml") as f:
            data = yaml.safe_load(f)
        sbom = SBOMGenerated.model_validate(data)
        assert isinstance(sbom.components, list)

    def test_risk_categories_exist_in_model(self):
        """Verify risks reference categories defined in the model."""
        with open("data/model.yaml") as f:
            model_data = yaml.safe_load(f)
        with open("data/risks.yaml") as f:
            risk_data = yaml.safe_load(f)
        
        model = RiskModel.model_validate(model_data)
        register = RiskRegister.model_validate(risk_data)
        
        valid_categories = {cat.id for cat in model.risk_categories}
        for risk in register.risks:
            assert risk.category in valid_categories, f"{risk.id} has invalid category"
