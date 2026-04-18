# 01. What is GDR (General Decision Record)

> *Translated from Japanese using Claude (Anthropic).*

## 1. Overview

**GDR (General Decision Record)** is a derivative concept of [ADR (Architectural Decision Record)](https://iroirotool.com/platform/ja/knowledge/hosyu_unyou/adr.html). While ADR is a means of recording decisions related to software architecture, GDR is not limited to architecture — it provides a unified way to record all types of decisions within a project, including **specification design, UI design, operational policies, development processes, and business decisions**.

The scope implied by "General" **varies depending on the project and industry**. In software development, the focus tends to be on architecture / UI / policy, but in manufacturing, quality management and supply chain may be added, and in healthcare, clinical procedures and regulatory compliance may come into scope. The GDR framework itself does not depend on specific scope definitions — it can be applied to any domain simply by replacing the scope table.

## 2. Purpose

Same as ADR:
1. **Preserve the rationale behind decisions** — So that your future self and teammates can trace why a decision was made
2. **Enable reconsideration** — When circumstances change, you can review the original assumptions and update the decision
3. **Record alternatives** — By documenting options that were not adopted and the reasons why, you prevent the same discussions from recurring

## 3. Format

```markdown
**GDR-{PREFIX}-{number}: {Summary of the decision}**

- **status:** {Proposed | Approved | Implemented | Superseded}
- **scope:** {Comma-separated scope abbreviations}
- **decision:** What to do (or what not to do)
- **rationale:** Why this decision was reached (comparison with alternatives, trade-offs)
- **impact:** Specific effects of this decision
- **review trigger:** Under what circumstances should this decision be reconsidered
```

- `{PREFIX}` is a short identifier indicating the domain
- `{number}` is a sequential number within the PREFIX (3-digit zero-padded: 001, 002, ...)
- `scope` requires one or more values. Multiple values are comma-separated (e.g., `arch, pol`)
- `status` takes one of the following 4 values:

| status | Meaning |
|---|---|
| `Proposed` | Under proposal. Awaiting review and approval |
| `Approved` | Approved. Implementation may proceed |
| `Implemented` | Implemented. Reflected in code or configuration |
| `Superseded` | Superseded. Replaced by a new GDR |

When setting a status to `Superseded`, include the replacement GDR ID and link back from the replacement GDR as well (e.g., `Superseded by GDR-UI-003` / `Supersedes GDR-UI-001`)

## 4. scope and PREFIX

This section defines the two classification axes used in the GDR format (Section 3).

### 4.1. scope — Impact Area of the Decision

scope is a classification that indicates "what this decision affects." The GDR framework does not enforce a specific set of scopes. They are defined according to the project and industry.

Examples: `arch` (architecture), `spec` (functional specification), `ui` (UI/UX), `pol` (development process), `prod` (product direction), `perf` (performance), `meta` (GDR operations)

A single GDR may have multiple scopes (e.g., `arch, pol`).

Industry-specific scope lists → [01_SCOPE_GUIDE.md](/01_GDR/guide/01_SCOPE_GUIDE.md)

### 4.2. PREFIX — Domain Identifier

PREFIX is a short identifier used in the format `GDR-{PREFIX}-{number}` to indicate the domain. While scope represents "classification of impact areas," PREFIX uniquely identifies "which domain the decision belongs to."

Examples: `INFRA` (infrastructure), `UI` (UI/UX), `AD` (advertising/monetization), `META` (GDR operations)

Industry-specific PREFIX lists → [02_PREFIX_GUIDE.md](/01_GDR/guide/02_PREFIX_GUIDE.md)

## 5. Related Documents

| # | Document | Content |
|---|---|---|
| 02 | [02_AI_DRIVEN_GDR_BUILDUP.md](/01_GDR/02_AI_DRIVEN_GDR_BUILDUP.md) | AI-Driven GDR Build-Up (definition / cycle / principles) |
| G-01 | [01_SCOPE_GUIDE.md](/01_GDR/guide/01_SCOPE_GUIDE.md) | Scope guidelines (common + industry-specific) |
| G-02 | [02_PREFIX_GUIDE.md](/01_GDR/guide/02_PREFIX_GUIDE.md) | PREFIX guidelines (common + industry-specific) |
| G-03 | [03_FIRST_PROMPT_GUIDE.md](/01_GDR/guide/03_FIRST_PROMPT_GUIDE.md) | Localization first prompt guide |
| G-04 | [04_PROMPT_GUIDE.md](/01_GDR/guide/04_PROMPT_GUIDE.md) | Prompt guidelines (recommended prompt collection) |
| T1 | [T1_CONTEXT_DEFINITIONS.md](/01_GDR/templates/T1_CONTEXT_DEFINITIONS.md) | Context Definitions template |
| T2 | [T2_BUILDUP_RECORD.md](/01_GDR/templates/T2_BUILDUP_RECORD.md) | Build-Up record template |
