#set page(
  paper: "a4",
  margin: (x: 2cm, y: 2cm),
  numbering: "1",
)

#set text(
  size: 10pt,
)

#set heading(numbering: "1.1")

// Load risk data
#let model = yaml("model.yaml")
#let risk_data = yaml("risks.yaml")
#let metadata = risk_data.metadata

// Helper function to calculate risk score
#let calc_risk(severity, probability) = {
  let sev_val = model.severity_levels.at(severity).value
  let prob_val = model.probability_levels.at(probability).value
  sev_val * prob_val
}

// Helper function to get risk level from score
#let get_risk_level(score) = {
  if score >= 15 {
    ("critical", model.risk_levels.critical.color)
  } else if score >= 10 {
    ("high", model.risk_levels.high.color)
  } else if score >= 6 {
    ("medium", model.risk_levels.medium.color)
  } else if score >= 3 {
    ("low", model.risk_levels.low.color)
  } else {
    ("very_low", model.risk_levels.very_low.color)
  }
}

// Title page
#align(center)[
  #v(3cm)
  
  #text(size: 24pt, weight: "bold")[
    Cyber Security Risk Assessment
  ]
  
  #v(1em)
  
  #text(size: 16pt)[
    #metadata.product_name
  ]
  
  #v(0.5em)
  
  #text(size: 14pt)[
    Version #metadata.version
  ]
  
  #v(3em)
  
  #text(size: 12pt)[
    Cyber Resilience Act (CRA) Compliance
  ]
  
  #v(5em)
  
  #table(
    columns: (auto, 1fr),
    stroke: none,
    align: (right, left),
    row-gutter: 0.5em,
    
    [*Assessment Date:*], [#metadata.assessment_date],
    [*Assessor:*], [#metadata.assessor],
    [*Next Review:*], [#metadata.review_date],
    [*Scope:*], [#metadata.scope],
  )
]

#pagebreak()

#outline(
  title: [Table of Contents],
  indent: auto,
)

#pagebreak()

= Executive Summary

This document presents a comprehensive cybersecurity risk assessment for #metadata.product_name, conducted in accordance with the EU Cyber Resilience Act (CRA) requirements.

== Purpose

This risk assessment identifies, analyzes, and evaluates cybersecurity risks associated with the software product throughout its lifecycle. The assessment supports compliance with CRA Article 13 (Cybersecurity requirements) and Article 14 (Vulnerability handling).

== Scope

The assessment covers:
- Data security and privacy risks
- Access control and authentication
- Network security threats
- Software integrity and update mechanisms
- Supply chain security
- System availability and resilience
- Regulatory compliance
- Incident detection and response

== Key Findings

#let risks = risk_data.risks
#let total_risks = risks.len()

#let critical_risks = risks.filter(r => {
  let score = calc_risk(r.impact, r.probability)
  score >= 15
})

#let high_risks = risks.filter(r => {
  let score = calc_risk(r.impact, r.probability)
  score >= 10 and score < 15
})

#let residual_critical = risks.filter(r => {
  let score = calc_risk(r.residual_risk_impact, r.residual_risk_probability)
  score >= 15
})

- *Total Risks Identified:* #total_risks
- *Critical Risks (Initial):* #critical_risks.len()
- *High Risks (Initial):* #high_risks.len()
- *Critical Risks (Residual):* #residual_critical.len()

All identified risks have been assigned mitigation controls. Additional controls are planned or in progress to further reduce residual risk levels.

#pagebreak()

= Risk Assessment Methodology

== Risk Rating Matrix

Risk is calculated as: *Risk Score = Severity × Probability*

=== Severity Levels

#table(
  columns: (auto, auto, 1fr),
  stroke: 0.5pt,
  align: (center, center, left),
  
  [*Level*], [*Value*], [*Description*],
  
  [NEGLIGIBLE], [1], model.severity_levels.negligible.description,
  [MINOR], [2], model.severity_levels.minor.description,
  [MODERATE], [3], model.severity_levels.moderate.description,
  [CRITICAL], [4], model.severity_levels.critical.description,
  [CATASTROPHIC], [5], model.severity_levels.catastrophic.description,
)

=== Probability Levels

#table(
  columns: (auto, auto, 1fr, auto),
  stroke: 0.5pt,
  align: (center, center, left, left),
  
  [*Level*], [*Value*], [*Description*], [*Frequency*],
  
  [RARE], [1], model.probability_levels.rare.description, model.probability_levels.rare.frequency,
  [UNLIKELY], [2], model.probability_levels.unlikely.description, model.probability_levels.unlikely.frequency,
  [POSSIBLE], [3], model.probability_levels.possible.description, model.probability_levels.possible.frequency,
  [LIKELY], [4], model.probability_levels.likely.description, model.probability_levels.likely.frequency,
  [ALMOST CERTAIN], [5], model.probability_levels.almost_certain.description, model.probability_levels.almost_certain.frequency,
)

#pagebreak()

=== Risk Level Classification

#table(
  columns: (auto, auto, 1fr, 1fr),
  stroke: 0.5pt,
  align: (left, center, left, left),
  
  [*Risk Level*], [*Score Range*], [*Description*], [*Action Required*],
  
  [CRITICAL], [≥15], model.risk_levels.critical.description, model.risk_levels.critical.action,
  [HIGH], [10-14], model.risk_levels.high.description, model.risk_levels.high.action,
  [MEDIUM], [6-9], model.risk_levels.medium.description, model.risk_levels.medium.action,
  [LOW], [3-5], model.risk_levels.low.description, model.risk_levels.low.action,
  [VERY LOW], [#sym.lt 3], model.risk_levels.very_low.description, model.risk_levels.very_low.action,
)

#pagebreak()

= Risk Matrix

#table(
  columns: (auto, auto, auto, auto, auto, auto, auto),
  stroke: 0.5pt,
  align: center + horizon,
  inset: 8pt,
  
  // Header row
  table.cell(rowspan: 2, colspan: 2, fill: rgb("f0f0f0"))[*Risk Matrix*],
  table.cell(colspan: 5, fill: rgb("f0f0f0"))[*Severity →*],
  
  // Severity values
  table.cell(fill: rgb("f0f0f0"))[1], table.cell(fill: rgb("f0f0f0"))[2], table.cell(fill: rgb("f0f0f0"))[3], table.cell(fill: rgb("f0f0f0"))[4], table.cell(fill: rgb("f0f0f0"))[5],
  
  // Probability 5
  table.cell(rowspan: 5, fill: rgb("f0f0f0"))[#rotate(-90deg)[*Probability ↓*]],
  table.cell(fill: rgb("f0f0f0"))[5],
  table.cell(fill: rgb(model.risk_levels.medium.color))[#text(fill: white, weight: "bold")[5]],
  table.cell(fill: rgb(model.risk_levels.high.color))[#text(fill: white, weight: "bold")[10]],
  table.cell(fill: rgb(model.risk_levels.critical.color))[#text(fill: white, weight: "bold")[15]],
  table.cell(fill: rgb(model.risk_levels.critical.color))[#text(fill: white, weight: "bold")[20]],
  table.cell(fill: rgb(model.risk_levels.critical.color))[#text(fill: white, weight: "bold")[25]],
  
  // Probability 4
  table.cell(fill: rgb("f0f0f0"))[4],
  table.cell(fill: rgb(model.risk_levels.low.color))[#text(weight: "bold")[4]],
  table.cell(fill: rgb(model.risk_levels.medium.color))[#text(fill: white, weight: "bold")[8]],
  table.cell(fill: rgb(model.risk_levels.high.color))[#text(fill: white, weight: "bold")[12]],
  table.cell(fill: rgb(model.risk_levels.critical.color))[#text(fill: white, weight: "bold")[16]],
  table.cell(fill: rgb(model.risk_levels.critical.color))[#text(fill: white, weight: "bold")[20]],
  
  // Probability 3
  table.cell(fill: rgb("f0f0f0"))[3],
  table.cell(fill: rgb(model.risk_levels.low.color))[#text(weight: "bold")[3]],
  table.cell(fill: rgb(model.risk_levels.medium.color))[#text(fill: white, weight: "bold")[6]],
  table.cell(fill: rgb(model.risk_levels.medium.color))[#text(fill: white, weight: "bold")[9]],
  table.cell(fill: rgb(model.risk_levels.high.color))[#text(fill: white, weight: "bold")[12]],
  table.cell(fill: rgb(model.risk_levels.critical.color))[#text(fill: white, weight: "bold")[15]],
  
  // Probability 2
  table.cell(fill: rgb("f0f0f0"))[2],
  table.cell(fill: rgb(model.risk_levels.very_low.color))[#text(weight: "bold")[2]],
  table.cell(fill: rgb(model.risk_levels.low.color))[#text(weight: "bold")[4]],
  table.cell(fill: rgb(model.risk_levels.medium.color))[#text(fill: white, weight: "bold")[6]],
  table.cell(fill: rgb(model.risk_levels.medium.color))[#text(fill: white, weight: "bold")[8]],
  table.cell(fill: rgb(model.risk_levels.high.color))[#text(fill: white, weight: "bold")[10]],
  
  // Probability 1
  table.cell(fill: rgb("f0f0f0"))[1],
  table.cell(fill: rgb(model.risk_levels.very_low.color))[#text(weight: "bold")[1]],
  table.cell(fill: rgb(model.risk_levels.very_low.color))[#text(weight: "bold")[2]],
  table.cell(fill: rgb(model.risk_levels.low.color))[#text(weight: "bold")[3]],
  table.cell(fill: rgb(model.risk_levels.low.color))[#text(weight: "bold")[4]],
  table.cell(fill: rgb(model.risk_levels.medium.color))[#text(fill: white, weight: "bold")[5]],
)

#pagebreak()

= Risk Categories

The risks are organized into the following categories:

#for cat in model.risk_categories [
  == #cat.name
  
  #emph[#cat.description]
  
  #v(0.5em)
]

#pagebreak()

= Detailed Risk Register

#for risk in risks [
  == Risk #risk.id: #risk.title
  
  #grid(
    columns: (auto, 1fr),
    row-gutter: 0.3em,
    column-gutter: 1em,
    
    [*Risk ID:*], [#risk.id],
    [*Category:*], [#risk.category],
    [*CRA Requirement:*], [#risk.cra_requirement],
  )
  
  #v(0.5em)
  
  === Description
  #risk.description
  
  === Threat Source
  #risk.threat_source
  
  === Vulnerability
  #risk.vulnerability
  
  === Initial Risk Assessment
  
  #let initial_score = calc_risk(risk.impact, risk.probability)
  #let (initial_level, initial_color) = get_risk_level(initial_score)
  
  #grid(
    columns: (1fr, 1fr, 1fr, 1fr),
    row-gutter: 0.5em,
    column-gutter: 0.5em,
    
    [*Impact*], [*Probability*], [*Risk Score*], [*Risk Level*],
    
    box(fill: rgb(model.severity_levels.at(risk.impact).color), inset: 5pt, radius: 2pt)[
      #text(fill: white, weight: "bold", size: 9pt)[
        #upper(risk.impact)
      ]
    ],
    
    [#upper(risk.probability)],
    
    [#initial_score],
    
    box(fill: rgb(initial_color), inset: 5pt, radius: 2pt)[
      #text(fill: white, weight: "bold", size: 9pt)[
        #upper(initial_level)
      ]
    ],
  )
  
  === Existing Controls
  
  #for control in risk.existing_controls [
    - #control
  ]
  
  === Residual Risk Assessment
  
  #let residual_score = calc_risk(risk.residual_risk_impact, risk.residual_risk_probability)
  #let (residual_level, residual_color) = get_risk_level(residual_score)
  
  #grid(
    columns: (1fr, 1fr, 1fr, 1fr),
    row-gutter: 0.5em,
    column-gutter: 0.5em,
    
    [*Impact*], [*Probability*], [*Risk Score*], [*Risk Level*],
    
    box(fill: rgb(model.severity_levels.at(risk.residual_risk_impact).color), inset: 5pt, radius: 2pt)[
      #text(fill: white, weight: "bold", size: 9pt)[
        #upper(risk.residual_risk_impact)
      ]
    ],
    
    [#upper(risk.residual_risk_probability)],
    
    [#residual_score],
    
    box(fill: rgb(residual_color), inset: 5pt, radius: 2pt)[
      #text(fill: white, weight: "bold", size: 9pt)[
        #upper(residual_level)
      ]
    ],
  )
  
  === Additional Controls
  
  #if risk.additional_controls.len() > 0 [
    #table(
      columns: (2fr, 1fr, auto, auto),
      stroke: 0.5pt,
      align: (left, left, center, center),
      
      [*Control*], [*Responsible*], [*Deadline*], [*Status*],
      
      ..for ctrl in risk.additional_controls {
        (
          ctrl.control,
          ctrl.responsible,
          ctrl.deadline,
          if ctrl.status == "completed" [✓] else if ctrl.status == "in_progress" [⟳] else if ctrl.status == "ongoing" [∞] else [○],
        )
      }
    )
  ] else [
    _No additional controls required._
  ]
  
  #v(1em)
  #line(length: 100%, stroke: 0.5pt)
  #v(1em)
]

#pagebreak()

= Risk Summary

== Risks by Initial Level

#let initial_risk_counts = (
  critical: 0,
  high: 0,
  medium: 0,
  low: 0,
  very_low: 0,
)

#for risk in risks {
  let score = calc_risk(risk.impact, risk.probability)
  let (level, _) = get_risk_level(score)
  initial_risk_counts.insert(level, initial_risk_counts.at(level) + 1)
}

#table(
  columns: (1fr, auto),
  stroke: 0.5pt,
  
  [*Risk Level*], [*Count*],
  [CRITICAL], str(initial_risk_counts.critical),
  [HIGH], str(initial_risk_counts.high),
  [MEDIUM], str(initial_risk_counts.medium),
  [LOW], str(initial_risk_counts.low),
  [VERY LOW], str(initial_risk_counts.very_low),
)

== Risks by Residual Level

#let residual_risk_counts = (
  critical: 0,
  high: 0,
  medium: 0,
  low: 0,
  very_low: 0,
)

#for risk in risks {
  let score = calc_risk(risk.residual_risk_impact, risk.residual_risk_probability)
  let (level, _) = get_risk_level(score)
  residual_risk_counts.insert(level, residual_risk_counts.at(level) + 1)
}

#table(
  columns: (1fr, auto),
  stroke: 0.5pt,
  
  [*Risk Level*], [*Count*],
  [CRITICAL], str(residual_risk_counts.critical),
  [HIGH], str(residual_risk_counts.high),
  [MEDIUM], str(residual_risk_counts.medium),
  [LOW], str(residual_risk_counts.low),
  [VERY LOW], str(residual_risk_counts.very_low),
)

#pagebreak()

= Action Items

== Controls by Status

#let all_controls = ()
#for risk in risks {
  for ctrl in risk.additional_controls {
    all_controls.push((
      risk_id: risk.id,
      control: ctrl.control,
      responsible: ctrl.responsible,
      deadline: ctrl.deadline,
      status: ctrl.status,
    ))
  }
}

=== In Progress

#table(
  columns: (auto, 2fr, 1fr, auto),
  stroke: 0.5pt,
  align: (left, left, left, center),
  
  [*Risk ID*], [*Control*], [*Responsible*], [*Deadline*],
  
  ..for ctrl in all_controls.filter(c => c.status == "in_progress") {
    (
      ctrl.risk_id,
      ctrl.control,
      ctrl.responsible,
      ctrl.deadline,
    )
  }
)

=== Planned

#table(
  columns: (auto, 2fr, 1fr, auto),
  stroke: 0.5pt,
  align: (left, left, left, center),
  
  [*Risk ID*], [*Control*], [*Responsible*], [*Deadline*],
  
  ..for ctrl in all_controls.filter(c => c.status == "planned") {
    (
      ctrl.risk_id,
      ctrl.control,
      ctrl.responsible,
      ctrl.deadline,
    )
  }
)

#pagebreak()

= CRA Compliance Mapping

This section maps the identified risks to specific Cyber Resilience Act requirements.

#let cra_mapping = (:)
#for risk in risks {
  let req = risk.cra_requirement
  if req not in cra_mapping {
    cra_mapping.insert(req, ())
  }
  cra_mapping.at(req).push(risk.id)
}

#table(
  columns: (1fr, 2fr),
  stroke: 0.5pt,
  align: (left, left),
  
  [*CRA Requirement*], [*Risk IDs*],
  
  ..for (req, risk_ids) in cra_mapping {
    (
      req,
      risk_ids.join(", "),
    )
  }
)

#pagebreak()

= Review and Approval

== Assessment Team

#table(
  columns: (1fr, 1fr),
  stroke: 0.5pt,
  
  [*Role*], [*Name/Signature*],
  [Risk Assessor], [#metadata.assessor],
  [Security Manager], [________________],
  [Product Manager], [________________],
  [Chief Technology Officer], [________________],
)

#v(2em)

== Review Schedule

This risk assessment shall be reviewed and updated:
- At minimum annually
- When significant system changes occur
- When new threats or vulnerabilities are identified
- Following security incidents
- As required by regulatory updates

*Next Scheduled Review:* #metadata.review_date

#v(2em)

== Document Control

#table(
  columns: (auto, auto, 1fr),
  stroke: 0.5pt,
  
  [*Version*], [*Date*], [*Changes*],
  [#metadata.version], [#metadata.assessment_date], [Initial risk assessment],
)

#v(3em)

#align(center)[
  #text(size: 9pt, style: "italic")[
    This document contains confidential information.\
    Distribution restricted to authorized personnel only.
  ]
]
