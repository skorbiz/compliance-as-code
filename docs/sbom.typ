#set page(paper: "a4", margin: 2.5cm, numbering: "1")
#set text(size: 11pt)
#set heading(numbering: "1.1")

// Load auto-generated dependencies
#let generated = yaml("/data/sbom.yaml")

// Manual components (infrastructure/tooling not in package manager)
#let manual_components = (
  (name: "Typst", version: "0.14.2", type: "Document Compiler", license: "Apache-2.0"),
  (name: "Python", version: "3.12", type: "Runtime", license: "PSF"),
  (name: "Ubuntu", version: "24.04 LTS", type: "Operating System", license: "Various"),
)

// Metadata
#let product_name = "Example Product"
#let product_version = "1.0.0"
#let vendor = "Your Company"

#align(center)[
  #text(size: 18pt, weight: "bold")[Software Bill of Materials (SBOM)]
  #v(1em)
  #text(size: 14pt)[#product_name v#product_version]
]

#v(2em)

= Document Information

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  [*Product Name*], [#product_name],
  [*Version*], [#product_version],
  [*Vendor*], [#vendor],
  [*Generated*], [#datetime.today().display("[day] [month repr:long] [year]")],
)

#pagebreak()

= Purpose

This Software Bill of Materials provides an inventory of all software components included in #product_name to support:

- Security vulnerability tracking
- License compliance
- Supply chain transparency

= Manual Components

Infrastructure and tooling components:

#table(
  columns: (1fr, auto, auto, auto),
  stroke: 0.5pt,
  [*Name*], [*Version*], [*Type*], [*License*],
  ..manual_components.map(c => (c.name, c.version, c.type, c.license)).flatten()
)

= Python Dependencies

Auto-generated from project dependencies:

#table(
  columns: (1fr, auto, auto),
  stroke: 0.5pt,
  [*Name*], [*Version*], [*Type*],
  ..generated.components.map(c => (c.name, c.version, c.type)).flatten()
)

= License Summary

#let get_license(component) = {
  component.at("license", default: "Unknown")
}

#let manual_licenses = manual_components.map(get_license)
#let generated_licenses = generated.components.map(get_license)
#let all_licenses = manual_licenses + generated_licenses
#let unique_licenses = all_licenses.dedup()

#if unique_licenses.len() > 0 [
  The following open source and commercial licenses are used by components in this product:
  
  #for license in unique_licenses [
    - #license
  ]
  
  #v(1em)
  For detailed license information, please refer to the individual component documentation or contact #vendor.
] else [
  _License information is being compiled. Please refer to individual component documentation._
]

= Summary

#let total = manual_components.len() + generated.components.len()

*Total Components:* #total
- Manual: #manual_components.len()
- Auto-generated: #generated.components.len()


#v(2em)

#align(center)[
  #text(size: 9pt, style: "italic")[
    This document is automatically generated and should not be edited manually.\
    Last generated: #datetime.today().display("[day] [month repr:long] [year]")
  ]
]