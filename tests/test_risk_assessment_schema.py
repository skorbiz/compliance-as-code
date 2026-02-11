"""
Tests for risk assessment YAML schema validation.

Validates:
- risk-assessment/model.yaml
- risk-assessment/risks.yaml
"""

from pathlib import Path

import pytest
import yaml

from schemas.risk_assessment import (
    AdditionalControl,
    ControlStatus,
    ProbabilityLevel,
    Risk,
    RiskCategory,
    RiskModel,
    RiskRegister,
    SeverityLevel,
)


# Fixtures
@pytest.fixture
def risk_model_path() -> Path:
    """Path to risk model YAML file."""
    return Path("risk-assessment/model.yaml")


@pytest.fixture
def risk_register_path() -> Path:
    """Path to risk register YAML file."""
    return Path("risk-assessment/risks.yaml")


@pytest.fixture
def risk_model_data(risk_model_path: Path) -> dict:
    """Load risk model YAML data."""
    with open(risk_model_path) as f:
        return yaml.safe_load(f)


@pytest.fixture
def risk_register_data(risk_register_path: Path) -> dict:
    """Load risk register YAML data."""
    with open(risk_register_path) as f:
        return yaml.safe_load(f)


# Model.yaml tests
class TestRiskModel:
    """Tests for risk-assessment/model.yaml schema."""

    def test_model_file_exists(self, risk_model_path: Path):
        """Test that model.yaml exists."""
        assert risk_model_path.exists(), "risk-assessment/model.yaml not found"

    def test_model_is_valid_yaml(self, risk_model_data: dict):
        """Test that model.yaml is valid YAML."""
        assert isinstance(risk_model_data, dict), "model.yaml must be a dictionary"

    def test_model_validates_against_schema(self, risk_model_data: dict):
        """Test that model.yaml validates against Pydantic schema."""
        model = RiskModel.model_validate(risk_model_data)
        assert model is not None

    def test_model_has_five_severity_levels(self, risk_model_data: dict):
        """Test that exactly 5 severity levels are defined."""
        model = RiskModel.model_validate(risk_model_data)
        assert len(model.severity_levels) == 5

    def test_model_has_five_probability_levels(self, risk_model_data: dict):
        """Test that exactly 5 probability levels are defined."""
        model = RiskModel.model_validate(risk_model_data)
        assert len(model.probability_levels) == 5

    def test_severity_values_are_1_to_5(self, risk_model_data: dict):
        """Test that severity values are exactly 1, 2, 3, 4, 5."""
        model = RiskModel.model_validate(risk_model_data)
        values = sorted([level.value for level in model.severity_levels.values()])
        assert values == [1, 2, 3, 4, 5]

    def test_probability_values_are_1_to_5(self, risk_model_data: dict):
        """Test that probability values are exactly 1, 2, 3, 4, 5."""
        model = RiskModel.model_validate(risk_model_data)
        values = sorted([level.value for level in model.probability_levels.values()])
        assert values == [1, 2, 3, 4, 5]

    def test_all_severity_levels_have_colors(self, risk_model_data: dict):
        """Test that all severity levels have valid hex colors."""
        model = RiskModel.model_validate(risk_model_data)
        for level in model.severity_levels.values():
            assert level.color.startswith("#")
            assert len(level.color) == 7

    def test_risk_categories_are_unique(self, risk_model_data: dict):
        """Test that risk category IDs are unique."""
        model = RiskModel.model_validate(risk_model_data)
        ids = [cat.id for cat in model.risk_categories]
        assert len(ids) == len(set(ids)), "Risk category IDs must be unique"

    def test_risk_categories_have_valid_ids(self, risk_model_data: dict):
        """Test that all risk categories have valid IDs."""
        model = RiskModel.model_validate(risk_model_data)
        for category in model.risk_categories:
            assert category.id in RiskCategory


# Risks.yaml tests
class TestRiskRegister:
    """Tests for risk-assessment/risks.yaml schema."""

    def test_risks_file_exists(self, risk_register_path: Path):
        """Test that risks.yaml exists."""
        assert risk_register_path.exists(), "risk-assessment/risks.yaml not found"

    def test_risks_is_valid_yaml(self, risk_register_data: dict):
        """Test that risks.yaml is valid YAML."""
        assert isinstance(risk_register_data, dict), "risks.yaml must be a dictionary"

    def test_risks_validates_against_schema(self, risk_register_data: dict):
        """Test that risks.yaml validates against Pydantic schema."""
        register = RiskRegister.model_validate(risk_register_data)
        assert register is not None

    def test_metadata_has_valid_version(self, risk_register_data: dict):
        """Test that metadata has valid semver version."""
        register = RiskRegister.model_validate(risk_register_data)
        assert register.metadata.version.count(".") == 2

    def test_review_date_is_after_assessment_date(self, risk_register_data: dict):
        """Test that review date is after assessment date."""
        register = RiskRegister.model_validate(risk_register_data)
        assert register.metadata.review_date > register.metadata.assessment_date

    def test_all_risk_ids_are_unique(self, risk_register_data: dict):
        """Test that all risk IDs are unique."""
        register = RiskRegister.model_validate(risk_register_data)
        ids = [risk.id for risk in register.risks]
        assert len(ids) == len(set(ids)), f"Duplicate risk IDs found"

    def test_all_risk_ids_follow_format(self, risk_register_data: dict):
        """Test that all risk IDs follow R### format."""
        register = RiskRegister.model_validate(risk_register_data)
        for risk in register.risks:
            assert risk.id.startswith("R")
            assert len(risk.id) == 4
            assert risk.id[1:].isdigit()

    def test_all_risks_have_categories(self, risk_register_data: dict):
        """Test that all risks have valid categories."""
        register = RiskRegister.model_validate(risk_register_data)
        for risk in register.risks:
            assert risk.category in RiskCategory

    def test_all_risks_have_cra_requirements(self, risk_register_data: dict):
        """Test that all risks have CRA requirements."""
        register = RiskRegister.model_validate(risk_register_data)
        for risk in register.risks:
            assert risk.cra_requirement.lower().startswith("article")

    def test_all_additional_controls_have_valid_status(self, risk_register_data: dict):
        """Test that all additional controls have valid status."""
        register = RiskRegister.model_validate(risk_register_data)
        for risk in register.risks:
            for control in risk.additional_controls:
                assert control.status in ControlStatus

    def test_residual_risk_not_higher_than_initial(self, risk_register_data: dict):
        """Test that residual risk is not higher than initial risk (warning only)."""
        register = RiskRegister.model_validate(risk_register_data)
        
        severity_values = {
            SeverityLevel.NEGLIGIBLE: 1,
            SeverityLevel.MINOR: 2,
            SeverityLevel.MODERATE: 3,
            SeverityLevel.CRITICAL: 4,
            SeverityLevel.CATASTROPHIC: 5,
        }
        
        probability_values = {
            ProbabilityLevel.RARE: 1,
            ProbabilityLevel.UNLIKELY: 2,
            ProbabilityLevel.POSSIBLE: 3,
            ProbabilityLevel.LIKELY: 4,
            ProbabilityLevel.ALMOST_CERTAIN: 5,
        }
        
        import warnings as warn_module
        
        warning_messages = []
        for risk in register.risks:
            initial_score = severity_values[risk.impact] * probability_values[risk.probability]
            residual_score = (
                severity_values[risk.residual_risk_impact] * 
                probability_values[risk.residual_risk_probability]
            )
            
            if residual_score > initial_score:
                warning_messages.append(
                    f"{risk.id}: Residual risk ({residual_score}) is higher than "
                    f"initial risk ({initial_score})"
                )
        
        if warning_messages:
            warn_module.warn("\n".join(warning_messages), UserWarning)


# Cross-validation tests
class TestRiskCrossValidation:
    """Cross-validation tests between model.yaml and risks.yaml."""

    def test_all_risk_categories_exist_in_model(
        self,
        risk_model_data: dict,
        risk_register_data: dict
    ):
        """Test that all risk categories used exist in model."""
        model = RiskModel.model_validate(risk_model_data)
        register = RiskRegister.model_validate(risk_register_data)
        
        model_categories = {cat.id for cat in model.risk_categories}
        risk_categories = {risk.category for risk in register.risks}
        
        missing = risk_categories - model_categories
        assert not missing, f"Risk categories not defined in model: {missing}"

    def test_all_severity_levels_are_used(
        self,
        risk_model_data: dict,
        risk_register_data: dict
    ):
        """Test that risks use severity levels defined in model (informational)."""
        import warnings
        
        model = RiskModel.model_validate(risk_model_data)
        register = RiskRegister.model_validate(risk_register_data)
        
        model_severities = set(model.severity_levels.keys())
        used_severities = set()
        for risk in register.risks:
            used_severities.add(risk.impact)
            used_severities.add(risk.residual_risk_impact)
        
        unused = model_severities - used_severities
        if unused:
            warnings.warn(
                f"Severity levels defined but not used: {unused}",
                UserWarning
            )

    def test_all_probability_levels_are_used(
        self,
        risk_model_data: dict,
        risk_register_data: dict
    ):
        """Test that risks use probability levels defined in model (informational)."""
        import warnings
        
        model = RiskModel.model_validate(risk_model_data)
        register = RiskRegister.model_validate(risk_register_data)
        
        model_probabilities = set(model.probability_levels.keys())
        used_probabilities = set()
        for risk in register.risks:
            used_probabilities.add(risk.probability)
            used_probabilities.add(risk.residual_risk_probability)
        
        unused = model_probabilities - used_probabilities
        if unused:
            warnings.warn(
                f"Probability levels defined but not used: {unused}",
                UserWarning
            )
