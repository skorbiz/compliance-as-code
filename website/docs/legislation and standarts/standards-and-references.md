---
title: Standards and References
description: Reference list of the cybersecurity standards and frameworks relevant to the Cyber Resilience Act, plus links to the CRA legal text.
tags:
  - cra
  - standards
  - references
  - iec 62443
  - iso 27001
  - nist
  - compliance
---

This page collects the important standards and frameworks that come up when discussing CRA compliance.

## Standards and frameworks

### NIST Cybersecurity Framework (CSF) 2.0

| Aspect           | Summary                                                                                                                       |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **What**         | Voluntary framework organising cybersecurity outcomes into the functions Govern, Identify, Protect, Detect, Respond, Recover. |
| **CRA relation** | Provides a common vocabulary and outcome structure that can be mapped to CRA essential requirements; not itself a CRA basis.  |
| **Where**        | [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)                                                           |

### CIS Controls (CIS Critical Security Controls)

| Aspect           | Summary                                                                                                   |
| ---------------- | --------------------------------------------------------------------------------------------------------- |
| **What**         | Prioritised, prescriptive set of security safeguards grouped into implementation groups.                  |
| **CRA relation** | Concrete, actionable controls that can be used to satisfy CRA technical expectations.                     |
| **Notes**        | Practical starting point for baseline hardening; maps to other frameworks such as NIST CSF and ISO 27001. |
| **Where**        | [CIS Controls](https://www.cisecurity.org/controls)                                                       |

### ISO/IEC 27001

| Aspect           | Summary                                                                                     |
| ---------------- | ------------------------------------------------------------------------------------------- |
| **What**         | Requirements for an Information Security Management System (ISMS).                          |
| **CRA relation** | Organisational management-system evidence supporting CRA process and lifecycle obligations. |
| **Notes**        | Certifiable; often paired with the ISO 27002 control set.                                   |
| **Where**        | [ISO/IEC 27001](https://www.iso.org/standard/27001)                                         |

### ISO/IEC 27005

| Aspect           | Summary                                                                  |
| ---------------- | ------------------------------------------------------------------------ |
| **What**         | Guidance on information security risk management within an ISMS context. |
| **CRA relation** | Supports the risk-management methodology behind the CRA risk assessment. |
| **Notes**        | Complements ISO 27001; methodology-focused rather than control-focused.  |
| **Where**        | [ISO/IEC 27005](https://www.iso.org/standard/80585.html)                 |

### ISO 31000

| Aspect           | Summary                                                                   |
| ---------------- | ------------------------------------------------------------------------- |
| **What**         | Principles and generic guidelines on risk management (organisation-wide). |
| **CRA relation** | General risk-management framing that underpins a risk-based CRA approach. |
| **Notes**        | Not security-specific; provides overarching risk vocabulary and process.  |
| **Where**        | [ISO 31000](https://www.iso.org/standard/65694.html)                      |

### IEC 62443 (series)

The **IEC 62443** series covers security for Industrial Automation and Control Systems (IACS). It is split into multiple parts; the parts most relevant to CRA discussions are listed individually below.

:::info
Individual IEC 62443 parts are published separately. Use the [IEC Webstore](https://webstore.iec.ch/searchform&q=62443) to locate and obtain each part.
:::

#### IEC 62443-1-1 — Terminology, concepts and models

| Aspect           | Summary                                                                                              |
| ---------------- | ---------------------------------------------------------------------------------------------------- |
| **What**         | Defines the terminology, concepts, and reference models (zones, conduits, levels) for IACS security. |
| **CRA relation** | Often used as the basis for the network architecture and the risk assessment.                        |
| **Notes**        |                                            |

#### IEC 62443-3-3 — System security requirements and security levels

| Aspect           | Summary                                                                                                   |
| ---------------- | --------------------------------------------------------------------------------------------------------- |
| **What**         | System-level security requirements grouped by security level, including authentication and authorisation. |
| **CRA relation** | Maps system technical requirements to CRA essential requirements at the system level.                     |
| **Notes**        | The 62443-3 parts are relatively concise on authentication and authorisation.                             |

#### IEC 62443-4-1 — Secure product development lifecycle

| Aspect           | Summary                                                                                                                        |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **What**         | Requirements for a secure product development lifecycle for IACS components.                                                   |
| **CRA relation** | Directly supports the CRA lifecycle and secure-by-design obligations.                                                          |
| **Notes**        | According to 62443s classification of level 1, 2 and critical (vpn, dns and such) systems this is where jensen machine belongs |

#### IEC 62443-4-2 — Technical security requirements for components

| Aspect           | Summary                                                                            |
| ---------------- | ---------------------------------------------------------------------------------- |
| **What**         | Component-level technical security requirements aligned to security levels.        |
| **CRA relation** | Component technical requirements that can be mapped to CRA essential requirements. |
| **Notes**        | Complements 62443-3-3 at the component level.                                      |

### EN 40000 series (harmonised CRA standards, draft)

:::warning
The **EN 40000** numbering is provisional. The harmonised European standards for the CRA are still under development by CEN/CENELEC; final numbering, scope, and structure may differ. Treat this entry as a placeholder until the standards are published.
:::

| Aspect           | Summary                                                                                                                                                                                                                              |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **What**         | Intended harmonised European standard(s) describing how to meet CRA requirements.                                                                                                                                                    |
| **CRA relation** | Once published and cited in the Official Journal, conformance would give a presumption of conformity with the CRA.                                                                                                                   |
| **Notes**        | Standard focuses on technical compliance of CRA, but formal measures like how to treat the risk assessment, how to do incident reporting and so forth.                                                                               |

### prEN 50742 — Protection of machinery against corruption

**prEN 50742** defines two alternative approaches for protecting machinery against corruption. This is the standard behind the "Approach A vs Approach B" distinction in CRA discussions.

| Aspect           | Summary                                                                                                                                                                                                                                                                                                           |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **What**         | Defines two alternative approaches for protecting machinery against corruption. **Approach A** is a machinery-specific risk-assessment approach. **Approach B** lets manufacturers use the IEC 62443 framework, including its security levels and defined system, component, and secure-development requirements. |
| **CRA relation** | Provides two routes to demonstrate the machinery cybersecurity protection expected under the CRA.                                                                                                                                                                                                                 |
| **Notes**        | We leans towards **Approach B** — adopting the IEC 62443 security levels and requirements rather than a purely machinery-specific risk assessment. Draft; still under development, details may change.                                                                                                       |
| **Where**        | Track via [CEN/CENELEC](https://www.cencenelec.eu/) (JTC 13, cybersecurity).                                                                                                                                                                                                                                      |

## CRA legal text

The Cyber Resilience Act is **Regulation (EU) 2024/2847** of the European Parliament and of the Council.

| Aspect            | Detail                                                                                                                                      |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **Instrument**    | Regulation (EU) 2024/2847                                                                                                                   |
| **Scope**         | Cybersecurity requirements for products with digital elements across their lifecycle.                                                       |
| **Official text** | [EUR-Lex — Regulation (EU) 2024/2847](https://eur-lex.europa.eu/eli/reg/2024/2847/oj)                                                       |
