"""
Pydantic schemas for YAML validation.

Schemas for:
- Risk assessment (risk_model.yaml, risks.yaml)
- SBOM (sbom.yaml)
"""

from __future__ import annotations

from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

Phase = Literal["all", "commissioning", "operation", "maintenance", "decommissioning"]
EdgeCloud = Literal["edge", "cloud", "both"]
Impact = Literal["intolerable", "undesirable", "tolerable", "acceptable", "unscored"]
Likelihood = Literal["frequent", "probable", "possible", "improbable", "unscored"]
# Risk-treatment decision per IEC 62443-3-2 ZCR 5.7 / 5.11.
Treatment = Literal["undecided", "accept", "transfer", "mitigate"]
# IEC 62443-3-3 foundational requirements (FRs); defined as data in risk_model.yaml's risk_categories.
FoundationalRequirement = Literal["iac", "uc", "si", "dc", "rdf", "tre", "ra"]


# --- Risk model (risk_model.yaml) ---------------------------------------------


class ImpactLevelDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    value: int = Field(ge=0, le=4, description="Impact/consequence value, 0 (unscored) to 4")
    color: str = Field(pattern=r"^#[0-9A-Fa-f]{6}$")


class LikelihoodLevelDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    value: int = Field(ge=0, le=4, description="Likelihood value, 0 (unscored) to 4")


class RiskLevelDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    threshold: int = Field(ge=0, description="Minimum impact x likelihood score for this band")
    description: str
    color: str = Field(pattern=r"^#[0-9A-Fa-f]{6}$")
    action: str


class RiskCategoryDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    description: str


class RiskModel(BaseModel):
    """Risk assessment scoring model (risk_model.yaml): a 4-level impact x likelihood
    matrix, the resulting risk bands, and the IEC 62443-3-3 foundational-requirement
    categories a risk can be tagged with.
    """

    model_config = ConfigDict(extra="forbid")

    impact_levels: dict[str, ImpactLevelDefinition]
    likelihood_levels: dict[str, LikelihoodLevelDefinition]
    risk_levels: dict[str, RiskLevelDefinition]
    risk_categories: list[RiskCategoryDefinition]


# --- Risk register (risks.yaml) -----------------------------------------------


class AdditionalControl(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task: str
    description: str = ""
    owner: str
    due_date: date


class RiskMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    product_name: str
    version: str = Field(pattern=r"^\d+\.\d+\.\d+$")
    assessment_date: date
    assessors: str
    review_date: date | None = None
    reviewer: str
    scope: str

    @model_validator(mode="after")
    def _review_after_assessment(self) -> RiskMetadata:
        if self.review_date is not None and self.review_date <= self.assessment_date:
            raise ValueError("review_date must be after assessment_date")
        return self


class Risk(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=r"^R\d{3,}$")
    title: str
    category: list[FoundationalRequirement] = Field(default_factory=list)
    zone_edge_cloud: EdgeCloud
    conduit_or_exposure_area: str
    phases: list[Phase] = Field(min_length=1)
    iec_62443_3_3_requirement_inspiration: str = ""
    vulnerability: str = ""
    threat: str
    consequence: str
    impact: Impact
    likelihood: Likelihood
    treatment: Treatment = "undecided"
    existing_controls: list[str] = Field(default_factory=list)
    impact_residual: Impact | None = None
    likelihood_residual: Likelihood | None = None
    additional_controls: list[AdditionalControl] = Field(default_factory=list)
    notes: str = ""

    @model_validator(mode="after")
    def _residual_pairing(self) -> Risk:
        if (self.impact_residual is None) != (self.likelihood_residual is None):
            raise ValueError("impact_residual and likelihood_residual must both be set or both omitted")
        return self


class RiskRegister(BaseModel):
    """Risk register (risks.yaml)."""

    model_config = ConfigDict(extra="forbid")

    metadata: RiskMetadata
    risks: list[Risk]

    @model_validator(mode="after")
    def _unique_risk_ids(self) -> RiskRegister:
        ids = [risk.id for risk in self.risks]
        if len(ids) != len(set(ids)):
            raise ValueError("risk IDs must be unique")
        return self


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
