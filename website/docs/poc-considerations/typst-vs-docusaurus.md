---
title: Typst vs Docusaurus
---

# Typst vs Docusaurus in This PoC

Both are useful, but for different outputs.

| Area | Typst | Docusaurus |
| --- | --- | --- |
| Primary use | Formal compliance PDFs | Web documentation site |
| Best for | Printable, controlled layouts | Navigation, discoverability, cross-linking |
| Data source fit | Strong when fed by YAML at compile time | Strong when generated markdown is built from YAML |
| Reviewer experience | Good for sign-off and archived artifacts | Good for browsing and quick review |
| Weakness | Harder to browse large document sets | Not ideal for strict formal document formatting |

## Practical Guidance

- Keep Typst as the official artifact generator for CE/manual/risk/SBOM PDFs.
- Keep Docusaurus as a lightweight browsing layer from the same source data.
- Generate only a few pages from YAML in this PoC to keep complexity low.
