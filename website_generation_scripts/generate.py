"""Generate MDX docs for the Docusaurus risk register from YAML source.

Pipeline: load YAML -> validate against Pydantic schemas -> render a standalone
doc page per risk, an index partial that ``risk-assessment.mdx`` imports and
that links to each risk's doc page, and a risk-model summary partial (the
scoring matrix, risk bands, and categories) also imported by that page.

The impact / likelihood / risk-level scale and the risk categories are data,
not code: they live in ``model/risk_model.yaml`` and are loaded at generation
time, so the generated summary partial is always in sync with it.

Run with ``uv run python website_generation_scripts/generate.py``.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from model.schemas import Risk, RiskModel, RiskRegister

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

MODEL_DIR = ROOT / "model"
RISK_MODEL_SOURCE = MODEL_DIR / "risk_model.yaml"
RISKS_SOURCE = MODEL_DIR / "risks.yaml"

WEBSITE_DOCS = ROOT / "website" / "docs"
# Partials imported by 02-product-security/risk-assessment.mdx via `import X from '../_generated/...'`.
RISKS_OUT = WEBSITE_DOCS / "_generated" / "risks"
MODEL_OUT = WEBSITE_DOCS / "_generated" / "risk-model.mdx"
# Detail pages live outside `_generated/` (Docusaurus excludes `_`-prefixed
# folders from routing) so each risk gets a real, linkable doc page.
DETAILS_OUT = WEBSITE_DOCS / "02-product-security" / "risks"

# Color emoji + Docusaurus admonition type per risk level. This is presentation
# only (risk_model.yaml has no notion of emoji/admonition); keyed by the level
# keys used in `model/risk_model.yaml`'s `risk_levels`, with a safe fallback
# for any key the model defines that isn't listed here.
RISK_LEVEL_STYLES = {
    "high": ("🔴", "danger"),
    "serious": ("🟠", "warning"),
    "medium": ("🟡", "warning"),
    "low": ("🟢", "tip"),
    "unscored": ("⚪", "note"),
}
DEFAULT_RISK_LEVEL_STYLE = ("⚪", "note")


# --- Presentation filters -----------------------------------------------------
# Escaping is context-dependent, so it lives in the templates (as filters) where
# the output context — heading, table cell, or YAML frontmatter — is known.


def _mdx(text: str) -> str:
    """Escape characters that MDX would otherwise parse as JSX/expressions."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("{", "&#123;")
        .replace("}", "&#125;")
    )


def _cell(text: str) -> str:
    """Escape a value for use inside a Markdown table cell."""
    return _mdx(text).replace("|", "\\|").replace("\n", " ")


def _pretty(key: str) -> str:
    """Turn a snake_case scale/category key into a human label."""
    return key.replace("_", " ").title()


def _yaml_str(text: str) -> str:
    """Double-quote a string for safe use as a YAML frontmatter value."""
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


FILTERS = {"mdx": _mdx, "cell": _cell, "pretty": _pretty, "yaml_str": _yaml_str}


# --- Scoring (business logic, stays in Python; the scale itself is data) ------


@dataclass(frozen=True)
class Scale:
    """The impact x likelihood scoring scale, derived once from RiskModel."""

    model: RiskModel
    levels: list[tuple[str, "RiskLevelDefinition"]]  # highest threshold first
    category_names: dict[str, str]

    @classmethod
    def from_model(cls, model: RiskModel) -> "Scale":
        levels = sorted(model.risk_levels.items(), key=lambda kv: kv[1].threshold, reverse=True)
        category_names = {category.id: category.name for category in model.risk_categories}
        return cls(model=model, levels=levels, category_names=category_names)

    def score(self, impact: str, likelihood: str) -> int:
        return self.model.impact_levels[impact].value * self.model.likelihood_levels[likelihood].value

    def level_key(self, score: int) -> str:
        for key, definition in self.levels:
            if score >= definition.threshold:
                return key
        return self.levels[-1][0]


@dataclass(frozen=True)
class Assessment:
    """A computed risk rating (initial or residual) for one risk."""

    score: int
    level_key: str
    level: str  # pretty label
    emoji: str
    admonition: str
    impact: str  # display, e.g. "Intolerable (4)"
    likelihood: str  # display, e.g. "Frequent (4)"
    impact_value: int
    likelihood_value: int


def _assess(scale: Scale, impact: str, likelihood: str) -> Assessment:
    impact_value = scale.model.impact_levels[impact].value
    likelihood_value = scale.model.likelihood_levels[likelihood].value
    score = scale.score(impact, likelihood)
    key = scale.level_key(score)
    emoji, admonition = RISK_LEVEL_STYLES.get(key, DEFAULT_RISK_LEVEL_STYLE)
    impact_display = _pretty(impact) if impact == "unscored" else f"{_pretty(impact)} ({impact_value})"
    likelihood_display = (
        _pretty(likelihood) if likelihood == "unscored" else f"{_pretty(likelihood)} ({likelihood_value})"
    )
    return Assessment(
        score=score,
        level_key=key,
        level=_pretty(key),
        emoji=emoji,
        admonition=admonition,
        impact=impact_display,
        likelihood=likelihood_display,
        impact_value=impact_value,
        likelihood_value=likelihood_value,
    )


@dataclass(frozen=True)
class RiskView:
    """Everything a template needs for one risk: the raw model plus derived data.

    Text fields are escaped in the template via filters, so ``risk`` is passed
    through untouched.
    """

    risk: Risk
    doc_url: str
    category_name: str
    initial: Assessment
    residual: Assessment | None


def _view(scale: Scale, risk: Risk) -> RiskView:
    residual = None
    if risk.impact_residual is not None and risk.likelihood_residual is not None:
        residual = _assess(scale, risk.impact_residual, risk.likelihood_residual)
    category_names = [scale.category_names.get(category, _pretty(category)) for category in risk.category]
    return RiskView(
        risk=risk,
        doc_url=f"/product-security/risks/{risk.id.lower()}",
        category_name=", ".join(category_names) if category_names else "—",
        initial=_assess(scale, risk.impact, risk.likelihood),
        residual=residual,
    )


def _load_risk_model() -> RiskModel:
    with RISK_MODEL_SOURCE.open(encoding="utf-8") as handle:
        return RiskModel.model_validate(yaml.safe_load(handle))


def _load_risks() -> RiskRegister:
    with RISKS_SOURCE.open(encoding="utf-8") as handle:
        return RiskRegister.model_validate(yaml.safe_load(handle))


def _sort_key(view: RiskView) -> tuple[int, int]:
    # Highest risk first: mitigated (residual, falling back to initial when not yet
    # assessed) breaks ties by initial risk.
    mitigated_score = view.residual.score if view.residual is not None else view.initial.score
    return (-mitigated_score, -view.initial.score)


def _build_risks_context(scale: Scale, register: RiskRegister, generated_at: str) -> dict:
    views = sorted((_view(scale, risk) for risk in register.risks), key=_sort_key)
    counts = {key: 0 for key, _ in scale.levels}
    for view in views:
        counts[view.initial.level_key] += 1

    return {
        "generated_at": generated_at,
        "metadata": register.metadata,
        "distribution": [{"level": _pretty(key), "count": counts[key]} for key, _ in scale.levels],
        "risks": views,
        "total_risks": len(register.risks),
    }


# --- Risk-model summary (the scoring matrix, bands, and categories as data) --


def _levels_table(levels: dict) -> list[dict]:
    ordered = sorted(levels.items(), key=lambda kv: kv[1].value, reverse=True)
    return [{"label": _pretty(key), "value": definition.value} for key, definition in ordered]


def _matrix(scale: Scale) -> dict:
    impacts = sorted(
        ((key, definition) for key, definition in scale.model.impact_levels.items() if key != "unscored"),
        key=lambda kv: kv[1].value,
        reverse=True,
    )
    likelihoods = sorted(
        ((key, definition) for key, definition in scale.model.likelihood_levels.items() if key != "unscored"),
        key=lambda kv: kv[1].value,
        reverse=True,
    )
    rows = []
    for impact_key, impact_def in impacts:
        cells = []
        for likelihood_key, likelihood_def in likelihoods:
            score = impact_def.value * likelihood_def.value
            level_key = scale.level_key(score)
            emoji, _ = RISK_LEVEL_STYLES.get(level_key, DEFAULT_RISK_LEVEL_STYLE)
            cells.append({"score": score, "level": _pretty(level_key), "emoji": emoji})
        rows.append({"label": _pretty(impact_key), "value": impact_def.value, "cells": cells})
    return {
        "impacts": rows,
        "likelihoods": [{"label": _pretty(key), "value": definition.value} for key, definition in likelihoods],
    }


def _bands(scale: Scale) -> list[dict]:
    max_impact = max(d.value for k, d in scale.model.impact_levels.items() if k != "unscored")
    max_likelihood = max(d.value for k, d in scale.model.likelihood_levels.items() if k != "unscored")
    max_score = max_impact * max_likelihood

    scored_levels = [(key, definition) for key, definition in scale.levels if key != "unscored"]
    bands = []
    for index, (key, definition) in enumerate(scored_levels):
        upper = max_score if index == 0 else scored_levels[index - 1][1].threshold - 1
        emoji, _ = RISK_LEVEL_STYLES.get(key, DEFAULT_RISK_LEVEL_STYLE)
        bands.append(
            {
                "emoji": emoji,
                "label": _pretty(key),
                "threshold": definition.threshold,
                "upper": upper,
                "action": definition.action,
            }
        )
    return bands


def _build_model_context(scale: Scale, generated_at: str) -> dict:
    return {
        "generated_at": generated_at,
        "impact_levels": _levels_table(scale.model.impact_levels),
        "likelihood_levels": _levels_table(scale.model.likelihood_levels),
        "matrix": _matrix(scale),
        "bands": _bands(scale),
        "categories": [
            {"label": category.id.upper(), "name": category.name, "description": category.description}
            for category in scale.model.risk_categories
        ],
    }


def render() -> list[Path]:
    model = _load_risk_model()
    register = _load_risks()
    scale = Scale.from_model(model)
    generated_at = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(enabled_extensions=(), default=False),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    env.filters.update(FILTERS)

    RISKS_OUT.mkdir(parents=True, exist_ok=True)
    DETAILS_OUT.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    # Non-.mdx marker so Docusaurus (which only reads .md/.mdx) ignores it, but
    # it still flags the folder as generated for anyone browsing the repo.
    marker = DETAILS_OUT / "_generated"
    marker.write_text(
        "AUTO-GENERATED by compliance-as-code. Do not edit files in this folder by hand.\n"
        "Edit model/risks.yaml and run: uv run python website_generation_scripts/generate.py\n",
        encoding="utf-8",
    )
    written.append(marker)

    risks_context = _build_risks_context(scale, register, generated_at)

    # Remove stale detail pages for risks that were deleted or renamed since the last run.
    expected_details = {f"{view.risk.id.lower()}.mdx" for view in risks_context["risks"]}
    for existing in DETAILS_OUT.glob("*.mdx"):
        if existing.name not in expected_details:
            existing.unlink()  # Delete stale detail page

    detail_template = env.get_template("risk-detail.md.j2")
    for view in risks_context["risks"]:
        rendered = detail_template.render(generated_at=generated_at, r=view)
        output = DETAILS_OUT / f"{view.risk.id.lower()}.mdx"
        output.write_text(rendered.rstrip("\n") + "\n", encoding="utf-8")
        written.append(output)

    index_template = env.get_template("risk-index.md.j2")
    rendered = index_template.render(**risks_context)
    output = RISKS_OUT / "index.mdx"
    output.write_text(rendered.rstrip("\n") + "\n", encoding="utf-8")
    written.append(output)

    model_template = env.get_template("risk-model.md.j2")
    rendered = model_template.render(**_build_model_context(scale, generated_at))
    MODEL_OUT.parent.mkdir(parents=True, exist_ok=True)
    MODEL_OUT.write_text(rendered.rstrip("\n") + "\n", encoding="utf-8")
    written.append(MODEL_OUT)

    return written


def main() -> int:
    for path in render():
        print(f"Generated {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

