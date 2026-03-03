---
title: Overview
slug: /
---

# Compliance Documentation as Code

This site is a minimal web companion to the Typst-generated PDF documents.

The goal is to show one source of truth in YAML feeding more than one document type:

- Typst PDFs for formal compliance artifacts
- Docusaurus pages for easy browsing and linking in the browser

## What Is Generated

- [Risk Model (Generated)](generated/risk-model)

The generated page is built from:

- `model/risk_model.yaml`
- `model/risks.yaml`

## Compare the Output Types

- [Typst vs Docusaurus](typst-vs-docusaurus)

## Regenerate This Site Data

From repository root:

```bash
uv run main.py --web
```
