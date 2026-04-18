# T1. Context Definitions Template

> *Translated from Japanese using Claude (Anthropic).*

> Replace `{...}` placeholders when using this template.

## 1. Project Information

Project: {project name}
Domain: {software / manufacturing / healthcare / finance / other}

## 2. Scope Definitions

| scope | Abbreviation | Target |
|---|---|---|
| `architecture` | `arch` | System structure, data flow, layer boundaries, DB schema |
| `spec` | `spec` | Functional specifications, data models, API contracts |
| `ui` | `ui` | Visual design, layout, interaction |
| `policy` | `pol` | Development process, coding standards, release policy |
| `product` | `prod` | Product direction, naming, target users, revenue model |
| `performance` | `perf` | Performance goals, optimization policy, measurement strategy |
| `meta` | `meta` | Changes to GDR operational rules themselves, document structure |
| | | {Add project-specific scopes} |

## 3. PREFIX Definitions

| PREFIX | Domain | Representative Scopes | Usage |
|---|---|---|---|
| INFRA | Infrastructure | `arch`, `pol` | Error handling, retry strategies, common infrastructure |
| PERF | Performance | `perf`, `arch` | Response time targets, optimization policies, measurement strategies |
| LOG | Logging / Audit | `arch`, `pol` | Log persistence, rotation, audit trails |
| APP | App / Product Identity | `prod` | Identifiers, naming, versioning |
| META | Meta (GDR Operations) | `meta` | Changes to GDR operational rules themselves |
| | | | {Add project-specific PREFIXes} |
