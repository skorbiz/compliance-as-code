---
title: Risk Model (Generated)
description: Generated from model/risk_model.yaml and model/risks.yaml
---

# Risk Model (Generated)

This page is generated from YAML files and should not be edited directly.

## Source Files

- `model/risk_model.yaml`
- `model/risks.yaml`
- Generated at: `2026-03-03 07:59 UTC`

## Metadata

| Field | Value |
| --- | --- |
| Product | Example Product |
| Version | `1.0.0` |
| Assessment Date | `2026-02-11` |
| Review Date | `2026-08-11` |
| Assessor | Security Team |

## Severity Levels

| Key | Value | Description |
| --- | --- | --- |
| `catastrophic` | 5 | Complete system failure or major data breach |
| `critical` | 4 | Major disruption or significant data exposure |
| `moderate` | 3 | Partial disruption or limited data exposure |
| `minor` | 2 | Minor disruption with minimal impact |
| `negligible` | 1 | Insignificant impact |

## Probability Levels

| Key | Value | Description | Frequency |
| --- | --- | --- | --- |
| `almost_certain` | 5 | Expected to occur (&gt;90%) | Multiple times per year |
| `likely` | 4 | Will probably occur (60-90%) | Once per year |
| `possible` | 3 | Might occur (30-60%) | Once every 1-3 years |
| `unlikely` | 2 | Could occur (10-30%) | Once every 3-10 years |
| `rare` | 1 | Exceptional circumstances (&lt;10%) | Less than once in 10 years |

## Risk Level Thresholds

| Level | Threshold | Action |
| --- | --- | --- |
| Critical | 15 | Implement controls immediately |
| High | 10 | Implement controls within 30 days |
| Medium | 6 | Implement controls within 90 days |
| Low | 3 | Review annually |
| Very Low | 0 | Routine monitoring |

## Initial Risk Distribution

| Level | Count |
| --- | --- |
| Critical | 1 |
| High | 2 |
| Medium | 0 |
| Low | 0 |
| Very Low | 0 |

## Risk Register Summary

| Risk ID | Category | Title | Initial Risk | Residual Risk |
| --- | --- | --- | --- | --- |
| `R001` | Data Security | Unauthorized access to user data | 12 (High) | 6 (Medium) |
| `R002` | Access Control | Brute force attack on authentication | 16 (Critical) | 9 (Medium) |
| `R003` | Software Integrity | Malicious software update | 10 (High) | 4 (Low) |

Total risks: **3**
