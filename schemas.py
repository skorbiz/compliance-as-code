"""
Pydantic schemas for YAML validation.

Simplified schemas for:
- Risk assessment (model.yaml, risks.yaml)
- SBOM (sbom.yaml)
"""

from datetime import date
from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


# Risk Assessment Schemas

class SeverityDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    value: int = Field(ge=1, le=5, description="Severity value 1-5")
    description: str
    color: str = Field(pattern=r"^#[0-9A-Fa-f]{6}$")


class ProbabilityDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    value: int = Field(ge=1, le=5, description="Probability value 1-5")
    description: str
    frequency: str


class RiskLevelDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    threshold: int = Field(ge=0)
    description: str
    color: str = Field(pattern=r"^#[0-9A-Fa-f]{6}$")
    action: str


class RiskCategoryDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    id: str
    name: str
    description: str


class RiskModel(BaseModel):
    """Risk assessment model (model.yaml)."""
    model_config = ConfigDict(extra="forbid")
    
    severity_levels: dict[str, SeverityDefinition]
    probability_levels: dict[str, ProbabilityDefinition]
    risk_levels: dict[str, RiskLevelDefinition]
    risk_categories: list[RiskCategoryDefinition]


class AdditionalControl(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    control: str
    responsible: str
    deadline: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$", description="Deadline in YYYY-MM-DD format")
    status: Literal["planned", "in_progress", "completed", "ongoing"]


class RiskMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    product_name: str
    version: str = Field(pattern=r"^\d+\.\d+\.\d+$")
    assessment_date: date
    assessor: str
    review_date: date
    scope: str
    
    @field_validator("review_date")
    @classmethod
    def review_after_assessment(cls, v: date, info) -> date:
        if "assessment_date" in info.data and v <= info.data["assessment_date"]:
            raise ValueError("Review date must be after assessment date")
        return v


class Risk(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    id: str = Field(pattern=r"^R\d{3,}$")
    category: str
    title: str
    description: str
    threat_source: str
    vulnerability: str
    impact: str
    probability: str
    existing_controls: list[str] = Field(default_factory=list)
    residual_risk_impact: str
    residual_risk_probability: str
    additional_controls: list[AdditionalControl] = Field(default_factory=list)
    cra_requirement: str


class RiskRegister(BaseModel):
    """Risk register (risks.yaml)."""
    model_config = ConfigDict(extra="forbid")
    
    metadata: RiskMetadata
    risks: list[Risk]


# SBOM Schemas

class SBOMComponent(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    name: str
    version: str
    type: str
    source: Optional[str] = None


class SBOMGenerated(BaseModel):
    """Generated SBOM file (sbom.yaml)."""
    model_config = ConfigDict(extra="forbid")
    
    components: list[SBOMComponent] = Field(default_factory=list)
