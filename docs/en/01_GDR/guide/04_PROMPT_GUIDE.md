# 04. Prompt Guidelines

> *Translated from Japanese using Claude (Anthropic).*

> A collection of recommended prompts for efficiently running the AI-Driven GDR Build-Up cycle.
> Prerequisites: [02. AI-Driven GDR Build-Up](/01_GDR/02_AI_DRIVEN_GDR_BUILDUP.md) / [03. Localization First Prompt](/01_GDR/guide/03_FIRST_PROMPT_GUIDE.md)

## 1. Requirement Communication

The starting point of the cycle. Communicate issues or requirements to AI and initiate GDR structuring.

| Prompt | Effect |
|---|---|
| `[description of issue/requirement]` | Communicate the issue in natural language. AI structures it as a GDR |
| `improvement proposal: [title]` | Generate an improvement proposal document in a 3-part structure: GDR → execution plan → retrospective |
| `[issue]. Convert to GDR` | Explicitly convert a verbal-level issue into GDR format |
| `bug report: [content]` | Generate a report document organizing the bug details |

## 2. Structuring / Deep Dive

Deepen the analysis to improve decision accuracy against AI's initial proposal.

| Prompt | Effect |
|---|---|
| `show alternatives` | Request a comparison table including rejected options and their reasons |
| `what's the scope?` | Have AI clarify the impact areas of the decision |
| `be specific about review triggers` | Have AI refine abstract triggers into numerical thresholds or specific conditions |
| `quantify it` | Request measured data or numerical evidence |
| `what's the impact scope?` | Have AI enumerate affected files, modules, and teams |
| `compare [option A] and [option B]` | Have AI organize trade-offs between specific alternatives |

## 3. Review

Verify the quality of proposals and documents, and prune over-engineering.

| Prompt | Effect |
|---|---|
| `review: [filename]` | Generate a review document for the target file |
| `incorporate review: [filename]` | Incorporate review content into the original file and delete the review document |
| `isn't this overkill?` | Have AI compress the proposal from an ROI perspective |
| `optimize` | Trigger to prune over-engineering. Request the solution that achieves the goal with minimal means |
| `edit according to guidelines` | Have AI fix missing required GDR format fields or format deviations |

## 4. Implementation

Translate GDRs into concrete code, configuration, and documents.

| Prompt | Effect |
|---|---|
| `implement it` | Reflect the preceding proposal/GDR into implementation |
| `break into tasks` | Have AI decompose the GDR into executable tasks (phases/checklists) |
| `renumber` | Have AI align numbering across filenames, headings, and cross-links |
| `commit` | Have AI commit the changes |

## 5. Retrospective / Verification

Confirmation at the end of a cycle and knowledge consolidation.

| Prompt | Effect |
|---|---|
| `retrospective` | Generate the retrospective section (quantitative summary, trends, notes for next time) from T2 |
| `consistency check` | Have AI verify consistency of links, numbering, and paths across files |
| `organize document consistency` | Detect inconsistencies and execute fixes |
| `re-edit [filename]` | Have AI rewrite the document according to current template structure and operational rules |

---

## 6. Context Shortcut Keywords (CLAUDE.md Integration)

By defining **shortcut keywords** in CLAUDE.md (the AI agent instruction file at the project root), you can trigger standard operations with a single word. Keywords are loaded by AI at session start, so there is no need to explain them in prompts each time.

### Defined Keywords

| Keyword | Format | Behavior |
|---|---|---|
| **improvement proposal** | `improvement proposal: [title]` | Generate an improvement proposal document following the T2_BUILDUP_RECORD.md template structure |
| **review** | `review: [filename]` | Generate a review document as `{filename}_reviewed` at the same location as the target file |
| **incorporate review** | `incorporate review: [filename]` | Review, organize, and incorporate the `_reviewed` file content into the original file, then delete the `_reviewed` file |
| **bug report** | `bug report: [filename]` | Create a bug report document organizing the bug details under `documents/bug_fix_report/` |

### How It Works

- Define keywords and their behaviors in the `context shortcut keywords` section
- AI **loads CLAUDE.md at session start**, so the keyword alone conveys the intent
- Project-specific keywords can be freely added

### Customization Examples

Add keywords tailored to the project:

```markdown
## Context Shortcut Keywords

5. **"release notes[:|;][version]":** Compile the change history for the target version in CHANGELOG.md.
6. **"design discussion[:|;][topic]":** Generate a design review memo including alternatives and trade-offs.
```

---

## 7. Usage Tips

1. **Keep it short** — Effective prompts are short. A single phrase like `implement it`, `commit`, `optimize` is sufficient
2. **Combine them** — Run the cycle like `improvement proposal: X` → `isn't this overkill?` → `implement it` → `commit`
3. **When in doubt, ask** — When lacking decision material, draw out information with `show alternatives` or `quantify it` before deciding
4. **Retroactive is fine** — GDRs crystallize during dialogue. There's no need to write the perfect prompt from the start
5. **Don't mix documents and implementation** — Don't request "document creation" and "code implementation" in a single instruction. Create and review documents first, gain consensus, then proceed to implementation. Mixing them causes implementation to proceed with ambiguous decisions, leading to costly rework
