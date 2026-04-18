# 02. AI-Driven GDR Build-Up

> *Translated from Japanese using Claude (Anthropic).*

> Prerequisite: [01. What is GDR (General Decision Record)](/01_GDR/01_GENERAL_DECISION_RECORD.md)

## 1. Definition

**AI-Driven GDR Build-Up** (hereafter "GDR Build-Up") is a development process in which GDRs (General Decision Records) are iteratively accumulated through dialogue with AI, driving the project forward.

It is neither the traditional "design → implement → document" waterfall approach, nor the "write tests first → implement" approach like TDD. **Decisions crystallize during dialogue, become established as GDRs, and flow into implementation** — this accumulation cycle itself is the methodology.

## 2. Comparison with Conventional Methods

| Method | Starting Point | Timing of Decision Recording | Compatibility with AI |
|---|---|---|---|
| Waterfall | Design documents | Created in advance during design phase | Low (requires writing lengthy documents upfront) |
| TDD | Tests | Implicitly during test creation | Medium (test generation is possible but decision rationale is not preserved) |
| Agile with ADR | Stories | Retroactively recorded after implementation | Medium (prone to forgotten records) |
| **GDR Build-Up** | **Dialogue** | **Crystallized in real-time during dialogue** | **High (AI structures decisions and converts them to GDRs on the spot)** |

### 2.1. Why Not Call It "GDR-Driven Development"?

Following the naming convention of TDD (Test-Driven Development), "GDR-Driven Development" might seem natural. However, "Driven" implies a cycle where **GDRs are written first, and implementation is done to satisfy them**. The reality is different. GDRs crystallize retroactively during dialogue — they are not written before development begins. An initial proposal may be over-engineered and then compressed by a single human remark. A bug found during implementation may cause a GDR to be rewritten. The term that accurately represents this process of "decisions accumulating through dialogue and implementation" is not "Driven" but "Build-Up."

### 2.2. The Role of AI-Driven

It is not the GDR that drives development, but **AI**. **AI-Driven GDR Build-Up** captures this entire picture in one phrase. AI drives development (code generation, design proposals, implementation, verification), and the decisions that emerge in the process accumulate as GDRs. The two are inseparable — removing GDR from AI-driven development causes decisions to evaporate, and removing AI-driven from GDR turns it into mere documentation work.

## 3. Expected Benefits

### 3.1. Core Benefits

1. **Prevent decision evaporation** — Decisions made verbally or in chat no longer disappear without being recorded. Dialogue is directly persisted as GDRs
2. **Eliminate personal dependency** — Because "why things are the way they are" remains in GDRs, decisions can be traced even when team members change. AI can also reference past GDRs to make consistent proposals
3. **Accelerate decision-making** — AI structures alternatives, trade-offs, and impact scope, so humans can focus on "choosing." AI handles gathering and organizing the information needed for decisions
4. **Early detection of over-engineering** — When a human simply responds "optimize" to an AI proposal, low-ROI measures are pruned. Since decision rationale is quantified, debates about whether something is excessive become objective
5. **Systematize reconsideration** — Because each GDR has explicit "review triggers," decisions that should be revisited are automatically identified when circumstances change. Reconsideration triggers depend on documentation, not human memory
6. **Accelerate onboarding** — New team members can follow the project's decision history through GDR_INDEX. Instead of asking "why this design," they can simply read the GDR

### 3.2. Deterrent Effects Against Known AI Failure Modes

AI has several named failure modes. Each mechanism of GDR Build-Up provides deterrent effects against them:

| Failure Mode | Description | GDR Build-Up Deterrent | Effect |
|---|---|---|---|
| **Hallucination** | Generates plausible but false information | The "quantification" principle of GDR incorporates measurement data from actual code as evidence. Unsubstantiated claims are exposed in the GDR format's "rationale" field | ◎ |
| **Context loss** | Forgets early context in long conversations | GDR persists decisions, so past decisions can be referenced even when dialogue is interrupted. Consistency is maintained across sessions | ◎ |
| **Sycophancy** | Excessively agrees with the user and fails to point out problems | The "presentation of alternatives" and "review triggers" in GDR structurally require counterarguments and reservations. Documenting "why not" mitigates conformity pressure | ○ |
| **Over-engineering** | Proposes unnecessarily complex solutions | A single human remark of "optimize" triggers ROI-based compression. GDR quantification objectively visualizes excess | ◎ |
| **Contradiction generation** | Generates new output that contradicts past output | Past GDRs are persisted, enabling consistency checks against new proposals. AI can also reference past GDRs to maintain consistency | ◎ |
| **Scope creep** | Adds unrequested features or changes | The GDR "impact" field explicitly states the scope of changes, and deviations can be detected during review. Phase separation delineates scope | ○ |
| **Overconfidence** | States uncertain decisions definitively | The GDR "review trigger" explicitly asks "when might this decision break down." There is a structural force that converts assertions into reservations | ○ |
| **Repetition loops** | Repeats the same errors or proposals | Past decisions are accumulated in GDR_INDEX, enabling detection of recurring discussions. You can reference "already decided in GDR-XXX-NNN" | ◎ |

**Legend:** ◎ Strong structural deterrent effect / ○ Effective when combined with review cycles

### 3.3. Disadvantages and Considerations

GDR Build-Up is not a silver bullet. Here are the costs and trade-offs to be aware of when adopting it:

| Disadvantage | Description | Mitigation |
|---|---|---|
| **Increased token consumption** | Token usage in AI interactions increases due to GDR structuring, enumeration of alternatives, and referencing past GDRs. This is especially notable when including many past GDRs in context | Limit referenced GDRs to the minimum necessary. Use summaries and indexes to avoid loading full texts |
| **Document management overhead** | As GDRs accumulate, maintaining status management, cross-links, and numbering consistency becomes more labor-intensive | Delegate consistency checking to AI (`consistency check` prompt). Periodically archive Superseded GDRs |
| **Excessive formalization** | Trying to write a GDR for every small decision can make formality the goal itself, slowing development velocity | Agree as a team on the granularity of decisions that warrant GDRs. Obviously self-evident decisions should not become GDRs |
| **AI dependency risk** | The process is designed with AI as a premise, making it harder to operate in situations where AI is unavailable (outages, costs, regulations) | The GDR format and principles themselves can be operated by humans alone. AI is merely an efficiency tool, not a requirement |
| **Learning cost** | There are many concepts the entire team needs to understand: scope / PREFIX / templates / shortcut keywords, etc. | Start with the minimum configuration (format + cycle) and introduce guides and templates incrementally as needed |

## 4. Cycle

```
     ┌─────────────────────────────────────────┐
     │                                         │
     ▼                                         │
  1. Communicate requirements/issues            │
     │                                         │
     ▼                                         │
  2. AI analyzes and structures decisions       │
     as GDRs                                   │
     ├─ Clarifies scope / alternatives /       │
     │   trade-offs                             │
     └─ Proposes implementation plan (Phase)    │
     │                                         │
     ▼                                         │
  3. Review & feedback                          │
     ├─ Approve → proceed                      │
     └─ Revise → update GDR and repropose      │
     │                                         │
     ▼                                         │
  4. Implementation                             │
     ├─ AI writes code                         │
     ├─ Verify with tests and builds           │
     └─ Update GDR status to "Implemented"     │
     │                                         │
     ▼                                         │
  5. Next requirement/issue ───────────────────┘
```

One or more GDRs accumulate in each cycle. The project's decision history is stored in GDR_INDEX and serves as a reference point for future decision-making.

## 5. Three Principles

### 5.1. Dialogue Produces the Design Document (Dialog-First)

Rather than writing a design document before having a dialogue, **design emerges within the dialogue**. AI receives requirements in natural language and handles the structuring of decisions (decision / rationale / alternatives / impact / review triggers). Humans focus on the direction and acceptance of decisions.

### 5.2. Decisions Accumulate (Incremental Crystallization)

A perfect GDR does not need to emerge from a single dialogue. Start with rough decisions, and precision improves through review, feedback, and implementation.

- Improvement proposal → Review → Incorporate review → Re-review → Implementation
- An initial GDR may later be split into separate GDRs
- Constraints discovered during implementation may satisfy a GDR's review trigger, leading to decision updates

### 5.3. Implementation Validates Decisions (Implementation Validates Decision)

A GDR is a hypothesis. It is only validated through implementation and testing. A GDR that has been validated changes its status to "Implemented," increasing its reliability. If problems are found during validation, the GDR is updated.

## 6. Expected AI Behavior

| Role | Specific Actions |
|---|---|
| **Structuring** | Convert natural language requirements into GDR format (decision / rationale / alternatives / impact / review triggers) |
| **Quantification** | Incorporate measurement data from actual code (file sizes, line counts, execution times) as evidence |
| **Presenting alternatives** | Present not only the adopted option but also rejected options with their reasons. "Why not" is as important as "why" |
| **Deterring over-engineering** | Be ROI-conscious and point out excessive investments like "hundreds of lines of modification for a few dozen ms of optimization" |
| **Scope determination** | Clarify which areas (arch / ui / pol, etc.) the decision affects |
| **Setting review triggers** | Describe "when this decision should be reconsidered" with specific conditions (numerical thresholds / requirement changes / scale changes) |
| **Implementation and verification** | Write code based on GDRs, verify with tests and builds, and update GDR statuses |
| **Persisting changes** | Reflect implementation and document changes in version control at appropriate granularity (e.g., git commit). AI handles creating change messages, selecting target files, and determining commit units. Humans focus on approving the commits |

## 7. Context Definitions

Before starting GDR Build-Up, define the project's scope and PREFIX. Copy `templates/T1_CONTEXT_DEFINITIONS.md` to create one.

It is natural to create this together with AI in the project's first dialogue, and the scope and PREFIX selection itself can become the first GDR (e.g., `GDR-META-001`).

The definitions document is updated as the project grows. When new domains emerge, add PREFIXes; when new impact areas are identified, add scopes.

## 8. Build-Up Record

A document that records the dialogue history and accumulation of decisions across cycles. Independent of the Context Definitions, it is appended to with each cycle. Copy `templates/T2_BUILDUP_RECORD.md` to create one.

Record at a granularity that suits the team — per session, per sprint, per milestone, etc. The purpose of the record is traceability of "what decisions emerged from what dialogue," not meeting minutes.

## 9. How to Adopt

1. Place `documents/GDR/` in the project
2. Create a Context Definitions document from `templates/T1_CONTEXT_DEFINITIONS.md`
3. Finalize scope and PREFIX in the first dialogue with AI (this itself becomes the first GDR)
4. Thereafter, cycle through "communicate requirements → AI structures GDR → review → implement"
5. Append the cycle flow to the Build-Up Record
6. Records accumulate in `GDR_INDEX`
7. When in doubt about a decision, reference past GDRs. If review triggers are met, update the GDR
