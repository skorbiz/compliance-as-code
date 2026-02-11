# ADR 0001: Compliance Documents as Code (PoC)

- Status: Proposal
- Date: 2026-02-11
- Deciders: Project contributors

## Context

This proof-of-concept (PoC) explores producing compliance-oriented documents (CE declaration, CRA-aligned risk assessment, SBOM, user manual) from version-controlled, structured sources.

Traditional approaches usually store these artifacts as Word/Excel files on shared drives or SharePoint. That workflow often leads to:

- Manual, error-prone edits and copy/paste across documents
- Weak validation (structure, required fields, consistent IDs, dates)
- Limited review ergonomics (diffs are noisy, merge conflicts are hard)
- Difficult automation (CI checks, reproducible builds)
- Tool-driven fragmentation (templates, macros, hidden spreadsheet logic)

We want a workflow that treats compliance artifacts like other engineering deliverables: reviewable, testable, reproducible, and automatable.

## Decision

Use a “compliance-as-code” pipeline where:

- Compliance content is stored as **structured YAML** (source data)
- Data is validated using **Pydantic schemas** (single source of truth)
- **JSON Schema** is exported for IDE support (e.g., YAML autocomplete)
- Documents are rendered to **PDF using Typst**
- A single build entrypoint (a CLI task/script) orchestrates validate → export schema → render documents
- Tests (pytest) verify the YAML validates and the schemas behave as expected

This PoC keeps the documents and their source data in the same repository as the project, enabling standard engineering controls (code review, CI, traceability).

## Pipeline (reference implementation)

1. **Author / edit source data**
  - YAML files for risks, SBOM, declarations, and other structured inputs (e.g., `data/risks.yaml`, `data/sbom.yaml`)

2. **Validate**
  - Pydantic models validate YAML structure and constraints
  - A build command (e.g., `main.py --validate`) and tests fail fast on invalid data

3. **Export schemas for tooling**
  - A build command (e.g., `main.py --export-schemas`) exports auto-generated JSON Schemas used by IDE tooling
   - Generated artifacts are clearly marked as auto-generated and not hand-edited

4. **Render documents**
  - Typst sources load YAML (e.g., `yaml("/data/risks.yaml")`) and produce PDFs
  - A build command (e.g., `main.py --all`) renders the document set

5. **CI-friendly execution**
   - Command-line pipeline is deterministic and suitable for CI runners
   - Dependencies are managed with `uv`

## Why this is better than Word/Excel/SharePoint

### Advantages

- **Version control & reviewability**
  - Small, readable diffs for YAML/Typst
  - PR-based review with comments tied to exact lines
  - Easy history/blame to answer “who changed what and why?”

- **Validation and correctness by construction**
  - Schema validation prevents missing required fields, invalid enums, malformed IDs/dates
  - Tests catch regressions early (before PDF generation or audit deadlines)

- **Single source of truth**
  - The same YAML data can drive multiple outputs (risk assessment, CE annexes, summaries)
  - Eliminates copy/paste divergence across documents

- **Automation and repeatability**
  - Deterministic builds: same inputs → same outputs
  - Works in CI to generate artifacts per release tag

- **Traceability and audit readiness**
  - Link compliance changes to commits, releases, issues, and evidence
  - Enables “compliance delta” reporting between versions

- **Tooling ergonomics**
  - JSON Schema export enables IDE autocomplete/validation for YAML editors

### Trade-offs / risks

- **Learning curve**: Typst + Pydantic is less familiar than Office tools.
- **Schema maintenance**: updating a schema requires updating validation/tests.
- **Stakeholder access**: some non-engineering stakeholders prefer Word workflows.
- **Rendering tool choice**: Typst is newer than LaTeX and may have fewer org-standard templates.

## Alternatives considered

### A. Keep Word/Excel + SharePoint

- Pros: familiar, easy for non-engineers, existing templates.
- Cons: weak validation, poor diffs, hard automation, fragile macros, duplicated content, difficult reproducible builds.

### B. Markdown/AsciiDoc + Pandoc

- Pros: simple authoring, widely used, good diffs, Pandoc supports many outputs.
- Cons: structured data validation still needs a schema system; complex layouts and tables can be harder; PDF styling may require LaTeX.

### C. LaTeX

- Pros: powerful typesetting, mature ecosystem.
- Cons: steeper learning curve; much higher template complexity; slower iteration for non-LaTeX users.

### D. Keep YAML, validate with JSON Schema directly (no Pydantic)

- Pros: schema is language-agnostic; many validators exist.
- Cons: harder to express richer constraints/derived validation;

### E. Other validation frameworks

- Examples: `jsonschema`, `yamale`, `cerberus`, `voluptuous`, `pandera`, OPA/Rego.
- Rationale for Pydantic here: strong typing model, good error messages, easy composition, and straightforward JSON Schema export.

### F. Use SBOM standards output directly (CycloneDX/SPDX tooling)

- Pros: standardized interchange formats, better ecosystem integration.
- Cons: Goal here is a compliance document + process pipeline; standards export can be added later without changing the core approach.

## Consequences

- We standardize on YAML + Pydantic as the source-of-truth data model for compliance documents in this PoC.
- Document generation becomes buildable and testable like application code.
- The repo becomes the authoritative location for compliance artifacts (inputs, validation rules, and generated PDFs).

## Next steps (out of scope for this ADR)

- Add schema evolution guidance (versioning, deprecations)
- Consider exporting additional machine-readable outputs (CycloneDX/SPDX, CSV extracts)
- Add evidence links (tickets, threat modeling outputs, security test results) tied to risk IDs
