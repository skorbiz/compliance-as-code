"""
Pydantic schemas for YAML validation.

Simplified schemas for:
- Risk assessment (model.yaml, risks.yaml)
- SBOM (sbom.yaml)
"""

from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


# Risk Assessment Schemas

class SeverityDefinition(BaseModel):
    value: int = Field(ge=1, le=5)
    description: str
    color: str


class ProbabilityDefinition(BaseModel):
    value: int = Field(ge=1, le=5)
    description: str
    frequency: str


class RiskLevelDefinition(BaseModel):
    threshold: int = Field(ge=0)
    description: str
    color: str
    action: str


class RiskCategoryDefinition(BaseModel):
    id: str
    name: str
    description: str


class RiskModel(BaseModel):
    """Risk assessment model (model.yaml)."""
    severity_levels: dict[str, SeverityDefinition]
    probability_levels: dict[str, ProbabilityDefinition]
    risk_levels: dict[str, RiskLevelDefinition]
    risk_categories: list[RiskCategoryDefinition]


class AdditionalControl(BaseModel):
    control: str
    responsible: str
    deadline: str
    status: str


class RiskMetadata(BaseModel):
    product_name: str
    version: str
    assessment_date: date
    assessor: str
    review_date: date
    scope: str


class Risk(BaseModel):
    id: str
    category: str
    title: str
    description: str
    threat_source: str
    vulnerability: str
    impact: str
    probability: str
    existing_controls: list[str] = []
    residual_risk_impact: str
    residual_risk_probability: str
    additional_controls: list[AdditionalControl] = []
    cra_requirement: str


class RiskRegister(BaseModel):
    """Risk register (risks.yaml)."""
    metadata: RiskMetadata
    risks: list[Risk]


# SBOM Schemas

class SBOMComponent(BaseModel):
    name: str
    version: str
    type: str
    source: Optional[str] = None


class SBOMGenerated(BaseModel):
    """Generated SBOM file (sbom.yaml)."""
    components: list[SBOMComponent] = []
