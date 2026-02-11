# Risk Assessment

This folder contains the cybersecurity risk assessment for CRA (Cyber Resilience Act) compliance.

## Files

- `risk-assessment.typ` - Typst template for the risk assessment document
- `model.yaml` - Risk assessment model (severity/probability scales, risk levels, categories)
- `risks.yaml` - Risk register with all identified risks and controls
- `risk-assessment.pdf` - Generated PDF output (not committed to git)

## Building

Build the risk assessment document:

```bash
# Using the Python wrapper (recommended)
python3 main.py --risk

# Watch mode - auto-rebuild on changes
python3 main.py --risk --watch

# Direct Typst compilation
typst compile risk-assessment/risk-assessment.typ risk-assessment/risk-assessment.pdf
```

## Structure

### Model (model.yaml)

Defines the risk assessment framework:
- **Severity levels**: catastrophic, critical, moderate, minor, negligible
- **Probability levels**: almost_certain, likely, possible, unlikely, rare
- **Risk levels**: critical, high, medium, low, very_low
- **Risk categories**: Data security, access control, network security, etc.

### Risk Register (risks.yaml)

Contains all identified risks with:
- Risk identification (ID, category, title, description)
- Threat sources and vulnerabilities
- Initial risk rating (impact × probability)
- Existing controls
- Residual risk rating
- Additional controls (with responsible party, deadline, status)
- CRA requirement mapping

## Adding New Risks

Edit `risks.yaml` and add a new entry:

```yaml
- id: "R0XX"
  category: "data_security"  # Use category ID from model.yaml
  title: "Risk title"
  description: "Detailed risk description"
  threat_source: "Who/what causes this risk"
  vulnerability: "What makes system vulnerable"
  impact: "critical"  # catastrophic, critical, moderate, minor, negligible
  probability: "possible"  # almost_certain, likely, possible, unlikely, rare
  existing_controls:
    - "Control 1"
    - "Control 2"
  residual_risk_impact: "minor"
  residual_risk_probability: "unlikely"
  additional_controls:
    - control: "What needs to be done"
      responsible: "Who is responsible"
      deadline: "YYYY-MM-DD"
      status: "planned"  # planned, in_progress, completed, ongoing
  cra_requirement: "Article XX - Description"
```

## Updating Risk Status

1. Edit `risks.yaml`
2. Update control status: `planned` → `in_progress` → `completed`
3. Adjust residual risk levels as controls are implemented
4. Rebuild document: `python3 main.py --risk`

## CRA Compliance

This risk assessment addresses CRA requirements including:
- Article 13: Cybersecurity requirements (secure by design)
- Article 14: Vulnerability handling and incident response
- Annex I: Essential cybersecurity requirements

Each risk is mapped to specific CRA articles to demonstrate compliance coverage.
