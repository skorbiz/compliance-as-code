# ADR 0001: Compliance Documents as Code

- Status: Proposal
- Date: 2026-02-11
- Deciders: Project contributors

## Context

This ADR discusses the benefits and a potential pipeline for producing compliance-oriented documents as code. That means producing CE declaration, CRA-aligned risk assessment, SBOM, and user manual from version-controlled, structured sources.

Traditional approaches usually store these artifacts as Word/Excel files on shared drives or SharePoint.
We want a workflow that treats compliance artifacts like other engineering deliverables: reviewable, testable, reproducible, and automatable.

## Why code-based compliance documents?

### What Word/Excel/SharePoint does well

- **Familiarity and accessibility:** Non-engineering stakeholders can edit and review easily.
- **Existing templates and standards:** Established org formatting and workflows already exist.
- **Low overhead for simple docs:** Works well when content is mostly narrative and not driven by structured data.

### What code-based workflows do well
- **Known workflow for developers:** Edit → commit → PR → review → merge
- **Version control with history:** clear diffs, history, PR-based review, and clear “who changed what and why.”
- **Validation and correctness:** Schema validation and tests catch missing fields, invalid enums, and regressions.
- **Single source of truth:** Structured data can drive multiple documents if needed (or repeat in same document).
- **Automation friendly:** Deterministic builds (same inputs → same outputs), CI generation per tag/release, and consistent formatting.
- **Traceability and ecosystem integration:** Easier to link risks to commits, issues, releases, tests, and evidence.
- **Future enablement:** Creates a foundation for AI-assisted drafting/review (e.g., completeness checks, suggested mitigations), while keeping the authoritative source structured and validated.

**Trade-offs**
- **Learning curve:** Typst + Pydantic is less familiar than Office tools for many stakeholders.
- **Schema maintenance:** Evolving schemas requires keeping validators/tests in sync.
- **Stakeholder workflows:** Some reviewers will still prefer Word-style commenting unless provided rendered PDFs.

## Suggested approach

Use a “compliance-as-code” pipeline where:

- Compliance content is stored as **structured YAML** (source data)
- Document templates are written in **Typst**, loading YAML data at build time
- Data is validated using **Pydantic schemas** (single source of truth)
- **JSON Schema** is exported for IDE support (e.g., YAML autocomplete/validation)
- Documents are rendered to **PDF using Typst**
- A single build entrypoint (**python/uv script**) orchestrates: validate → export schema → render documents
- Tests (**pytest**) verify:
  - YAML validates against schemas
  - schema rules behave as expected
  - compliance requirements are enforced (e.g., no high risks without mitigations)
- A minimal **Docusaurus** site is generated from the same YAML source data. This is partly to show the model driven approach investigates complexities of a Docusaurus output. 

## Reference folder structure


```
compliance-as-code/
├── model/                          # Source YAML models/data
│   ├── model/schemas.py            # Pydantic schema definitions
│   ├── risk_model.yaml             # Risk assessment model (severity/probability scales)
│   ├── risks.yaml                  # Risk register with identified risks
│   └── sbom.yaml                   # Software bill of materials
│
├── docs/                           # Typst document templates
│   ├── ce.typ                      # CE Declaration template
│   ├── manual.typ                  # User manual template
│   ├── risk-assessment.typ         # Risk assessment document template
│   └── sbom.typ                    # SBOM document template
│
├── tests/                          # Test suite
│   ├── test_schemas.py             # Schema validation tests
│   └── test_review_schedule.py     # Example of using monitoring compliance deadlines with tests
│
├── schemas-generated/json-schemas/ # Auto-generated JSON schemas for IDE validation (gitignored)
│   ├── risk-model.schema.json
│   └── ...
│
├── website/                                  # Docusaurus documentation site
│   ├── scripts/generate_docs_from_yaml.py    # YAML -> markdown generator for web docs
│   ├── docs/                                 # Markdown pages (some generated from YAML)
│   └── docusaurus.config.js
│
├── main.py                         # Build orchestrator
└── pyproject.toml                  # Python dependencies

```


## Alternatives considered

### A. Keep Word/Excel + SharePoint
- Pros: Familiar, easy for non-engineers, existing templates.
- Cons: Weak validation, poor diffs, hard automation, fragile macros, duplicated content, difficult reproducible builds.

### B. Dedicated GRC platforms
- Pros: Built-in workflow controls, audit trails, reporting, and program management features.
- Cons: Hard to find the right fit, licensing costs, vendor lock-in, integration overhead, less flexibility, and limited agent/code friendliness.

### C. Markdown/AsciiDoc + Pandoc
- Pros: Simple authoring, widely used, good diffs, Pandoc supports many outputs.
- Cons: Structured data validation still needs a schema system; complex layouts/tables can be harder; PDF styling may require LaTeX.

### D. LaTeX
- Pros: Powerful typesetting, mature ecosystem.
- Cons: Steeper learning curve; higher template complexity; slower iteration for non-LaTeX users.

### E. Keep YAML, validate with JSON Schema directly (no Pydantic)
- Pros: Language-agnostic schema; many validators exist.
- Cons: Harder to express richer constraints/derived validation.

### F. Other validation frameworks
- Examples: `jsonschema`, `yamale`, `cerberus`, `voluptuous`, `pandera`, OPA/Rego.
- Rationale for Pydantic here: strong typing model, good error messages, easy composition, and straightforward JSON Schema export.

### G. Use SBOM standards output directly (CycloneDX/SPDX tooling)
- Pros: Standardized interchange formats, better ecosystem integration.
- Cons: Goal here is a compliance document + process pipeline; standards export can be added later without changing the core approach.

### I. Docusaurs for all outputs (no Typst/PDF)
- Pros: Single output format.
- Cons: Much less formal/printable artifact. No native yaml embedding. Based on limited markdown syntax.

## Consequences
- We standardize on YAML + Pydantic as the source-of-truth data model for compliance documents.
- Document generation becomes buildable and testable like application code.
- The same source data can feed both formal PDFs (Typst) and browsable web docs (Docusaurus).
- The repo becomes the authoritative location for compliance artifacts (inputs, validation rules, generated PDFs, and generated web pages).

## Next steps (out of scope for this ADR)
- Add schema evolution guidance (versioning, deprecations).
- Consider exporting additional machine-readable outputs (CycloneDX/SPDX, CSV extracts).
- Add evidence links (tickets, threat modeling outputs, security test results) tied to risk IDs.
- Expand generated Docusaurus pages beyond the first risk-model summary page if the MVP proves useful.
