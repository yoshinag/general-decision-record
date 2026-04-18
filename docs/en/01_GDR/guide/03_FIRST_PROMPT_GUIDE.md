# 03. Localization First Prompt Guide

> *Translated from Japanese using Claude (Anthropic).*

> How to phrase the "first words" when introducing the GDR framework to a project.
> Prerequisites: [01. What is GDR](/01_GDR/01_GENERAL_DECISION_RECORD.md) / [02. AI-Driven GDR Build-Up](/01_GDR/02_AI_DRIVEN_GDR_BUILDUP.md)

## 1. What is Localization

The GDR framework itself is a generic design that does not depend on specific scope or PREFIX definitions. **Localization** refers to the process of customizing this generic framework to suit a specific project.

Specifically, the following are determined:

- The **scopes** (impact area classifications) to be used in the project
- The **PREFIXes** (domain identifiers) to be used in the project
- The **output location** (directory structure) for GDRs
- Operational settings such as **shortcut keywords**

These decisions themselves become the first GDR (e.g., `GDR-META-001`).

## 2. Recommended Prompt

```
Introduce GDR. Create the Context Definitions based on the following project information.

Project name: {project name}
Domain: {software / manufacturing / healthcare / finance / other}
Overview: {1-3 sentences describing the project}
Main concerns: {e.g., API design, screen UI, operational rules, cost management}
GDR output location: {e.g., documents/decisions/ documents/kaizen/}

Shortcut keywords:
  "improvement proposal[:|;][title]": Generate an improvement proposal document following the T2 template structure
  "review[:|;][filename]": Generate a review document as filename_reviewed at the same location
  "incorporate review[:|;][filename]": Incorporate the _reviewed content into the original file and delete the _reviewed file
  "bug report[:|;][filename]": Create a bug report under {output location}/bug_fix_report/
  {Add project-specific keywords}
```

This prompt causes AI to:

- Generate a Context Definitions document based on the [T1_CONTEXT_DEFINITIONS.md](/01_GDR/templates/T1_CONTEXT_DEFINITIONS.md) template
- Reference the [scope guide](/01_GDR/guide/01_SCOPE_GUIDE.md) / [PREFIX guide](/01_GDR/guide/02_PREFIX_GUIDE.md) to propose suitable scopes and PREFIXes for the project
- Propose the output directory structure
- Generate the `context shortcut keywords` section for CLAUDE.md

### 2.1. GDR Output Location Format

Specify directories in the same manner as the `mkdir` command. Multiple directories can be specified with spaces, and brace expansion is also supported.

```
# Space-separated for multiple directories
GDR output location: documents/decisions/ documents/kaizen/ documents/bug_fix_report/

# Brace expansion to group common prefixes
GDR output location: documents/{decisions,kaizen,bug_fix_report}/
```

AI will infer the purpose of each specified directory and organize them into an output location table for the Context Definitions.

## 3. Prompt Components

| Element | Required | Purpose | Tips |
|---|---|---|---|
| Project name | ○ | GDR identification | Does not need to be the formal name |
| Domain | ○ | Reference industry-specific guides | Comma-separate if spanning multiple domains |
| Overview | ○ | Context for scope/PREFIX proposals | 1-3 sentences describing "what the project does" |
| Main concerns | − | Prioritizing scopes | List areas with frequent decision-making |
| GDR output location | − | Determining directory structure | Multiple directories via spaces or brace expansion. AI proposes if omitted |
| Shortcut keywords | − | Generating CLAUDE.md shortcut keywords | Default 4 types (improvement proposal, review, incorporate review, bug report) + project-specific additions |
| Existing constraints | − | Improving proposal accuracy | Monorepo structure, existing ADRs, etc. |

## 4. Industry-Specific Examples

### 4.1. Web Application Development

```
Introduce GDR. Create the Context Definitions based on the following project information.

Project name: TaskFlow
Domain: Software
Overview: A team-oriented task management SaaS. React + Node.js + PostgreSQL.
Main concerns: API design, authentication/authorization, UI component design, deployment strategy
GDR output location: documents/{decisions,kaizen}/

Shortcut keywords:
  "improvement proposal[:|;][title]": Generate an improvement proposal document following the T2 template structure
  "review[:|;][filename]": Generate a review document as filename_reviewed at the same location
  "incorporate review[:|;][filename]": Incorporate the _reviewed content into the original file and delete the _reviewed file
  "bug report[:|;][filename]": Create a bug report under documents/bug_fix_report/
  "API spec[:|;][endpoint]": Generate an API specification document in OpenAPI format
  "migration[:|;][table name]": Generate a DB migration file
```

### 4.2. Mobile App Development

```
Introduce GDR. Create the Context Definitions based on the following project information.

Project name: HealthMate
Domain: Software, Healthcare
Overview: A patient-facing health records app. Built with Flutter. Integrates with HL7 FHIR-compliant APIs.
Main concerns: Data privacy, regulatory compliance, offline sync, UI/UX
GDR output location: documents/gdr/{decisions,compliance}/

Shortcut keywords:
  "improvement proposal[:|;][title]": Generate an improvement proposal document following the T2 template structure
  "review[:|;][filename]": Generate a review document as filename_reviewed at the same location
  "incorporate review[:|;][filename]": Incorporate the _reviewed content into the original file and delete the _reviewed file
  "bug report[:|;][filename]": Create a bug report under documents/gdr/bug_fix_report/
  "regulatory check[:|;][feature name]": Generate a compliance checklist against applicable regulatory requirements
```

### 4.3. Manufacturing Quality Control System

```
Introduce GDR. Create the Context Definitions based on the following project information.

Project name: QualityHub
Domain: Manufacturing
Overview: A system for managing factory inspection processes. Records inspection results, tracks defect rates, and manages corrective actions.
Main concerns: Inspection flow, quality standards, traceability, report generation
GDR output location: documents/decisions/ documents/quality_reports/

Shortcut keywords:
  "improvement proposal[:|;][title]": Generate an improvement proposal document following the T2 template structure
  "review[:|;][filename]": Generate a review document as filename_reviewed at the same location
  "incorporate review[:|;][filename]": Incorporate the _reviewed content into the original file and delete the _reviewed file
  "bug report[:|;][filename]": Create a bug report under documents/bug_fix_report/
  "inspection report[:|;][process name]": Generate an inspection result report template
  "corrective action[:|;][defect ID]": Generate a corrective action record document
```

### 4.4. E-Commerce Site

```
Introduce GDR. Create the Context Definitions based on the following project information.

Project name: FreshMarket
Domain: E-Commerce / Retail
Overview: A farm-to-consumer fresh food e-commerce platform. Features inventory management, delivery route optimization, and subscription functionality.
Main concerns: Inventory management, payment, delivery logic, product catalog design, promotions
GDR output location: documents/{decisions,kaizen,bug_fix_report}/

Shortcut keywords:
  "improvement proposal[:|;][title]": Generate an improvement proposal document following the T2 template structure
  "review[:|;][filename]": Generate a review document as filename_reviewed at the same location
  "incorporate review[:|;][filename]": Incorporate the _reviewed content into the original file and delete the _reviewed file
  "bug report[:|;][filename]": Create a bug report under documents/bug_fix_report/
  "promotion plan[:|;][campaign name]": Generate a promotional campaign plan document
  "inventory alert[:|;][product category]": Generate an inventory status summary report
```

## 5. Anti-Patterns

| Pattern | Problem | Improvement |
|---|---|---|
| Defining all scopes and PREFIXes yourself before passing them | Fails to leverage AI's structuring capability. Tends toward over-definition | Pass only the overview and concerns, and let AI propose |
| Writing project details in long text | AI loses focus due to information overload | Keep to 1-3 sentence overview + keyword listing of concerns |
| Not specifying the domain | Cannot reference industry-specific guides, resulting in overly generic proposals | State the domain in a single word |
| Aiming for perfection from the start | Contradicts the build-up philosophy. Progress stalls | It's fine to be rough — start the dialogue. Refine later |
