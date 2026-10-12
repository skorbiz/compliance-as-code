#set page(paper: "a4", margin: 2cm, numbering: "1")
#set text(size: 10pt)
#set heading(numbering: "1.1")

// Load risk data from YAML
#let model = yaml("/model/risk_model.yaml")
#let risk_data = yaml("/model/risks.yaml")
#let metadata = risk_data.metadata

// IEC 62443-3-3 foundational-requirement id -> display name
#let category_names = (:)
#for c in model.risk_categories {
  category_names.insert(c.id, c.name)
}

// Calculate risk score (impact value x likelihood value)
#let calc_risk(impact, likelihood) = {
  let impact_val = model.impact_levels.at(impact).value
  let likelihood_val = model.likelihood_levels.at(likelihood).value
  impact_val * likelihood_val
}

// Get risk level (key + definition) for a score, from risk_levels in risk_model.yaml.
// risk_levels is ordered highest threshold first, so the first match wins.
#let get_risk_level(score) = {
  let result = none
  for (k, v) in model.risk_levels.pairs() {
    if result == none and score >= v.threshold {
      result = (k, v)
    }
  }
  result
}

#let pretty(key) = upper(key.at(0)) + key.slice(1)

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
    [*Assessors:*], [#metadata.assessors],
    [*Reviewer:*], [#metadata.reviewer],
    [*Next Review:*], [#if metadata.review_date == none [_Pending_] else [#metadata.review_date]],
  )
]

#pagebreak()
#outline(title: [Contents], indent: auto, depth: 2)
#pagebreak()

= Executive Summary

This document presents a cybersecurity risk assessment for #metadata.product_name in accordance with the EU Cyber Resilience Act (CRA).

*Scope:* #metadata.scope

*Total Risks Identified:* #risk_data.risks.len()

#pagebreak()

= Risk Assessment Methodology

Risk Score = Impact × Likelihood (scale 1-4 each, 0 for unscored; max score 16)

== Impact Levels

#table(
  columns: (auto, auto, auto),
  stroke: 0.5pt,
  [*Level*], [*Value*], [*Color*],
  ..model.impact_levels.pairs().map(((k, v)) => (
    [#pretty(k)],
    [#v.value],
    box(fill: rgb(v.color), width: 1cm, height: 0.5cm),
  )).flatten()
)

== Likelihood Levels

#table(
  columns: (auto, auto),
  stroke: 0.5pt,
  [*Level*], [*Value*],
  ..model.likelihood_levels.pairs().map(((k, v)) => ([#pretty(k)], [#v.value])).flatten()
)

== Risk Levels

#table(
  columns: (auto, auto, 1fr, 1fr),
  stroke: 0.5pt,
  [*Level*], [*Threshold*], [*Description*], [*Action*],
  ..model.risk_levels.pairs().map(((k, v)) => (
    box(fill: rgb(v.color), inset: 4pt, radius: 2pt)[
      #text(fill: white, weight: "bold", size: 9pt)[#upper(pretty(k))]
    ],
    [#v.threshold],
    [#v.description],
    [#v.action],
  )).flatten()
)

== Risk Categories

Each risk may optionally be tagged with one or more IEC 62443-3-3 foundational requirements (FRs):

#table(
  columns: (auto, auto, 1fr),
  stroke: 0.5pt,
  [*ID*], [*Name*], [*Description*],
  ..model.risk_categories.map((c) => ([#upper(c.id)], [#c.name], [#c.description])).flatten()
)

== Risk Treatment

Every risk records an explicit treatment decision: *undecided* (no decision yet), *accept* (tolerated as-is),
*transfer* (shifted to a third party), or *mitigate* (reduced through additional controls).

#pagebreak()

= Detailed Risk Register

#for risk in risk_data.risks [
  == Risk #risk.id: #risk.title
  
  #grid(
    columns: (auto, 1fr),
    row-gutter: 0.3em,
    column-gutter: 1em,
    
    [*Risk ID:*], [#risk.id],
    [*Category:*], [#let category = risk.at("category", default: ())
      #if category.len() > 0 [#category.map((id) => category_names.at(id, default: id)).join(", ")] else [—]],
    [*Zone:*], [#upper(risk.zone_edge_cloud)],
    [*Conduit / exposure area:*], [#risk.conduit_or_exposure_area],
    [*Phases:*], [#risk.phases.map(pretty).join(", ")],
    [*Treatment:*], [#pretty(risk.at("treatment", default: "undecided"))],
  )
  
  #v(0.5em)
  
  #if risk.at("iec_62443_3_3_requirement_inspiration", default: "") != "" [
    === IEC 62443-3-3 Requirement Inspiration
    #risk.iec_62443_3_3_requirement_inspiration
  ]
  
  === Vulnerability
  #if risk.at("vulnerability", default: "") != "" [#risk.vulnerability] else [—]
  
  === Threat
  #risk.threat
  
  === Consequence
  #risk.consequence
  
  === Initial Risk Assessment
  
  #let initial_score = calc_risk(risk.impact, risk.likelihood)
  #let (initial_level, initial_def) = get_risk_level(initial_score)
  
  #grid(
    columns: (1fr, 1fr, 1fr, 1fr),
    row-gutter: 0.5em,
    column-gutter: 0.5em,
    
    [*Impact*], [*Likelihood*], [*Risk Score*], [*Risk Level*],
    
    box(fill: rgb(model.impact_levels.at(risk.impact).color), inset: 5pt, radius: 2pt)[
      #text(fill: white, weight: "bold", size: 9pt)[
        #upper(risk.impact)
      ]
    ],
    
    [#upper(risk.likelihood)],
    
    [#initial_score],
    
    box(fill: rgb(initial_def.color), inset: 5pt, radius: 2pt)[
      #text(fill: white, weight: "bold", size: 9pt)[
        #upper(initial_level)
      ]
    ],
  )
  
  === Existing Controls
  
  #let existing_controls = risk.at("existing_controls", default: ())
  #if existing_controls.len() > 0 [
    #for control in existing_controls [
      - #control
    ]
  ] else [
    _None_
  ]
  
  === Residual Risk Assessment
  
  #if risk.at("impact_residual", default: none) != none [
    #let residual_score = calc_risk(risk.impact_residual, risk.likelihood_residual)
    #let (residual_level, residual_def) = get_risk_level(residual_score)
    
    #grid(
      columns: (1fr, 1fr, 1fr, 1fr),
      row-gutter: 0.5em,
      column-gutter: 0.5em,
      
      [*Impact*], [*Likelihood*], [*Risk Score*], [*Risk Level*],
      
      box(fill: rgb(model.impact_levels.at(risk.impact_residual).color), inset: 5pt, radius: 2pt)[
        #text(fill: white, weight: "bold", size: 9pt)[
          #upper(risk.impact_residual)
        ]
      ],
      
      [#upper(risk.likelihood_residual)],
      
      [#residual_score],
      
      box(fill: rgb(residual_def.color), inset: 5pt, radius: 2pt)[
        #text(fill: white, weight: "bold", size: 9pt)[
          #upper(residual_level)
        ]
      ],
    )
  ] else [
    _Not yet assessed._
  ]
  
  === Additional Controls
  
  #let additional_controls = risk.at("additional_controls", default: ())
  #if additional_controls.len() > 0 [
    #table(
      columns: (1fr, 2fr, 1fr, auto),
      stroke: 0.5pt,
      align: (left, left, left, center),
      
      [*Task*], [*Description*], [*Owner*], [*Due Date*],
      
      ..for ctrl in additional_controls {
        (
          ctrl.task,
          ctrl.description,
          ctrl.owner,
          str(ctrl.due_date),
        )
      }
    )
  ] else [
    _No additional controls required._
  ]
  
  #if risk.at("notes", default: "") != "" [
    === Notes
    #risk.notes
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

*Next Scheduled Review:* #if metadata.review_date == none [_Pending_] else [#metadata.review_date]

