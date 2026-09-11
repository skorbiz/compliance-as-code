
## Ruff notes to be turned into something usefull at some point.

Create CRA / ISO documnet with strift references and paraphrases for easy understanding and verification.

lately i have had the problem that i talk to a lot of people about the probelm and they will make a claim about what ghe cra law says. But its really hard for me to ddistinquish what eople think it says, what it actually says and what people just suggest to to be compliant. So lately i have been reading through the law (and standarts) and made a small document withs parafrases ceirtian articels and sections with a specific reference to where that statement comes from..... right now its just in a markdown document - but i would like to treat this as code as well so i cluld use it a bit more generically..... i could ofcource create a new yaml format but i was wondering if there were other tools i should be aware of. Like bibtex for instance - but bibtex is more geared towards handling full reference instead of this very specifix reference with a parafrasi.


“What proposition am I making, exactly which part of an authoritative source supports it, and is this proposition a requirement, an interpretation, guidance, or our own implementation decision?”

Want to find a good balance between lightweight documentation and comprehensive compliance management:
OSCAL is considerably more elaborate. You could easily turn your nice lightweight solution into a miniature GRC platform that nobody on the team wants to edit.

Your instinct to treat the statement itself as structured data—not just the document containing it—is the useful distinction here. I’d separate “what the source says,” “how we interpret it,” and “what we choose to do,” then let documents be generated views of that graph.


---

BibTeX/Hayagriva/CSL are useful for answering:
“What document am I citing?”

----

For EU legislation, ELI—the European Legislation Identifier—is particularly interesting. It exists specifically to give legislation stable, machine-readable identifiers, and EUR-Lex is progressively supporting identifiers down to subdivisions such as individual articles.

For example, EUR-Lex supports URI structures along the lines of:
.../eli/reg/.../art_14/oj


----

SOURCE
  ↓ supports
NORMATIVE CLAIM
  ↓ interpreted-as
INTERPRETATION
  ↓ satisfied-by
IMPLEMENTATION / CONTROL
  ↓ verified-by
EVIDENCE / TEST

That gives you a really powerful property: you stop mixing law with engineering choices.


---

That gives you a really powerful property: you stop mixing law with engineering choices.

Imagine someone says:

“CRA requires us to rotate all service passwords every 90 days.”

You could search your compliance repository and discover:

statement: Service credentials must be rotated every 90 days.
classification: implementation
derived_from:
  - security-control-credentials-004

while that control says:

statement: Credentials must be protected against unauthorized access.
classification: requirement
source:
  document: some-standard
  clause: "..."


---

  NIST OSCAL.

OSCAL is explicitly designed around representing compliance information as machine-readable XML/JSON/YAML instead of Word/Excel documents. Its models cover control catalogs, profiles, implementations, assessment plans/results and risks.

Even more interesting for you: OSCAL now has a Control Mapping model intended to describe relationships between requirements from regulations, standards, frameworks and guidelines. It supports relationships such as equal-to, equivalent-to, subset-of, superset-of, and intersects-with.

And OSCAL explicitly supports links to external laws/regulations and internal back-matter resources.

I would definitely read OSCAL.

But I wouldn't necessarily adopt OSCAL as your internal format.

---

There's also Compliance Trestle, which is almost eerily similar philosophically to what you're building: compliance artifacts in Git, schema validation, YAML/JSON, Markdown authoring, CI/CD and document generation. It uses OSCAL underneath.

It's worth investigating just to see which problems they've already encountered.

---

def test_every_requirement_has_source():
    ...

def test_law_claims_have_precise_locator():
    ...

def test_every_risk_has_at_least_one_requirement_or_rationale():
    ...

def test_claim_sources_still_reference_current_standard_revision():
    ...

And Docusaurus can provide filters:

[ Law ] [ Standards ] [ Guidance ] [ Internal decisions ]

CRA
 ├─ Article 10
 │   ├─ 4 direct requirements
 │   ├─ 2 interpretations
 │   └─ 7 controls implementing them

 ---

 Testing and integration with small LLM models. Could e.g. test

 def test_implementation_decisions_do_not_claim_law_as_authority():
    ...

---

You have effectively created a tiny knowledge graph, but YAML + IDs is perfectly sufficient; you don't need Neo4j or RDF.
with stable IDs linking everything together.

Keep Pydantic/YAML as your native format. Borrow ELI's identifiers, OSCAL's control/mapping concepts, and bibliography tooling such as Hayagriva for presentation. That gives you the benefits of existing standards without turning a small-team compliance-as-code repository into a heavyweight compliance product.

