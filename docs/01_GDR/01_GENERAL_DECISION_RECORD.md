# 01. GDR（General Decision Record）とは

## 目次

1. [概要](#1-概要)
2. [目的](#2-目的)
3. [書式](#3-書式)
4. [scope と PREFIX](#4-scope-と-prefix)
5. [関連文書](#5-関連文書)

## 1. 概要

**GDR（General Decision Record）** は、[ADR（Architectural Decision Record）](https://iroirotool.com/platform/ja/knowledge/hosyu_unyou/adr.html)の派生概念である。ADR がソフトウェアアーキテクチャに関する判断を記録する手段であるのに対し、GDR はアーキテクチャに限定せず、**仕様策定・UI 設計・運用方針・開発プロセス・ビジネス判断** を含む、プロジェクト内のあらゆる意思決定を統一的に記録する。

「General」が示す scope は **プロジェクトや業界によって異なる**。ソフトウェア開発では architecture / UI / policy が中心になるが、製造業であれば品質管理・サプライチェーン、医療分野であれば臨床手順・規制対応がスコープに加わりうる。GDR のフレームワーク自体は scope の具体的な定義に依存しない — scope テーブルを差し替えるだけで任意のドメインに適用できる。

## 2. 目的

ADR と同一:
1. **判断の根拠を残す** — なぜそう決めたかを将来の自分・チームメイトが追跡できる
2. **再検討を可能にする** — 状況が変わった時に、当時の前提を確認して判断を更新できる
3. **代替案を記録する** — 採用しなかった選択肢とその理由を残し、同じ議論の繰り返しを防ぐ

## 3. 書式

```markdown
**GDR-{PREFIX}-{番号}: {決定の要約}**

- **status:** {Proposed | Approved | Implemented | Superseded}
- **scope:** {scope の略記をカンマ区切り}
- **決定:** 何をするか（または何をしないか）
- **理由:** なぜその判断に至ったか（代替案との比較、トレードオフ）
- **影響:** この決定がもたらす具体的な影響
- **再検討条件:** どのような状況変化があれば判断を見直すか
```

- `{PREFIX}` はドメインを示す短い識別子
- `{番号}` は PREFIX 内の連番（3 桁ゼロ埋め: 001, 002, ...）
- `scope` は 1 つ以上。複数の場合はカンマ区切り（例: `arch, pol`）
- `status` は以下の 4 値:

| status | 意味 |
|---|---|
| `Proposed` | 提案中。レビュー・承認を待っている |
| `Approved` | 承認済み。実装に着手してよい |
| `Implemented` | 実装済み。コードや設定に反映された |
| `Superseded` | 代替済み。新しい GDR に置き換えられた |

`Superseded` にする場合は、代替先の GDR ID を記載し、代替先からも元の GDR へリンクを貼ること（例: `Superseded by GDR-UI-003` / `Supersedes GDR-UI-001`）

## 4. scope と PREFIX

GDR の書式（3 章）に登場する 2 つの分類軸を定義する。

### 4.1. scope — 決定の影響領域

scope は「この判断が何に影響するか」を示す分類である。GDR フレームワークは特定の scope セットを強制しない。プロジェクトや業界に合わせて定義する。

例: `arch`（アーキテクチャ）、`spec`（機能仕様）、`ui`（UI・UX）、`pol`（開発プロセス）、`prod`（プロダクト方針）、`perf`（パフォーマンス）、`meta`（GDR 運用）

1 つの GDR が複数の scope を持つことがある（例: `arch, pol`）。

業種別の scope 一覧 → [01_SCOPE_GUIDE.md](/01_GDR/guide/01_SCOPE_GUIDE.md)

### 4.2. PREFIX — ドメイン識別子

PREFIX は `GDR-{PREFIX}-{番号}` の形式で使われる、ドメインを示す短い識別子である。scope が「影響領域の分類」であるのに対し、PREFIX は「どのドメインの判断か」を一意に識別する。

例: `INFRA`（インフラ基盤）、`UI`（UI・UX）、`AD`（広告・収益化）、`META`（GDR 運用）

業種別の PREFIX 一覧 → [02_PREFIX_GUIDE.md](/01_GDR/guide/02_PREFIX_GUIDE.md)

## 5. 関連文書

| # | 文書 | 内容 |
|---|---|---|
| 02 | [02_AI_DRIVEN_GDR_BUILDUP.md](/01_GDR/02_AI_DRIVEN_GDR_BUILDUP.md) | AI-Driven GDR ビルドアップ（定義 / サイクル / 原則） |
| G-01 | [01_SCOPE_GUIDE.md](/01_GDR/guide/01_SCOPE_GUIDE.md) | scope ガイドライン（共通 + 業種別） |
| G-02 | [02_PREFIX_GUIDE.md](/01_GDR/guide/02_PREFIX_GUIDE.md) | PREFIX ガイドライン（共通 + 業種別） |
| G-03 | [03_FIRST_PROMPT_GUIDE.md](/01_GDR/guide/03_FIRST_PROMPT_GUIDE.md) | ローカライズ初回プロンプトガイド |
| G-04 | [04_PROMPT_GUIDE.md](/01_GDR/guide/04_PROMPT_GUIDE.md) | プロンプトガイドライン（推奨プロンプト集） |
| T1 | [T1_CONTEXT_DEFINITIONS.md](/01_GDR/templates/T1_CONTEXT_DEFINITIONS.md) | Context Definitions テンプレート |
| T2 | [T2_BUILDUP_RECORD.md](/01_GDR/templates/T2_BUILDUP_RECORD.md) | ビルドアップ記録テンプレート |
