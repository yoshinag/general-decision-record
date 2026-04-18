# 02. PREFIX Guidelines

> *Translated from Japanese using Claude (Anthropic).*

The `{PREFIX}` in GDR is a short identifier indicating the domain. PREFIX selection varies by project and industry, but the following provides common and industry-specific examples.

## 1. Common PREFIXes

PREFIXes used across many projects regardless of industry.

| PREFIX | Domain | Representative Scopes | Usage |
|---|---|---|---|
| INFRA | Infrastructure | `arch`, `pol` | Error handling, retry strategies, common infrastructure design policies |
| PERF | Performance | `perf`, `arch` | Response time targets, optimization policies, measurement strategies |
| LOG | Logging / Audit | `arch`, `pol` | Log persistence, rotation, audit trails |
| SEC | Security | `pol`, `arch` | Authentication/authorization methods, encryption policies, vulnerability response |
| DATA | Data Management | `arch`, `spec` | Data models, backups, retention periods |
| META | Meta | `meta` | Changes to GDR operational rules themselves, document structure |
| APP | App / Product Identity | `prod` | Identifiers, naming, versioning |

## 2. Software Development

| PREFIX | Domain | Representative Scopes | Usage |
|---|---|---|---|
| UI | UI / UX | `ui`, `spec` | Layout, interaction, accessibility |
| API | API Design | `arch`, `spec` | Endpoint design, versioning, authentication |
| HTTP | HTTP Communication | `arch`, `spec` | Request design, caching, timeouts |
| FS | File System | `arch`, `pol` | Storage structure, permissions, platform support |
| FILE | File Transfer | `arch` | Upload/download methods, retry |
| ASSET | Asset Management | `arch`, `pol` | Bundle structure, build pipeline |
| IMPORT | Import / Export | `arch`, `spec` | Data ingestion, format conversion |
| AD | Advertising / Monetization | `prod`, `pol` | Ad SDK selection, placement, compliance |
| TEST | Test Strategy | `pol` | Test scope, coverage targets, E2E policy |
| CI | CI/CD | `pol`, `arch` | Build pipeline, deployment, release flow |
| DEP | Dependency Management | `pol` | Package selection criteria, update policy |

## 3. Manufacturing / Hardware

| PREFIX | Domain | Representative Scopes | Usage |
|---|---|---|---|
| HW | Hardware Design | `arch`, `spec` | Circuit design, component selection, thermal design |
| QC | Quality Control | `pol`, `spec` | Inspection criteria, defect rate targets, sampling |
| SCM | Supply Chain | `pol`, `prod` | Supplier selection, lead times, inventory policy |
| MFG | Manufacturing Process | `arch`, `pol` | Process design, jigs, production line configuration |
| CERT | Certification / Standards | `pol` | CE / UL / PSE certification policies, test plans |
| PKG | Packaging | `spec`, `prod` | Package design, transport durability, labeling requirements |

## 4. Healthcare

| PREFIX | Domain | Representative Scopes | Usage |
|---|---|---|---|
| REG | Regulatory Compliance | `pol` | FDA / PMDA compliance, class classification, submission strategy |
| CLIN | Clinical | `spec`, `pol` | Clinical trial design, endpoint definition |
| PHI | Personal Health Information | `pol`, `arch` | HIPAA / personal data protection compliance, anonymization |
| IFU | Instructions for Use | `spec`, `prod` | Package inserts, labeling, usage precautions |
| BIO | Biocompatibility | `spec` | Material selection, toxicity testing, sterilization methods |

## 5. Finance / Fintech

| PREFIX | Domain | Representative Scopes | Usage |
|---|---|---|---|
| COMP | Compliance | `pol` | Financial regulations, AML/KYC, reporting obligations |
| RISK | Risk Management | `pol`, `arch` | Risk assessment, limit setting, monitoring |
| PAY | Payment | `arch`, `spec` | Payment flow, tokenization, idempotency |
| AUDIT | Audit | `pol` | Audit trail, data retention, internal controls |
| PRIV | Privacy | `pol`, `arch` | GDPR / CCPA compliance, data minimization |

## 6. Education / EdTech

| PREFIX | Domain | Representative Scopes | Usage |
|---|---|---|---|
| CUR | Curriculum | `cur`, `spec` | Learning sequence, chapter structure, difficulty design |
| ASMT | Assessment / Grading | `asmt`, `spec` | Passing criteria, accuracy rate calculation, proficiency determination |
| LRN | Learning Experience | `ped`, `ui` | Feedback design, review intervals, hint policy |
| A11Y | Accessibility | `a11y`, `ui` | Screen reader support, color vision support, font size |

## 7. Game Development

| PREFIX | Domain | Representative Scopes | Usage |
|---|---|---|---|
| GP | Gameplay | `gp`, `spec` | Mechanics, balance, reward design |
| NAR | Narrative | `nar`, `spec` | Scenario branching, text display, presentation |
| MTX | Monetization | `mon`, `prod` | Billing design, gacha rates, ad frequency |
| NET | Network | `mp`, `arch` | Multiplayer communication, synchronization, matchmaking |

## 8. E-Commerce / Retail

| PREFIX | Domain | Representative Scopes | Usage |
|---|---|---|---|
| CART | Cart / Orders | `chk`, `spec` | Cart design, order flow, inventory allocation |
| CTLG | Product Catalog | `cat`, `spec` | Product data model, search, filters |
| SHIP | Shipping / Logistics | `log`, `pol` | Carrier integration, return policy, tracking |
| PRC | Pricing / Promotions | `prc`, `prod` | Price setting, coupons, campaigns |

## 9. Infrastructure / DevOps

| PREFIX | Domain | Representative Scopes | Usage |
|---|---|---|---|
| DEPLOY | Deployment | `dep`, `pol` | Deployment strategy, rollback policy |
| SCALE | Scaling | `scl`, `arch` | Auto-scaling, load balancing |
| MON | Monitoring / Alerting | `mon`, `pol` | Alert thresholds, SLO/SLI, on-call |
| COST | Cost Management | `cost`, `pol` | Resource limits, cost allocation, reduction targets |
| DR | Disaster Recovery | `dr`, `pol` | RPO/RTO targets, regional redundancy |

## 10. Tourism / Travel

| PREFIX | Domain | Representative Scopes | Usage |
|---|---|---|---|
| BOOK | Booking | `book`, `spec` | Reservation flow, cancellation, payment integration |
| L10N | Localization | `l10n`, `ui` | Translation management, currency, date/time display |
| MAP | Maps / Routes | `geo`, `ui` | Map SDK selection, route display method |
| VENUE | Facilities / Spots | `spec`, `prod` | Facility data model, reviews, business information |

## 11. Revenue / Financial Management (Cross-Industry)

| PREFIX | Domain | Representative Scopes | Usage |
|---|---|---|---|
| REV | Revenue Model | `rev`, `prod` | Revenue composition, KPI design, monetization policy |
| BILL | Billing | `bill`, `spec` | Subscriptions, pricing plans, refunds |
| ADS | Ad Operations | `ads`, `prod` | Ad networks, display frequency, eCPM optimization |
| PAYOUT | Payments / Distribution | `pay`, `pol` | Reward rates, payment cycles, transfer methods |
| ACCT | Accounting / Tax | `acct`, `pol` | Revenue recognition, sales tax, invoice compliance |

## 12. Legal / Rights / Compliance (Cross-Industry)

| PREFIX | Domain | Representative Scopes | Usage |
|---|---|---|---|
| LEGAL | Legal | `legal`, `pol` | Contracts, terms of service, license policies |
| PRIV | Privacy | `priv`, `pol` | Personal data protection, consent management, GDPR/CCPA |
| IP | Intellectual Property | `ip`, `pol` | Patent filing policy, trademark search, OSS licensing |
| CR | Copyright | `copy`, `pol` | Copyright processing, licensing, DRM, citation guidelines |
| PORT | Portrait Rights | `port`, `pol` | Portrait/publicity right permission management, posting scope/period |

## 13. Adoption Guide

When adopting GDR for a project:
1. Select PREFIXes from the common PREFIXes + relevant industry sections of this guide
2. For projects spanning multiple industries, combine necessary PREFIXes from each industry
3. Add custom PREFIXes if project-specific ones are needed
4. Document the PREFIXes and their corresponding scopes in the Context Definitions
5. When adding a new PREFIX, create a new section in `GDR_INDEX`
