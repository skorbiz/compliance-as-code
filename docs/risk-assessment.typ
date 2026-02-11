#set page(paper: "a4", margin: 2cm, numbering: "1")
#set text(size: 10pt)
#set heading(numbering: "1.1")

// Load risk data from YAML
#let model = yaml("/data/model.yaml")
#let risk_data = yaml("/data/risks.yaml")
#let metadata = risk_data.metadata

// Calculate risk score
#let calc_risk(severity, probability) = {
  let sev_val = model.severity_levels.at(severity).value
  let prob_val = model.probability_levels.at(probability).value
  sev_val * prob_val
}

// Title page
#align(center)[
  #v(3cm)
  #text(size: 24pt, weight: "bold")[Cyber Security Risk Assessment]
  #v(1em)
  #text(size: 16pt)[#metadata.product_name]
  #v(0.5em)
  #text(size: 14pt)[Version #metadata.version]
  #v(3em)
  #text(size: 12pt)[Cyber Resilience Act (CRA) Compliance]
  #v(3em)
  
  #table(
    columns: (auto, 1fr),
    stroke: none,
    [*Assessment Date:*], [#metadata.assessment_date],
    [*Assessor:*], [#metadata.assessor],
    [*Next Review:*], [#metadata.review_date],
  )
]

#pagebreak()
#outline(title: [Contents], indent: auto)
#pagebreak()

= Executive Summary

This document presents a cybersecurity risk assessment for #metadata.product_name in accordance with the EU Cyber Resilience Act (CRA).

*Total Risks Identified:* #risk_data.risks.len()

#pagebreak()

= Risk Assessment Methodology

Risk Score = Severity × Probability (scale 1-5 each, max score 25)

== Severity Levels

#table(
  columns: (auto, auto, 1fr),
  stroke: 0.5pt,
  [*Level*], [*Value*], [*Description*],
  ..model.severity_levels.pairs().map(((k, v)) => ([#k], [#v.value], [#v.description])).flatten()
)

== Probability Levels

#table(
  columns: (auto, auto, 1fr),
  stroke: 0.5pt,
  [*Level*], [*Value*], [*Description*],
  ..model.probability_levels.pairs().map(((k, v)) => ([#k], [#v.value], [#v.description])).flatten()
)

#pagebreak()

= Risk Register

#for risk in risk_data.risks [
  == #risk.id: #risk.title
  
  *Category:* #risk.category \
  *CRA Requirement:* #risk.cra_requirement
  
  *Description:* #risk.description
  
  *Threat Source:* #risk.threat_source \
  *Vulnerability:* #risk.vulnerability
  
  === Initial Risk Assessment
  
  - *Impact:* #risk.impact
  - *Probability:* #risk.probability  
  - *Risk Score:* #calc_risk(risk.impact, risk.probability)
  
  === Existing Controls
  
  #for ctrl in risk.existing_controls [
    - #ctrl
  ]
  
  === Residual Risk
  
  - *Impact:* #risk.residual_risk_impact
  - *Probability:* #risk.residual_risk_probability
  - *Risk Score:* #calc_risk(risk.residual_risk_impact, risk.residual_risk_probability)
  
  #v(1em)
]
