# ADR-001: Compliance as Code - Document Generation and Validation

**Status:** Accepted

**Date:** 2026-02-11

**Authors:** Engineering Team

**Decision:** Implement compliance documentation (CE declaration, risk assessments, SBOM, manuals) as code using structured data (YAML), validation schemas (Pydantic), and programmatic document generation (Typst).

---

## Context

Traditional compliance documentation suffers from critical challenges:

### Problems with Traditional Approaches (Excel/Word)

1. **No Validation**
   - Manual entry errors in risk severity/probability
   - Inconsistent terminology across documents
   - Missing required fields discovered late in audits
   - No enforcement of business rules

2. **Manual Maintenance Overhead**
   - Copy-paste errors between related documents
   - Version control conflicts
   - Difficult to track who changed what and when
   - Risk register updates don't propagate to manual

3. **No Automation**
   - Cannot integrate with CI/CD pipelines
   - No automated checks for compliance violations
   - Manual SBOM generation from dependencies
   - Cannot link risks to code commits/issues

4. **Audit Trail Issues**
   - Changes tracked in separate "revision history" tables
   - No atomic commits linking related changes
   - Difficult to prove document state at specific dates

5. **Collaboration Friction**
   - Email attachments with conflicting versions
   - "final_v2_reviewed_FINAL.xlsx"
   - Merge conflicts in binary formats
   - Limited to one editor at a time (or complex merging)

### Regulatory Context

For products requiring CE marking under the Cyber Resilience Act (CRA):
- **Risk assessment** must be documented and maintained (Articles 13, 14)
- **SBOM** required for vulnerability management
- **User documentation** must include security information
- **Traceability** from requirements → risks → mitigations → tests

Auditors need to see that these documents are:
- Consistent with each other
- Based on validated data
- Maintained throughout product lifecycle
- Traceable to actual product state

---

## Decision

Implement **Compliance as Code** using:

### 1. Structured Data (YAML)

Store compliance data in human-readable, version-controllable YAML:

```yaml
# risk-assessment/risks.yaml
- id: R001
  category: data_security
  title: Unauthorized access to customer data
  impact: critical
  probability: possible
  existing_controls:
    - Multi-factor authentication
    - Role-based access control
  cra_requirement: Article 13(2) - Secure by default
```

**Benefits:**
- Git-friendly text format
- Human-readable and editable
- Structured for automation
- Diff-friendly for reviews

### 2. Schema Validation (Pydantic)

Define schemas as Python code for validation:

```python
class Risk(BaseModel):
    id: str = Field(pattern=r"^R\d{3}$")
    impact: SeverityLevel  # Enum ensures valid values
    probability: ProbabilityLevel
    cra_requirement: str = Field(min_length=10)
```

**Validation enforces:**
- ✅ Required fields present
- ✅ Severity/probability from allowed values only
- ✅ Risk IDs follow R### format and are unique
- ✅ Dates are valid (review > assessment)
- ✅ Cross-references exist (categories defined in model)
- ✅ Business rules (residual risk ≤ initial risk)

### 3. Automated Document Generation (Typst)

Generate PDFs programmatically from validated data:

```typst
#let risks = yaml("risks.yaml")
#for risk in risks.risks [
  === #risk.id: #risk.title
  *Initial Risk:* #risk.impact × #risk.probability
]
```

**Benefits:**
- Consistent formatting across all documents
- Single source of truth (YAML)
- Changes propagate automatically
- Professional typesetting

### 4. CI/CD Integration

Validation runs automatically on every commit:

```yaml
# .github/workflows/validate.yml
- name: Validate compliance data
  run: python3 main.py --validate-only
```

**Enforces:**
- ❌ Fail build if YAML invalid
- ❌ Fail if residual risk > acceptance criteria
- ❌ Fail if hazards lack mitigations
- ❌ Fail if risks in manual don't exist
- ✅ Only merge if compliance data is valid

### 5. Integrated Workflow

Single command runs complete workflow:

```bash
python3 main.py --all
# 1. Validate YAML (fail fast on errors)
# 2. Export JSON Schemas (for IDE tooling)
# 3. Generate SBOM (auto-extract dependencies)
# 4. Build PDFs (CE, manual, SBOM, risk assessment)
```

---

## Advantages

### 1. Validation & Automation (Where Excel Dies)

**Problem:** Excel allows any input, no validation
**Solution:** Pydantic schemas enforce constraints

| Check | Excel | Compliance as Code |
|-------|-------|-------------------|
| Severity must be 1-5 | ❌ Can enter "high" or 7 | ✅ Enum enforced |
| Risk IDs unique | ❌ Manual check | ✅ Automatic validation |
| Dates valid | ❌ Can enter text | ✅ Type-checked |
| Required fields | ❌ Empty cells allowed | ✅ ValidationError raised |
| Cross-references | ❌ Broken links possible | ✅ Validated at build time |

### 2. CI/CD Enforcement

**Excel:** No way to enforce rules automatically
**Our approach:** CI pipeline as compliance gatekeeper

```python
# Example CI checks (in tests/)
def test_all_hazards_have_mitigations(risks):
    for risk in risks:
        assert len(risk.existing_controls) > 0, \
            f"{risk.id} has no mitigations"

def test_no_high_risks_accepted(risks):
    for risk in risks:
        score = risk.residual_risk_impact * risk.residual_risk_probability
        assert score < ACCEPTANCE_THRESHOLD, \
            f"{risk.id} exceeds risk acceptance"

def test_all_manual_risks_exist(manual, risk_register):
    manual_ids = extract_risk_ids_from_manual()
    register_ids = {r.id for r in risk_register.risks}
    assert manual_ids.issubset(register_ids), \
        "Manual references non-existent risks"
```

**Result:** Cannot merge code that violates compliance rules

### 3. Traceability & Linking

Link compliance artifacts to development:

```yaml
# risks.yaml with git integration
- id: R005
  title: SQL injection vulnerability
  existing_controls:
    - Parameterized queries
  related_commits:
    - abc123f  # Link to commit that added mitigation
  related_issues:
    - "#142"  # GitHub issue
  test_coverage:
    - tests/test_db_security.py::test_sql_injection
  requirements:
    - REQ-SEC-003
```

**Enables:**
- Audit trail: risk → mitigation → code → test
- Impact analysis: "This requirement affects which risks?"
- Coverage reports: "Which risks lack test coverage?"
- Automatic updates: SBOM regenerated when dependencies change

### 4. Version Control Benefits

**Excel/Word:**
- Binary formats, poor diffs
- "Track Changes" separate from source control
- Merge conflicts are nightmares

**YAML + Git:**
```diff
  - id: R001
-   probability: likely
+   probability: possible
    additional_controls:
+     - control: Implement rate limiting
+       deadline: 2026-03-01
+       status: in_progress
```

**Readable change history:**
- Who changed what, when, why (commit message)
- Easy code review: "Does this risk assessment make sense?"
- Rollback to any previous state
- Blame: "Who accepted this high risk?"

### 5. Single Source of Truth

**Problem:** Excel risk register ≠ Word manual ≠ actual code
**Solution:** YAML generates all documents

```
risks.yaml (source of truth)
    ↓
    ├─→ risk-assessment.pdf (auto-generated)
    ├─→ manual.pdf (includes risk summary)
    ├─→ CE declaration (references risk analysis)
    └─→ Test requirements (what to validate)
```

**Guarantees:**
- Manual risk summary matches risk register
- SBOM reflects actual dependencies
- CE declaration consistent with risk assessment
- Changes propagate everywhere automatically

### 6. Professional Output

Typst produces publication-quality PDFs:
- Consistent branding and formatting
- Automatic table of contents
- Cross-references (risk IDs, page numbers)
- Professional risk matrices with color coding
- Ready for submission to notified bodies

---

## Consequences

### Positive

1. **Quality & Consistency**
   - Impossible to have invalid data in production
   - All documents use same data source
   - Professional, consistent formatting

2. **Speed & Efficiency**
   - Validation runs in <1 second (43 tests)
   - Full document build in ~2 seconds
   - No manual copy-paste between documents
   - SBOM auto-generated from dependencies

3. **Audit Readiness**
   - Complete git history of all changes
   - Validated data provably correct
   - Documents always in sync
   - Traceability to code/requirements

4. **Developer Experience**
   - Familiar git workflow
   - IDE auto-completion (via JSON Schema)
   - Inline validation errors
   - CI catches mistakes before merge

5. **Scalability**
   - Easy to add new risks/components
   - Reusable across product variants
   - Template for other compliance needs
   - Automated regression testing

### Negative

1. **Learning Curve**
   - Team needs to learn YAML, Git, Typst basics
   - Different mindset from Excel/Word
   - Initial setup time

   **Mitigation:** Documentation, examples, training sessions

2. **Tooling Requirements**
   - Need Python, Typst, Git installed
   - Devcontainer for consistent environment
   - CI/CD pipeline setup

   **Mitigation:** Devcontainer includes everything, one-click setup

3. **Non-Technical Stakeholder Access**
   - QA/compliance team may prefer Excel
   - Auditors expect Word/PDF

   **Mitigation:** 
   - Generate Excel from YAML if needed
   - Provide PDFs as primary output
   - Web interface possible for editing YAML

4. **Initial Migration Effort**
   - Convert existing Excel → YAML
   - Define schemas for current data
   - Set up validation rules

   **Mitigation:** One-time cost, huge ongoing benefits

---

## Alternatives Considered

### Alternative 1: Continue with Excel/Word

**Pros:**
- No change needed
- Familiar to all stakeholders
- Quick for small edits

**Cons:**
- ❌ No validation
- ❌ No automation
- ❌ Poor version control
- ❌ Manual maintenance burden
- ❌ Error-prone
- ❌ Doesn't scale

**Decision:** Rejected - problems outweigh familiarity benefits

### Alternative 2: LaTeX for Document Generation

**Pros:**
- Mature ecosystem
- Publication quality output
- Good for complex math/tables

**Cons:**
- ❌ Steeper learning curve than Typst
- ❌ Verbose syntax
- ❌ Slower compilation
- ❌ Complex setup (TeX distribution)

**Decision:** Rejected - Typst provides similar quality with better DX

### Alternative 3: Generate Documents → Excel

**Approach:** Keep Excel as output format, generate from YAML

```python
# Possible: Export validated data to Excel
def export_to_excel(risks: RiskRegister):
    df = pd.DataFrame([r.dict() for r in risks.risks])
    df.to_excel("risks.xlsx")
```

**Pros:**
- ✅ Stakeholders can view in familiar format
- ✅ Can import to other systems
- ✅ Validation still happens (YAML → Excel, not Excel → YAML)

**Cons:**
- ⚠️ Excel becomes read-only (generated artifact)
- ⚠️ Changes must be made in YAML

**Decision:** Possible complementary approach, not replacement
- Primary: YAML → PDF (for audits)
- Optional: YAML → Excel (for stakeholder review)

### Alternative 4: Dedicated Compliance Tool (e.g., Jama, Polarion)

**Pros:**
- Purpose-built for compliance
- Rich UI for non-technical users
- Built-in traceability

**Cons:**
- ❌ Expensive licensing
- ❌ Vendor lock-in
- ❌ Often poor API/integration
- ❌ Separate from code repository
- ❌ Less developer-friendly

**Decision:** Rejected - our approach is more flexible and integrated

### Alternative 5: Markdown + Pandoc

**Pros:**
- Simple, widely known
- Good for text-heavy docs
- Easy to edit

**Cons:**
- ❌ Limited styling control
- ❌ Poor table support
- ❌ Not designed for data-driven generation
- ❌ Complex template syntax

**Decision:** Rejected - Typst better for structured documents

---

## Implementation

### Project Structure

```
compliance-as-code/
├── schemas/                    # Pydantic validation (source of truth)
│   ├── risk_assessment.py     # Risk model schemas
│   ├── sbom.py                # SBOM schemas
│   └── generated-json-schemas/ # Auto-generated (for IDE tooling)
│
├── tests/                      # 43 validation tests
│   ├── test_risk_assessment_schema.py
│   └── test_sbom_schema.py
│
├── risk-assessment/
│   ├── model.yaml             # Framework (severity, probability, categories)
│   ├── risks.yaml             # Risk register (validated data)
│   └── risk-assessment.typ    # Template (generates PDF)
│
├── software-bill-of-materials/
│   ├── sbom_manual.yaml       # Manual components
│   ├── sbom_generated.yaml    # Auto-generated dependencies
│   ├── sbom.typ               # Template
│   └── scripts/generate_sbom.py  # Auto-extraction
│
├── manual/
│   └── manual.typ             # User manual template
│
├── ce-declaration/
│   └── ce.typ                 # CE declaration template
│
└── main.py                     # Integrated build tool
```

### Workflow

```bash
# Developer workflow
1. Edit YAML (e.g., add new risk to risks.yaml)
2. Validate: python3 main.py --validate-only
3. Build: python3 main.py --all
4. Review PDFs
5. Git commit + push

# CI/CD workflow (automatic)
1. Run validation: python3 main.py --validate-only
2. Run tests: pytest tests/ -v
3. Build artifacts: python3 main.py --all
4. Archive PDFs
5. ✅ Merge if all pass, ❌ reject if any fail
```

### Key Technologies

- **YAML:** Human-readable structured data
- **Pydantic v2:** Python schema validation with rich type system
- **Typst 0.12+:** Modern document compiler (alternative to LaTeX)
- **pytest:** Testing framework for validation
- **Git:** Version control and audit trail
- **GitHub Actions / GitLab CI:** Automated validation and builds

---

## Specific Benefits for CE / ISO Processes

### 1. IEC 62304 (Medical Software)
- ✅ Risk analysis traceable to requirements
- ✅ Software items linked to risks
- ✅ SOUP (SBOM) automatically maintained
- ✅ Verification that all risks are addressed

### 2. ISO 14971 (Risk Management)
- ✅ Enforced risk analysis process
- ✅ Residual risk evaluation automated
- ✅ Risk acceptability criteria validated
- ✅ Post-market surveillance data can update YAML

### 3. Cyber Resilience Act (CRA)
- ✅ SBOM required → auto-generated
- ✅ Vulnerability management → CI checks for known CVEs
- ✅ Secure by default → enforce controls in schema
- ✅ Incident response → risks link to monitoring

### 4. Technical File for CE Marking
- ✅ Consistent documentation package
- ✅ Proven up-to-date (git timestamps)
- ✅ Signatures digitally verifiable
- ✅ All cross-references valid

---

## Metrics for Success

After 6 months, measure:

- **Time to generate compliance package:** <5 minutes (vs. days)
- **Validation errors caught in CI:** >0 (was impossible before)
- **Documentation inconsistencies:** 0 (guaranteed by automation)
- **Audit findings related to documentation:** Reduction of 80%+
- **Developer satisfaction:** Survey shows preference over Excel

---

## Future Enhancements

### Potential Extensions

1. **Web UI for YAML editing**
   - For non-technical stakeholders
   - Still commits to Git in background
   - Validation in real-time

2. **Advanced CI Checks**
   ```python
   # Link risks to test coverage
   def test_all_critical_risks_have_tests():
       for risk in get_critical_risks():
           assert has_test_coverage(risk.id)
   
   # Enforce CRA requirements
   def test_cra_article_13_coverage():
       cra_risks = [r for r in risks if "Article 13" in r.cra_requirement]
       assert len(cra_risks) >= MINIMUM_CRA_RISKS
   ```

3. **Automatic Linking to Commits/Issues**
   ```python
   # Extract from git history
   git log --grep="R001" → find related commits
   gh issue list --search="R001" → find related issues
   ```

4. **Delta Reports**
   - "What changed since last audit?"
   - "New risks added this quarter"
   - Auto-generate management review materials

5. **Export to Other Formats**
   - YAML → Excel (for stakeholder review)
   - YAML → JSON (for API integration)
   - YAML → CycloneDX/SPDX (standard SBOM formats)

6. **Template Library**
   - Share schemas across projects
   - Company-wide risk categories
   - Reusable Typst components

---

## References

- **Typst Documentation:** https://typst.app/docs
- **Pydantic Validation:** https://docs.pydantic.dev
- **CRA Requirements:** EU Regulation 2022/0272
- **IEC 62304:** Medical device software lifecycle processes
- **ISO 14971:** Risk management for medical devices

---

## Conclusion

**Compliance as Code** transforms compliance documentation from error-prone manual work into validated, automated, version-controlled processes. The investment in setup (schemas, templates, CI) pays dividends through:

- **Quality:** Guaranteed data validity
- **Speed:** Automated generation and validation  
- **Confidence:** Cannot merge invalid compliance data
- **Traceability:** Full audit trail in Git
- **Integration:** Compliance checks alongside code review

For organizations pursuing CE marking, ISO certification, or CRA compliance, this approach **significantly reduces risk** of documentation errors while **improving efficiency** of compliance processes.

The future of compliance is **code**.
