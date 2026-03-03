#!/usr/bin/env python3
"""
Generate Docusaurus markdown pages from YAML source-of-truth files.
"""

from __future__ import annotations

from datetime import datetime, timezone
from html import escape
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from model.schemas import RiskModel, RiskRegister


MODEL_SOURCE = ROOT / "model/risk_model.yaml"
RISKS_SOURCE = ROOT / "model/risks.yaml"
OUTPUT = ROOT / "website/docs/generated/risk-model.md"


def _escape_cell(value: str) -> str:
    # MDX parses raw "<...>" as JSX, so escape HTML-sensitive characters.
    return escape(value, quote=False).replace("|", "\\|").replace("\n", " ")


def _read_data() -> tuple[RiskModel, RiskRegister]:
    with MODEL_SOURCE.open(encoding="utf-8") as f:
        model_data = yaml.safe_load(f)
    with RISKS_SOURCE.open(encoding="utf-8") as f:
        risks_data = yaml.safe_load(f)
    return (
        RiskModel.model_validate(model_data),
        RiskRegister.model_validate(risks_data),
    )


def _risk_score(model: RiskModel, severity: str, probability: str) -> int:
    sev = model.severity_levels[severity].value
    prob = model.probability_levels[probability].value
    return sev * prob


def _risk_level(model: RiskModel, score: int) -> str:
    levels = sorted(
        model.risk_levels.items(),
        key=lambda item: item[1].threshold,
        reverse=True,
    )
    for key, definition in levels:
        if score >= definition.threshold:
            return key
    return levels[-1][0]


def _pretty(name: str) -> str:
    return name.replace("_", " ").title()


def _render(model: RiskModel, register: RiskRegister) -> str:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    category_names = {category.id: category.name for category in model.risk_categories}
    levels_by_threshold = sorted(
        model.risk_levels.items(),
        key=lambda item: item[1].threshold,
        reverse=True,
    )

    risk_counts = {key: 0 for key, _ in levels_by_threshold}
    risk_rows: list[str] = []

    for risk in register.risks:
        initial_score = _risk_score(model, risk.impact, risk.probability)
        initial_level = _risk_level(model, initial_score)
        residual_score = _risk_score(
            model, risk.residual_risk_impact, risk.residual_risk_probability
        )
        residual_level = _risk_level(model, residual_score)
        risk_counts[initial_level] = risk_counts.get(initial_level, 0) + 1

        risk_rows.append(
            "| "
            f"`{risk.id}` | "
            f"{_escape_cell(category_names.get(risk.category, risk.category))} | "
            f"{_escape_cell(risk.title)} | "
            f"{initial_score} ({_pretty(initial_level)}) | "
            f"{residual_score} ({_pretty(residual_level)})"
            " |"
        )

    lines = [
        "---",
        "title: Risk Model (Generated)",
        "description: Generated from model/risk_model.yaml and model/risks.yaml",
        "---",
        "",
        "# Risk Model (Generated)",
        "",
        "This page is generated from YAML files and should not be edited directly.",
        "",
        "## Source Files",
        "",
        "- `model/risk_model.yaml`",
        "- `model/risks.yaml`",
        f"- Generated at: `{generated_at}`",
        "",
        "## Metadata",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Product | {_escape_cell(register.metadata.product_name)} |",
        f"| Version | `{register.metadata.version}` |",
        f"| Assessment Date | `{register.metadata.assessment_date.isoformat()}` |",
        f"| Review Date | `{register.metadata.review_date.isoformat()}` |",
        f"| Assessor | {_escape_cell(register.metadata.assessor)} |",
        "",
        "## Severity Levels",
        "",
        "| Key | Value | Description |",
        "| --- | --- | --- |",
    ]

    for key, severity in model.severity_levels.items():
        lines.append(
            f"| `{key}` | {severity.value} | {_escape_cell(severity.description)} |"
        )

    lines.extend(
        [
            "",
            "## Probability Levels",
            "",
            "| Key | Value | Description | Frequency |",
            "| --- | --- | --- | --- |",
        ]
    )

    for key, probability in model.probability_levels.items():
        lines.append(
            "| "
            f"`{key}` | "
            f"{probability.value} | "
            f"{_escape_cell(probability.description)} | "
            f"{_escape_cell(probability.frequency)}"
            " |"
        )

    lines.extend(
        [
            "",
            "## Risk Level Thresholds",
            "",
            "| Level | Threshold | Action |",
            "| --- | --- | --- |",
        ]
    )

    for key, level in levels_by_threshold:
        lines.append(
            "| "
            f"{_pretty(key)} | "
            f"{level.threshold} | "
            f"{_escape_cell(level.action)}"
            " |"
        )

    lines.extend(
        [
            "",
            "## Initial Risk Distribution",
            "",
            "| Level | Count |",
            "| --- | --- |",
        ]
    )

    for key, _ in levels_by_threshold:
        lines.append(f"| {_pretty(key)} | {risk_counts.get(key, 0)} |")

    lines.extend(
        [
            "",
            "## Risk Register Summary",
            "",
            "| Risk ID | Category | Title | Initial Risk | Residual Risk |",
            "| --- | --- | --- | --- | --- |",
            *risk_rows,
            "",
            f"Total risks: **{len(register.risks)}**",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> int:
    model, register = _read_data()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(_render(model, register), encoding="utf-8")
    print(f"Generated {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
