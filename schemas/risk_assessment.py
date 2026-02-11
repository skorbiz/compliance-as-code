"""
Pydantic schemas for risk assessment YAML files.

Defines the structure for:
- model.yaml: Risk assessment framework (severity, probability, risk levels)
- risks.yaml: Risk register with all identified risks
"""

from datetime import date
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


# Enums for risk assessment
class SeverityLevel(str, Enum):
    """Severity levels for risk impact."""
    CATASTROPHIC = "catastrophic"
    CRITICAL = "critical"
    MODERATE = "moderate"
    MINOR = "minor"
    NEGLIGIBLE = "negligible"


class ProbabilityLevel(str, Enum):
    """Probability levels for risk occurrence."""
    ALMOST_CERTAIN = "almost_certain"
    LIKELY = "likely"
    POSSIBLE = "possible"
    UNLIKELY = "unlikely"
    RARE = "rare"


class ControlStatus(str, Enum):
    """Status of risk mitigation controls."""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ONGOING = "ongoing"


class RiskCategory(str, Enum):
    """Risk categories."""
    DATA_SECURITY = "data_security"
    ACCESS_CONTROL = "access_control"
    NETWORK_SECURITY = "network_security"
    SOFTWARE_INTEGRITY = "software_integrity"
    SUPPLY_CHAIN = "supply_chain"
    AVAILABILITY = "availability"
    COMPLIANCE = "compliance"
    INCIDENT_RESPONSE = "incident_response"


# Model.yaml schemas
class SeverityDefinition(BaseModel):
    """Definition of a severity level."""
    value: int = Field(ge=1, le=5, description="Numeric value 1-5")
    description: str = Field(min_length=10, description="Description of severity level")
    color: str = Field(pattern=r"^#[0-9A-Fa-f]{6}$", description="Hex color code")


class ProbabilityDefinition(BaseModel):
    """Definition of a probability level."""
    value: int = Field(ge=1, le=5, description="Numeric value 1-5")
    description: str = Field(min_length=10, description="Description of probability level")
    frequency: str = Field(min_length=5, description="Expected frequency of occurrence")


class RiskLevelDefinition(BaseModel):
    """Definition of a risk level."""
    threshold: int = Field(ge=0, description="Minimum risk score for this level")
    description: str = Field(min_length=10, description="Description of risk level")
    color: str = Field(pattern=r"^#[0-9A-Fa-f]{6}$", description="Hex color code")
    action: str = Field(min_length=10, description="Required action for this risk level")


class RiskCategoryDefinition(BaseModel):
    """Definition of a risk category."""
    id: RiskCategory = Field(description="Category identifier")
    name: str = Field(min_length=3, description="Category display name")
    description: str = Field(min_length=10, description="Category description")


class RiskModel(BaseModel):
    """Risk assessment model (model.yaml)."""
    severity_levels: dict[SeverityLevel, SeverityDefinition] = Field(
        description="Severity level definitions"
    )
    probability_levels: dict[ProbabilityLevel, ProbabilityDefinition] = Field(
        description="Probability level definitions"
    )
    risk_levels: dict[str, RiskLevelDefinition] = Field(
        description="Risk level classifications"
    )
    risk_categories: list[RiskCategoryDefinition] = Field(
        min_length=1,
        description="Risk categories"
    )

    @field_validator("severity_levels")
    @classmethod
    def validate_severity_values(cls, v: dict[SeverityLevel, SeverityDefinition]) -> dict:
        """Ensure severity values are 1-5 and unique."""
        if len(v) != 5:
            raise ValueError("Must have exactly 5 severity levels")
        
        values = [level.value for level in v.values()]
        if sorted(values) != [1, 2, 3, 4, 5]:
            raise ValueError("Severity values must be exactly 1, 2, 3, 4, 5")
        
        return v

    @field_validator("probability_levels")
    @classmethod
    def validate_probability_values(cls, v: dict[ProbabilityLevel, ProbabilityDefinition]) -> dict:
        """Ensure probability values are 1-5 and unique."""
        if len(v) != 5:
            raise ValueError("Must have exactly 5 probability levels")
        
        values = [level.value for level in v.values()]
        if sorted(values) != [1, 2, 3, 4, 5]:
            raise ValueError("Probability values must be exactly 1, 2, 3, 4, 5")
        
        return v

    @field_validator("risk_categories")
    @classmethod
    def validate_unique_category_ids(cls, v: list[RiskCategoryDefinition]) -> list:
        """Ensure category IDs are unique."""
        ids = [cat.id for cat in v]
        if len(ids) != len(set(ids)):
            raise ValueError("Category IDs must be unique")
        return v


# Risks.yaml schemas
class AdditionalControl(BaseModel):
    """Additional control to mitigate a risk."""
    control: str = Field(min_length=10, description="Control description")
    responsible: str = Field(min_length=2, description="Responsible party")
    deadline: str = Field(description="Deadline (YYYY-MM-DD or description)")
    status: ControlStatus = Field(description="Control implementation status")

    @field_validator("deadline")
    @classmethod
    def validate_deadline_format(cls, v: str) -> str:
        """Validate deadline is either a date or descriptive text."""
        # Try to parse as date
        if v.lower() in ("ongoing", "quarterly", "monthly", "annually"):
            return v
        
        try:
            date.fromisoformat(v)
        except ValueError:
            # If not a valid date, ensure it's at least descriptive
            if len(v) < 5:
                raise ValueError("Deadline must be a valid date (YYYY-MM-DD) or descriptive text")
        
        return v


class RiskMetadata(BaseModel):
    """Metadata for the risk register."""
    product_name: str = Field(min_length=3, description="Product name")
    version: str = Field(pattern=r"^\d+\.\d+\.\d+$", description="Version number (semver)")
    assessment_date: date = Field(description="Date of assessment")
    assessor: str = Field(min_length=3, description="Person/team who performed assessment")
    review_date: date = Field(description="Next review date")
    scope: str = Field(min_length=10, description="Scope of assessment")

    @model_validator(mode="after")
    def validate_review_after_assessment(self) -> "RiskMetadata":
        """Ensure review date is after assessment date."""
        if self.review_date <= self.assessment_date:
            raise ValueError("Review date must be after assessment date")
        return self


class Risk(BaseModel):
    """Individual risk entry."""
    id: str = Field(pattern=r"^R\d{3}$", description="Risk ID (e.g., R001)")
    category: RiskCategory = Field(description="Risk category")
    title: str = Field(min_length=10, description="Risk title")
    description: str = Field(min_length=20, description="Detailed risk description")
    threat_source: str = Field(min_length=10, description="Source of the threat")
    vulnerability: str = Field(min_length=10, description="Vulnerability being exploited")
    
    # Initial risk assessment
    impact: SeverityLevel = Field(description="Initial impact severity")
    probability: ProbabilityLevel = Field(description="Initial probability")
    
    existing_controls: list[str] = Field(
        min_length=0,
        description="Existing controls in place"
    )
    
    # Residual risk assessment
    residual_risk_impact: SeverityLevel = Field(description="Residual impact after controls")
    residual_risk_probability: ProbabilityLevel = Field(description="Residual probability after controls")
    
    additional_controls: list[AdditionalControl] = Field(
        default_factory=list,
        description="Additional controls to implement"
    )
    
    cra_requirement: str = Field(
        min_length=10,
        description="Relevant CRA requirement"
    )

    @field_validator("cra_requirement")
    @classmethod
    def validate_cra_format(cls, v: str) -> str:
        """Validate CRA requirement format."""
        if not v.lower().startswith("article"):
            raise ValueError("CRA requirement should start with 'Article'")
        return v


class RiskRegister(BaseModel):
    """Complete risk register (risks.yaml)."""
    metadata: RiskMetadata = Field(description="Assessment metadata")
    risks: list[Risk] = Field(min_length=1, description="List of identified risks")

    @field_validator("risks")
    @classmethod
    def validate_unique_risk_ids(cls, v: list[Risk]) -> list[Risk]:
        """Ensure risk IDs are unique."""
        ids = [risk.id for risk in v]
        if len(ids) != len(set(ids)):
            duplicates = [id for id in ids if ids.count(id) > 1]
            raise ValueError(f"Risk IDs must be unique. Duplicates: {set(duplicates)}")
        return v

    @field_validator("risks")
    @classmethod
    def validate_risk_ids_sequential(cls, v: list[Risk]) -> list[Risk]:
        """Warn if risk IDs are not sequential (informational only)."""
        ids = sorted([int(risk.id[1:]) for risk in v])
        expected = list(range(1, len(ids) + 1))
        if ids != expected:
            # This is just a warning, not an error
            import warnings
            warnings.warn(
                f"Risk IDs are not sequential. Found: {ids}, Expected: {expected}",
                UserWarning
            )
        return v

    @model_validator(mode="after")
    def validate_categories_exist(self) -> "RiskRegister":
        """Ensure all risk categories are valid."""
        # All categories are validated by the RiskCategory enum
        # This validator could be extended to cross-check with model.yaml
        return self
