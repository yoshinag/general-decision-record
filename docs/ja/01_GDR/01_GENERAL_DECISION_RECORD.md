# 01. GDR（General Decision Record）とは

## 1. 概要

**GDR（General Decision Record）** とは、[ADR（Architectural Decision Record）](https://iroirotool.com/platform/ja/knowledge/hosyu_unyou/adr.html)の派生概念である。ADR がソフトウェアアーキテクチャに関する判断を記録する手段であるのに対し、GDR はアーキテクチャに限定せず、**仕様策定・UI 設計・運用方針・開発プロセス・ビジネス判断** を含む、プロジェクト内のあらゆる意思決定を対象としている。

厳密にいえば「General」が示す scope は **プロジェクトや業界によって異なる**。ソフトウェア開発では architecture / UI / policy が中心になるが、製造業であれば品質管理・サプライチェーン、医療分野であれば臨床手順・規制対応がスコープに加わりうる。GDR のフレームワーク自体は scope の具体的な定義に依存しない — scope テーブルを差し替えるだけで任意のドメインに適用できる。

## 2. 目的

ADR と同一:
1. **判断の根拠を残す** — なぜそう決めたかを将来の自分・チームメイトが追跡できる
2. **再検討を可能にする** — 状況が変わった時に、当時の前提を確認して判断を更新できる
3. **代替案を記録する** — 採用しなかった選択肢とその理由を残し、同じ議論の繰り返しを防ぐ

## 3. 書式

```markdown
**GDR-{PREFIX}-{番号}: {決定の要約}**

- **status:** {Proposed | Accepted | Implemented | Superseded | Rejected}
- **scope:** {scope の略記をカンマ区切り}
- **決定:** 何をするか（または何をしないか）
- **理由:** なぜその判断に至ったか（代替案との比較、トレードオフ）
- **影響:** この決定がもたらす具体的な影響
- **再検討条件:** どのような状況変化があれば判断を見直すか
```

- `{PREFIX}` はドメインを示す短い識別子
- `{番号}` は PREFIX 内の連番（3 桁ゼロ埋め: 001, 002, ...）。採番しなおしても、任意フィールド `uid`（§3.1）は変えない
- `scope` は 1 つ以上。複数の場合はカンマ区切り（例: `arch, pol`）
- `status` は以下の 5 値。**有効**（現行の判断として扱う）と**失効**（判断の根拠にしない）の 2 区分を持つ（経緯: [009 提案](/91_demo_buildup_documents.md/kaizen/09_GDR信頼性強化提案.md) GDR-META-028）:

| status | 区分 | 意味 |
|---|---|---|
| `Proposed` | 有効（未確定） | 提案中。合意に至っていない |
| `Accepted` | 有効 | 合意済み・未実装 |
| `Implemented` | 有効 | 実装済み。コード・設定・運用（文書化された方針等）に反映された |
| `Superseded` | 失効 | 新しい GDR に置き換えられた |
| `Rejected` | 失効 | 起票された提案そのものが採用されなかった（合意後の撤回を含む） |

**遷移:**

| 遷移 | 契機 |
|---|---|
| `Proposed → Accepted` | 合意 |
| `Accepted → Implemented` | 実装・反映 |
| `Proposed → Rejected` | 不採用 |
| `Accepted → Rejected` | 合意後の撤回（実装段階で前提が崩れた等。却下理由にその旨を書く） |
| `Accepted / Implemented → Superseded` | 新しい GDR による置換 |

- `Accepted` への更新は合意の時点で行う
- `Rejected` と `Superseded` は終端状態（例外は後述の「撤回時の復帰」のみ）
- 「X はしない」こと自体を方針として拘束したい場合は、否定形の決定を持つ GDR を起票する（`Rejected` ではない）
- `Rejected` には理由配下にサブ箇条書き `- **却下理由:** ...` を必須とする。却下した案を再提案する場合は新 GDR を起票し、任意フィールド「関連」で `derived-from GDR-X-NNN` とつなぐ（`supersedes` は使わない）

![GDR の status と遷移 — 有効（Proposed・Accepted・Implemented）と失効（Superseded・Rejected）、撤回時の復帰、二段保管の退避時点](assets/gdr-status-transitions.svg)

**置換（supersede）の記法と切替時点:** 相互リンクは status 行に書く。status 行は「先頭トークンが status 値、以降の `by` 句・括弧が置換リンク」と読む:

```markdown
- **status:** Superseded by GDR-UI-003          ← 旧
- **status:** Accepted (supersedes GDR-UI-001)   ← 新（実装後は Implemented (supersedes GDR-UI-001)）
```

- 旧を `Superseded` にするのは**新が `Accepted` になった時点**。新が `Proposed` の間は旧を有効のまま残す
- **撤回時の復帰:** 置換予定だった新が `Accepted → Rejected` で撤回された場合、旧の status を置換前の値に戻し注記する（例: `Implemented（GDR-UI-003 の撤回により復帰）`）。判断内容は変わらないため軽微な訂正として扱う
- **波及チェック:** 置換・合意後の撤回で失効する GDR を「関連」の `depends-on` / `refines` で前提にしている有効な GDR は、置換の起票時に列挙し、合意時に人間が判定し、新が `Implemented` になった時点で「関連」を付け替える（合意後の撤回では、撤回を諮る時点で列挙し、`Rejected` の確定時に判定し、退避の前に付け替える）。旧を `depends-on` / `refines` で指す有効な GDR が残っている間は、旧を退避しない。手順は [02 §5.2](/01_GDR/02_AI_DRIVEN_GDR_BUILDUP.md#52-判断は積み上がるincremental-crystallization)（経緯: [013 提案](/91_demo_buildup_documents.md/kaizen/13_GDR置換時の波及チェック提案.md) GDR-META-038）

**二段保管の推奨:** 失効した GDR は、`GDR_INDEX` に 1 行サマリを残したうえで本文ファイルを `notes/_archive/91_gdr/gdr/` へ退避する運用を推奨する。AI は INDEX の 1 行で置換関係と再検討条件を把握でき、詳細議論本文は読まずに済むため、トークン消費が抑えられる。

| status | 退避のタイミング | INDEX の 1 行サマリ |
|---|---|---|
| `Superseded` | 新が `Implemented` になった時点（`Accepted` の間は元の位置に置く — 実装はまだ旧に従っており、撤回時の復帰も status 行の訂正で済む） | `GDR-OLD-NNN（要約） — Superseded by GDR-NEW-MMM → archived` |
| `Rejected` | 確定時点 | `GDR-X-NNN（要約） — Rejected（却下理由の要約） → archived` |

いずれの退避も、退避する GDR を「関連」の `depends-on` / `refines` で指す有効な GDR が残っていないこと（波及チェックの不変条件）を満たしてから行う。

詳細は [02. AI-Driven GDR ビルドアップ §5.2](/01_GDR/02_AI_DRIVEN_GDR_BUILDUP.md#52-判断は積み上がるincremental-crystallization) を参照。

### 3.1. 任意フィールド

可視化（[06_VISUALIZATION_GUIDE.md](/01_GDR/guide/06_VISUALIZATION_GUIDE.md)）と DB 化（横断検索基盤への取り込み）を見据え、6 フィールドの**後**に以下の任意フィールドを追加できる（経緯: [008 提案](/91_demo_buildup_documents.md/kaizen/08_GDR可視化対応提案.md) GDR-META-025）:

```markdown
- **日時:** 2026-07-15T14:30:00+09:00
- **関連:** depends-on GDR-INFRA-002, derived-from §2-1
- **理由の出所:** human（ユーザー発言「障害時にセッションが全部飛ぶのは許容できない」）
- **uid:** 01a2160a-ab52-7343-bb37-84748947ff68
```

（`uid` の値は例。写さずに、下のコマンドで生成する）

| フィールド | 形式 | 意味 |
|---|---|---|
| `日時` | ISO 8601 日付時刻・**タイムゾーンオフセット付き**（`YYYY-MM-DDTHH:MM:SS+09:00`）。時刻が不明な過去の判断は日付のみ（`YYYY-MM-DD`）も許容し、解釈は取り込み側で正規化する | 決定日時。同日に複数の判断が積み上がっても前後関係を保持する。status 遷移日時は追わない |
| `関連` | `{型} {対象}` のカンマ区切り。型は `depends-on`（前提依存）/ `refines`（親決定の細分化）/ `relates-to`（弱い関連）/ `derived-from`(由来) の**閉集合**、対象は GDR ID または文書内の `§{章}-{番号}` 参照 | GDR 間・課題間の型付きリンク。supersede 系は従来どおり status 行に記載する（関連には書かない） |
| `理由の出所` | `human` / `ai-reviewed` / `ai` の**閉集合**（信頼度の順序 `human > ai-reviewed > ai`）。先頭トークンが値、以降の括弧内は注記（全角・半角どちらも可）。`human` では発言の短い引用または出典の注記が必須 | 理由の核心がどこから来たか。`human` = 人間の発言・文書に由来（AI は整形のみ）/ `ai-reviewed` = AI が起案し人間がレビュー・合意で確認 / `ai` = AI の推論のみで人間未確認（経緯: [009 提案](/91_demo_buildup_documents.md/kaizen/09_GDR信頼性強化提案.md) GDR-META-030） |
| `uid` | UUID v7 の正規表記（小文字の 8-4-4-4-12）。ツールで生成し、手で書かない（生成のコマンドは下記） | GDR レコード 1 件の変わらない識別子。起票時に 1 回だけ付け、status の遷移・採番しなおし・退避でも変えない。置換・再提案の新しい GDR は新しい値を持ち、同じ GDR の写し（改善提案と記録）は同じ値を持つ。採番しなおしても同じ GDR だと分かるため、およびプロジェクトをまたぐ参照の併記（本文に `{リポジトリ名} リポジトリの GDR-…` と `uid`）に使う。リンクの対象・日時の順の確認には使わない（経緯: [015 提案](/91_demo_buildup_documents.md/kaizen/15_GDRの系譜の明確化とUUIDv7の検討提案.md) GDR-META-040） |

- 任意フィールドの**欠落は書式違反ではない**（lint 等で警告しない）。記録する価値がある場合にのみ書く
- 型の語彙の追加・改廃は GDR-META で行う

**理由の出所の規則:**

- **AI が GDR を起票・更新する場合は記入必須**（任意フィールドの例外）。欠落は「不明」とみなし、信頼度判断では `ai` と同等に扱う
- 出所が混在する場合は、理由を構成する部分のうち**最も弱い値**を書き、人間由来の部分は注記の引用で示す。レビュー・合意を経た時点で `ai` の部分は `ai-reviewed` に上がる（`Proposed → Accepted` と同時に更新。軽微な追記扱い）
- `human` の引用は要約・言い換えではなく**発言の断片そのもの**（1 文程度）。個人名は役割（「ユーザー」「レビュアー」）に置き換える
- **AI は理由が不明な判断に理由を補完しない。** 根拠が確認できない場合は理由欄に「不明（記録時点で根拠未確認）」と書き、出所は `ai` とする

**`uid` の生成:** AI が値を手で書かない（もっともらしい値を作ってしまい、時刻も一意性も保証されない）。次の 1 行で生成する（Python 3.7 以上。標準ライブラリだけ）。使えなければ `uid` を書かない（書式違反ではない）。macOS の `uuidgen` は v4 なので使わない。既存の GDR や上の例から値を写さない。遡って付けるのは任意で、軽微な追記として扱う（その時刻は付けた時点のもの）

```bash
python3 -c "import os,time,uuid;b=bytearray((time.time_ns()//10**6).to_bytes(6,'big')+os.urandom(10));b[6]=b[6]&15|112;b[8]=b[8]&63|128;print(uuid.UUID(bytes=bytes(b)))"
```

**系譜（先祖・子孫）の規則:**（経緯: [015 提案](/91_demo_buildup_documents.md/kaizen/15_GDRの系譜の明確化とUUIDv7の検討提案.md) GDR-META-040）

- GDR の親 → 子は、置換（旧 → 新。status 行）、`refines`（親決定 → 細分化した決定）、GDR を指す `derived-from`（元 → 派生）の 3 種で表す。先祖・子孫はこれを推移的にたどった集合。`depends-on` と `relates-to`、課題（`§N-M`）への `derived-from` は親子に含めない。前提の連鎖（`depends-on` と `refines` を推移的にたどる。波及チェックと同じ範囲）は親子と並べてたどる
- 型の選び分け: `refines` = 親の決定の範囲の内側（分けた・具体的にした）/ `depends-on` = 別の対象の判断で、親が成り立つことを条件にする / `derived-from GDR-…` = 親の案や検討から生まれたが、親が成り立つことを条件にしない（却下・保留された案の再提案など）。同じ相手には 1 つだけ書く（`refines` は前提であることを含むので `depends-on` と重ねない）
- 親を持たない GDR を「起点」、子を持たない GDR を「末端」と呼ぶ。系譜は現在の「関連」と status 行から導く
- **不変条件:** 系譜は閉路を持たない。置換と GDR 向き `derived-from` では、両端に日時があるとき親の日時 ≤ 子の日時（オフセットを考慮して比べ、日付のみ・オフセットの無い時刻が片方にあれば日付で比べて、同日は違反としない。読めない日時の端は比べない）。`refines` には日時の順を課さない（波及チェックの付け替えや、後から親を起票する流れで正当に破れるため）。違反は書式違反ではなく、`系譜` プロンプト（[04 §5](/01_GDR/guide/04_PROMPT_GUIDE.md#5-ふりかえり・検証)）の警告として出す。異なる GDR ID に同じ `uid` があるものも警告する
- 系譜は参照の規律（[02 §6](/01_GDR/02_AI_DRIVEN_GDR_BUILDUP.md#6-ai-に求められる振る舞い)）を変えない。後継としてたどるのは置換リンクだけ
- 既存の GDR を細分化・派生・置換して起票するときは、親を書く（推奨）。AI が起票するときは日時と `uid` も書く（推奨）。いずれも欠落は書式違反にしない

**あわせて定義する規約:**

- **主 scope:** `scope` の**先頭記載を主 scope** とみなす（可視化等で代表 scope が 1 つ必要な場面の規約。複数 scope の意味は従来どおり）
- **代替案の正式記法:** 理由フィールド配下のサブ箇条書き `- **代替案[ {ラベル}]:** {概要} → {評価}`。ラベル（A, B, ...）は複数案あるときのみ必須（1 件なら省略可）、却下した場合は末尾に「。却下」、部分採用・保留はその旨を記す

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

PREFIX と scope は同名になることがある（例: `GDR-UI-001` の `scope: ui`）。これは冗長ではなく、ドメイン識別と影響領域分類という異なる軸で記録されるため、両方を記述する。

業種別の PREFIX 一覧 → [02_PREFIX_GUIDE.md](/01_GDR/guide/02_PREFIX_GUIDE.md)

## 5. 関連文書

| # | 文書 | 内容 |
|---|---|---|
| 02 | [02_AI_DRIVEN_GDR_BUILDUP.md](/01_GDR/02_AI_DRIVEN_GDR_BUILDUP.md) | AI-Driven GDR ビルドアップ（定義 / サイクル / 原則） |
| G-00 | [00_GETTING_STARTED.md](/01_GDR/guide/00_GETTING_STARTED.md) | 最短導入ガイド（Getting Started） |
| G-01 | [01_SCOPE_GUIDE.md](/01_GDR/guide/01_SCOPE_GUIDE.md) | scope ガイドライン（共通 + 業種別） |
| G-02 | [02_PREFIX_GUIDE.md](/01_GDR/guide/02_PREFIX_GUIDE.md) | PREFIX ガイドライン（共通 + 業種別） |
| G-03 | [03_FIRST_PROMPT_GUIDE.md](/01_GDR/guide/03_FIRST_PROMPT_GUIDE.md) | ローカライズ初回プロンプトガイド |
| G-04 | [04_PROMPT_GUIDE.md](/01_GDR/guide/04_PROMPT_GUIDE.md) | プロンプトガイドライン（推奨プロンプト集） |
| G-05 | [05_CLAUDE_CODE_SETUP.md](/01_GDR/guide/05_CLAUDE_CODE_SETUP.md) | Claude Code セットアップ仕様（user-level config / スラッシュコマンド） |
| G-06 | [06_VISUALIZATION_GUIDE.md](/01_GDR/guide/06_VISUALIZATION_GUIDE.md) | 可視化ガイド（構造ビュー / 関係ビュー / `/gdr-map`） |
| T0 | [T0_FIRST_GDR_SAMPLE.md](/01_GDR/templates/T0_FIRST_GDR_SAMPLE.md) | 最初の GDR（`GDR-META-001`）の記述例 |
| T1 | [T1_CONTEXT_DEFINITIONS.md](/01_GDR/templates/T1_CONTEXT_DEFINITIONS.md) | Context Definitions テンプレート |
| T2 | [T2_BUILDUP_RECORD.md](/01_GDR/templates/T2_BUILDUP_RECORD.md) | ビルドアップ記録テンプレート |
