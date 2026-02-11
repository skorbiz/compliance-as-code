#set page(
  paper: "a4",
  margin: (x: 2.5cm, y: 2.5cm),
)

#set text(
  size: 11pt,
)

// Load SBOM data from YAML files
#let manual_data = yaml("sbom_manual.yaml")
#let generated_data = yaml("sbom_generated.yaml")

// Extract metadata
#let metadata = manual_data.at("metadata", default: (
  product_name: "Product Name",
  product_version: "1.0.0",
  vendor: "Vendor Name",
  release_date: "2026-01-01",
  sbom_version: "1.0"
))

#align(center)[
  #text(size: 18pt, weight: "bold")[
    Software Bill of Materials (SBOM)
  ]
  
  #v(1em)
  
  #text(size: 14pt)[
    #metadata.product_name v#metadata.product_version
  ]
]

#v(2em)

= Document Information

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  align: (left, left),
  
  [*Field*], [*Value*],
  [Product Name], [#metadata.product_name],
  [Product Version], [#metadata.product_version],
  [Vendor], [#metadata.vendor],
  [Release Date], [#metadata.release_date],
  [SBOM Version], [#metadata.sbom_version],
  [SBOM Format], [Typst/YAML],
  [Document Generated], [#datetime.today().display("[day] [month repr:long] [year]")],
)

#pagebreak()

= Purpose and Scope

This Software Bill of Materials (SBOM) provides a comprehensive inventory of all software components, libraries, and dependencies included in #metadata.product_name. This document is maintained to ensure transparency, support vulnerability management, and meet regulatory compliance requirements.

== What is an SBOM?

A Software Bill of Materials is a complete, formally structured list of components, libraries, and modules that are required to build and run a software application. It serves similar purposes to a bill of materials in manufacturing, providing:

- Transparency about software composition
- Support for security vulnerability tracking
- License compliance verification
- Supply chain risk management

== Scope

This SBOM covers:
- Direct dependencies explicitly included in the project
- Runtime dependencies and tools
- System-level components
- Third-party libraries and frameworks

#pagebreak()

= Component Summary

#let manual_components = manual_data.at("components", default: ())
#let generated_components = generated_data.at("components", default: ())

// Ensure components are arrays
#let manual_components = if type(manual_components) == array { manual_components } else { () }
#let generated_components = if type(generated_components) == array { generated_components } else { () }

#let total_components = manual_components.len() + generated_components.len()

#table(
  columns: (1fr, auto),
  stroke: 0.5pt,
  
  [*Category*], [*Count*],
  [Manual Components], [#manual_components.len()],
  [Generated Components (Python Dependencies)], [#generated_components.len()],
  [*Total Components*], [*#total_components*],
)

#pagebreak()

= Manual Components

These components are manually tracked and not automatically detected by dependency analysis tools.

#if manual_components.len() > 0 [
  #table(
    columns: (auto, auto, auto, 1fr, 1fr),
    stroke: 0.5pt,
    align: (left, left, left, left, left),
    
    [*Name*], [*Version*], [*Type*], [*License*], [*Supplier*],
    
    ..for component in manual_components {
      (
        component.at("name", default: "N/A"),
        component.at("version", default: "N/A"),
        component.at("type", default: "N/A"),
        component.at("license", default: "N/A"),
        component.at("supplier", default: "N/A"),
      )
    }
  )
  
  #v(1em)
  
  == Detailed Component Information
  
  #for component in manual_components [
    === #component.at("name", default: "Unknown")
    
    #table(
      columns: (auto, 1fr),
      stroke: 0.5pt,
      align: (left, left),
      
      [*Name*], [#component.at("name", default: "N/A")],
      [*Version*], [#component.at("version", default: "N/A")],
      [*Type*], [#component.at("type", default: "N/A")],
      [*License*], [#component.at("license", default: "N/A")],
      [*Supplier*], [#component.at("supplier", default: "N/A")],
      [*Description*], [#component.at("description", default: "N/A")],
    )
    
    #v(1em)
  ]
] else [
  _No manual components defined._
]

#pagebreak()

= Generated Components (Python Dependencies)

These components are automatically extracted from the project's dependency management files.

#if generated_components.len() > 0 [
  #table(
    columns: (1fr, auto, 1fr),
    stroke: 0.5pt,
    align: (left, left, left),
    
    [*Package Name*], [*Version*], [*Type*],
    
    ..for component in generated_components {
      (
        component.at("name", default: "N/A"),
        component.at("version", default: "N/A"),
        component.at("type", default: "N/A"),
      )
    }
  )
  
  #v(1em)
  
  #text(size: 9pt, style: "italic")[
    _Note: Generated from project dependency files. Re-run the SBOM generation script to update this list._
  ]
] else [
  _No Python dependencies found. Run the SBOM generation script to populate this section:_
  
  ```bash
  python3 software-bill-of-materials/scripts/generate_sbom.py
  ```
]

#pagebreak()

= License Summary

#let get_license(component) = {
  component.at("license", default: "Unknown")
}

#let manual_licenses = manual_components.map(get_license)
#let unique_licenses = manual_licenses.dedup()

#if unique_licenses.len() > 0 [
  The following open source and commercial licenses are used by components in this product:
  
  #for license in unique_licenses [
    - #license
  ]
  
  #v(1em)
  
  For detailed license information, please refer to the individual component documentation or contact #metadata.vendor.
] else [
  _License information is being compiled. Please refer to individual component documentation._
]

#pagebreak()

= Vulnerability Management

This SBOM is maintained to support vulnerability scanning and security management processes.

== Scanning Recommendations

Regular security scanning should be performed using tools such as:
- OWASP Dependency-Check
- Snyk
- GitHub Dependabot
- Trivy

== Update Policy

Dependencies are reviewed and updated according to the following schedule:
- Critical security vulnerabilities: Immediately upon disclosure
- High severity vulnerabilities: Within 7 days
- Medium/Low severity: Next scheduled release
- Regular dependency updates: Monthly review

== Reporting Vulnerabilities

If you discover a security vulnerability in any component listed in this SBOM, please report it to:

#grid(
  columns: (auto, 1fr),
  row-gutter: 0.5em,
  column-gutter: 1em,
  
  [*Email:*], [security\@example.com],
  [*Response Time:*], [Within 48 hours for critical issues],
)

#pagebreak()

= SBOM Maintenance

== Update Frequency

This SBOM is updated:
- Automatically: When dependencies are added or updated
- Manually: When system components or tools change
- For each product release
- At minimum: Quarterly review

== Version History

#table(
  columns: (auto, auto, 1fr),
  stroke: 0.5pt,
  
  [*Version*], [*Date*], [*Changes*],
  [#metadata.sbom_version], [#metadata.release_date], [Initial SBOM creation],
)

== Regenerating This Document

To update the generated components section:

```bash
# Generate dependency data
python3 software-bill-of-materials/scripts/generate_sbom.py

# Rebuild SBOM document
python3 main.py --sbom
```

To add manual components, edit:
```
software-bill-of-materials/sbom_manual.yaml
```

#pagebreak()

= Contact Information

For questions about this SBOM or component information:

#grid(
  columns: (auto, 1fr),
  row-gutter: 0.5em,
  column-gutter: 1em,
  
  [*Company:*], [#metadata.vendor],
  [*Email:*], [support\@example.com],
  [*Website:*], [www.example.com],
)

#v(2em)

#align(center)[
  #text(size: 9pt, style: "italic")[
    This document is automatically generated and should not be edited manually.\
    Last generated: #datetime.today().display("[day] [month repr:long] [year]")
  ]
]
