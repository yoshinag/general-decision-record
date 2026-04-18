# 01. Scope Guidelines

> *Translated from Japanese using Claude (Anthropic).*

The `scope` in GDR is a classification that indicates the impact area of a decision. Scope selection varies by project and industry, but the following provides common and industry-specific examples.

## 1. Common Scopes

Scopes used across many projects regardless of industry.

| scope | Abbreviation | Target | Decision Examples |
|---|---|---|---|
| `architecture` | `arch` | System structure, data flow, layer boundaries, DB schema | Component decomposition, communication method selection, data persistence approach |
| `policy` | `pol` | Development process, coding standards, release policy | Error handling policy, branching strategy, review criteria |
| `product` | `prod` | Product direction, naming, target users, revenue model | App name, target age group, billing model |
| `performance` | `perf` | Performance goals, optimization policy, measurement strategy | Response time targets, startup speed criteria, measurement points |
| `meta` | `meta` | Changes to GDR operational rules themselves, document structure | Adding scopes, deprecating PREFIXes, format changes |

## 2. Software Development

Scopes specific to mobile apps, web apps, backend services, etc.

| scope | Abbreviation | Target | Decision Examples |
|---|---|---|---|
| `spec` | `spec` | Functional specifications, data models, API contracts | Endpoint design, data format, screen transition specifications |
| `ui` | `ui` | Visual design, layout, interaction | Font size standards, responsive policy, animation presence |
| `testing` | `test` | Test strategy, coverage targets, E2E policy | Unit test scope, mocking policy, CI test configuration |
| `security` | `sec` | Authentication/authorization, encryption, vulnerability response | Authentication method selection, data encryption policy, dependency library auditing |
| `data` | `data` | Data management, backup, retention period | Migration strategy, backup frequency, personal data retention policy |

## 3. Manufacturing / Hardware

Scopes specific to hardware product development and manufacturing processes.

| scope | Abbreviation | Target | Decision Examples |
|---|---|---|---|
| `quality` | `qual` | Quality management, inspection criteria, defect rate targets | Incoming inspection sampling count, in-process inspection thresholds |
| `supply` | `sup` | Supply chain, procurement, inventory | Single/multi-source policy for parts, safety stock levels |
| `compliance` | `comp` | Certification/standards, regulatory compliance | CE/UL certification policy, RoHS compliance scope |
| `manufacturing` | `mfg` | Manufacturing process, process design | Automation scope, jig design policy, production line configuration |

## 4. Healthcare

Scopes specific to medical devices and healthcare apps.

| scope | Abbreviation | Target | Decision Examples |
|---|---|---|---|
| `regulatory` | `reg` | Regulatory compliance (FDA / PMDA, etc.) | Class classification, submission strategy, clinical trial necessity |
| `clinical` | `clin` | Clinical design, evidence | Endpoint definition, control group design |
| `privacy` | `priv` | Personal health information, anonymization | HIPAA compliance scope, data minimization policy |
| `safety` | `safe` | Safety, risk management | Hazard analysis methodology, risk tolerance criteria |

## 5. Finance / Fintech

Scopes specific to financial services and payment systems.

| scope | Abbreviation | Target | Decision Examples |
|---|---|---|---|
| `compliance` | `comp` | Financial regulations, AML/KYC, reporting obligations | Identity verification method, transaction monitoring thresholds |
| `risk` | `risk` | Risk assessment, limits, monitoring | Credit decision model, fraud detection logic |
| `audit` | `audit` | Audit trail, data retention, internal controls | Log retention period, tampering detection method |
| `privacy` | `priv` | GDPR / CCPA compliance, data minimization | Consent management method, data deletion policy |

## 6. Education / EdTech

Scopes specific to learning apps, LMS, and educational content development.

| scope | Abbreviation | Target | Decision Examples |
|---|---|---|---|
| `curriculum` | `cur` | Curriculum design, learning sequence, difficulty design | Chapter structure, prerequisite knowledge dependencies, number of questions |
| `pedagogy` | `ped` | Teaching methods, learning experience, feedback design | Immediate feedback presence, hint display policy, review intervals |
| `assessment` | `asmt` | Evaluation/grading, proficiency determination | Passing criteria, accuracy rate calculation method, rank definitions |
| `accessibility` | `a11y` | Accessibility, accommodating diverse learners | Screen reader support, color vision consideration, minimum font size |

## 7. Game Development

Scopes specific to game apps and game engine usage.

| scope | Abbreviation | Target | Decision Examples |
|---|---|---|---|
| `gameplay` | `gp` | Game mechanics, rules, balance | Score calculation formula, difficulty curve, reward design |
| `narrative` | `nar` | Story, scenario, presentation | Branching structure, text display method, cutscene presence |
| `monetization` | `mon` | Billing design, gacha, advertising | Billing point design, free/paid boundary, ad frequency |
| `multiplayer` | `mp` | Multiplayer, synchronization, matchmaking | Communication method, latency tolerance, room size limit |

## 8. E-Commerce / Retail

Scopes specific to e-commerce sites and retail systems.

| scope | Abbreviation | Target | Decision Examples |
|---|---|---|---|
| `catalog` | `cat` | Product management, categories, search | Product data model, search algorithm, filter design |
| `checkout` | `chk` | Cart, payment, order flow | Cart expiration, payment methods, inventory allocation timing |
| `logistics` | `log` | Shipping, inventory, warehouse management | Carrier integration method, inventory sync frequency, return policy |
| `pricing` | `prc` | Pricing, discounts, campaigns | Dynamic pricing presence, coupon stacking rules |

## 9. Infrastructure / DevOps

Scopes specific to cloud infrastructure and platform operations.

| scope | Abbreviation | Target | Decision Examples |
|---|---|---|---|
| `deployment` | `dep` | Deployment strategy, environment configuration | Blue-Green / Canary selection, rollback policy |
| `scaling` | `scl` | Scaling, load balancing | Auto-scaling thresholds, region distribution policy |
| `monitoring` | `mon` | Monitoring, alerting, SLO/SLI | Alert thresholds, on-call structure, SLO targets |
| `cost` | `cost` | Cost management, budget | Resource limits, cost allocation policy, reduction targets |
| `disaster` | `dr` | Disaster recovery, backup, BCP | RPO/RTO targets, regional redundancy policy |

## 10. Tourism / Travel

Scopes specific to travel services, reservation systems, and tourism guide apps.

| scope | Abbreviation | Target | Decision Examples |
|---|---|---|---|
| `booking` | `book` | Reservation management, availability/inventory, cancellation policy | Reservation confirmation flow, overbooking policy |
| `localization` | `l10n` | Multi-language, currency, time zones | Language support priority, currency conversion method |
| `geo` | `geo` | Location information, maps, routes, area classification | Offline map support, geofence accuracy |
| `seasonal` | `ssn` | Seasonal fluctuation, rate seasons, operating periods | Peak season rate table, off-peak display policy |

## 11. Revenue / Financial Management (Cross-Industry)

For projects involving monetization, billing, or expenses, regardless of specific industry.

| scope | Abbreviation | Target | Decision Examples |
|---|---|---|---|
| `revenue` | `rev` | Revenue model, revenue composition, KPI | Ad revenue vs. billing ratio target, ARPU target |
| `billing` | `bill` | Billing, subscriptions, refunds | Billing cycle, free trial period, refund policy |
| `ads` | `ads` | Ad operations, ad slots, revenue optimization | Ad network selection, display frequency, eCPM target |
| `payout` | `pay` | Payments, reward distribution, transfers | Creator reward rate, payment cycle, minimum payout amount |
| `accounting` | `acct` | Accounting, tax, bookkeeping | Revenue recognition timing, tax inclusion/exclusion, invoice compliance |

## 12. Legal / Rights / Compliance (Cross-Industry)

For projects involving legal decisions or rights management, regardless of specific industry.

| scope | Abbreviation | Target | Decision Examples |
|---|---|---|---|
| `legal` | `legal` | Contracts, terms of service, licenses | OSS license policy, terms of service update flow |
| `privacy` | `priv` | Personal data protection, consent management | GDPR / CCPA compliance scope, cookie consent method |
| `ip` | `ip` | Intellectual property, patents, trademarks | Patent filing policy, trademark search process |
| `copyright` | `copy` | Copyright, licensing, distribution rights, citation | Content licensing flow, CC license selection, secondary use policy, DRM policy |
| `portrait` | `port` | Portrait rights, publicity rights, talent management | Scope of permitted use of personal images, posting period, handling upon contract termination |

## 13. Adoption Guide

When adopting scopes for a project:
1. Select scopes from the common scopes + relevant industry sections of this guide
2. For projects spanning multiple industries, combine necessary scopes from each industry
3. Add custom scopes if project-specific ones are needed
4. Document the scopes in use in the Context Definitions
5. A single GDR may have multiple scopes (e.g., `arch, pol`)
