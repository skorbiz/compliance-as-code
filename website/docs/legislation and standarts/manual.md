---
title: Manual
description: User-facing security information and instructions required under the CRA.
tags:
  - cra
  - manual
  - documentation
  - security
  - compliance
---

The CRA requires products to ship with clear **information and instructions** for users, including security-relevant guidance
during both commissioning, operation, maintenance, and decommissioning.

:::info[Purpose of this page]
This page **collects the requirements a manual must satisfy** — from both the **CRA** and the **EU declaration of
conformity** — _before_ any actual manual is written. Treat it as the specification and checklist that the eventual manual is
authored against, not as the manual itself.
:::

## Manual content requirements (CRA Annex II)

The manual — or an internet address pointing to detailed instructions — must at minimum cover the following. Annex II point 8
is the source for the lifecycle instructions, including the commissioning and decommissioning sections.

| Requirement                                 | CRA reference (Annex II) | Notes                                                                             |
| ------------------------------------------- | ------------------------ | --------------------------------------------------------------------------------- |
| Manufacturer identity and contact details   | Point 1                  | Name, registered trade name/mark, and a postal/email/digital contact.             |
| Single point of contact for vulnerabilities | Point 2                  | Where users can report and receive information about vulnerabilities.             |
| Unique product identification               | Point 3                  | Name, type, and any info enabling unique identification of the product.           |
| Intended purpose and security properties    | Point 4                  | Including essential functionalities and security properties.                      |
| Known/foreseeable risks and misuse          | Point 5                  | Circumstances that may lead to significant cybersecurity risks.                   |
| Address of the EU declaration of conformity | Point 6                  | Internet address where the EU declaration of conformity can be accessed.          |
| Support period and security-update end date | Point 7                  | Type of technical security support and the date until which updates are provided. |
| **Secure commissioning instructions**       | Point 8(a)               | Measures during **initial commissioning** and throughout the product lifetime.    |
| Effect of product changes on data security  | Point 8(b)               | How changes to the product can affect the security of data.                       |
| Installing security-relevant updates        | Point 8(c)               | How security updates can be installed.                                            |
| **Secure decommissioning instructions**     | Point 8(d)               | **Secure decommissioning**, including how user data can be securely removed.      |
| Turning off automatic updates               | Point 8(e)               | How the default automatic-update setting can be disabled, where applicable.       |
| Integration guidance                        | Point 8(f)               | Where the product is intended for integration into other products.                |
| SBOM availability                           | Point 9                  | Where the SBOM can be accessed, if the manufacturer chooses to make it available. |

:::tip[Commissioning and decommissioning are mandatory]
Both a **commissioning** section (Annex II point 8(a)) and a **decommissioning** section (Annex II point 8(d)) are required.
The decommissioning section must also explain how user data can be securely removed.
:::

## EU declaration of conformity requirements

The manual must reference where the **EU declaration of conformity** can be accessed (Annex II point 6). The declaration
itself is a separate document whose required contents are defined in the CRA's declaration-of-conformity annex, and it must be
kept consistent with the manual. Capture those declaration requirements here as they are confirmed.
