---
title: YAML Model Generation and Import Ideas
slug: /yaml-model-generation-import-ideas
---

# Goal

List practical options to generate or import YAML-based models into Docusaurus docs.

# Options

## 1. Python-native pipeline (current approach)

Use Python scripts to read YAML models and generate Markdown/MDX files under `website/docs/generated`.

Pros:
- Reuses current implementation and team skills.
- Easy to add validation and pre-processing logic.
- Simple to test in CI with Python tooling.

Cons:
- Not scalable for large models or frequent updates.
- Adds a pre-build step before Docusaurus runs.
- Logic is outside the Docusaurus build lifecycle.

## 2. Python + Jinja templates

Keep Python for YAML parsing/validation, but render docs with Jinja templates.

Pros:
- Cleaner separation between data logic and document layout.
- Easier to maintain repeated sections/partials.
- Better control over output format consistency.

Cons:
- Another templating layer to learn and maintain.
- Complex templates can become hard to debug.

## 3. Docusaurus-native plugin (JavaScript/TypeScript)

Create a custom Docusaurus plugin that loads YAML during the site build and injects docs/pages.

Pros:
- Fully integrated with Docusaurus lifecycle.
- No separate pre-generation step required.
- Better path for interactive/route-based docs generation.

Cons:
- Requires JavaScript/TypeScript plugin code.
- More initial setup than script-based generation.
