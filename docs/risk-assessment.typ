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

// Get risk level based on score
#let get_risk_level(score) = {
  if score >= 15 {
    ("critical", "#8B0000")
  } else if score >= 10 {
    ("high", "#DC143C")
  } else if score >= 6 {
    ("medium", "#FFA500")
  } else {
    ("low", "#90EE90")
  }
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

= Detailed Risk Register

#for risk in risk_data.risks [
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
          str(ctrl.deadline),
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

= Review Schedule

This risk assessment shall be reviewed and updated:
- At minimum annually
- When significant system changes occur
- When new threats or vulnerabilities are identified
- Following security incidents
- As required by regulatory updates

*Next Scheduled Review:* #metadata.review_date
