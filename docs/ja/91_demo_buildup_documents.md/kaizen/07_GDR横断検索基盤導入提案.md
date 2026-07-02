# 007. GDR 横断検索基盤導入提案（gdr-index）

## 目次

**GDR 一覧:**

| GDR ID | 決定の要約 | status |
|---|---|---|
| GDR-META-019 | 実運用 GDR の横断検索基盤 gdr-index を「git を正とする再構築可能な派生インデックス」として導入する | Proposed |
| GDR-META-020 | 取り込み単位は GDR レコードとし、`(project, gdr_id)` を複合キーにする | Proposed |
| GDR-META-021 | 検索エンジンは SQLite + FTS5(trigram) + sqlite-vec のハイブリッドとし、embedding は差し替え可能な IF でローカル既定にする | Proposed |
| GDR-META-022 | 利用面は CLI + MCP サーバ（user scope）とし、`/gdr-docs` 完了処理を sync の標準トリガにする | Proposed |

---

## 1. GDR（General Decision Record）

**GDR-META-019: 実運用 GDR の横断検索基盤 gdr-index を「git を正とする再構築可能な派生インデックス」として導入する**

- **status:** Proposed
- **scope:** meta, arch
- **決定:** 各プロジェクトの git リポジトリを正（source of truth）とし、GDR レコードを SQLite 1 ファイルへ冪等に取り込む派生インデックスツール **gdr-index** を方法論のコンパニオンツールとして導入する。DB は永続的な真実を一切持たず、`rebuild` でいつでもソースから全再構築できる。`notes/_archive/91_gdr/` 配下も indexer の読み取り対象とし、`archived` フラグで区別して保持する
- **理由:** GDR の目的 3「同じ議論の繰り返しを防ぐ」（[01 §2](/01_GDR/01_GENERAL_DECISION_RECORD.md#2-目的)）は、プロジェクトを跨ぐと達成手段がない。判断は各リポジトリに閉じ、他プロジェクトの類似判断は運用者の記憶頼みになっている。また [GDR-META-016 / 018 の二段保管](/91_demo_buildup_documents.md/kaizen/06_アーカイブ機構導入提案.md)は AI 文脈からの除外（トークン節約）と引き換えに、詳細議論への到達手段を「明示パス指定」だけに細めた。DB 経由のオンデマンド参照はこの除外ルールと矛盾しない — 除外の目的はセッションのトークン節約であり、必要な瞬間だけ検索で引く動線はむしろ二段保管の意図の完成形である。これにより**三層構造**（アクティブ GDR＝セッション文脈 / INDEX 1 行＝置換関係の把握 / DB＝オンデマンドの長期記憶）が成立する
  - **代替案 A:** `rg` による横断 grep → 字面一致のみで意味検索ができず、scope / status の構造化フィルタも archive 層の扱いも弱い。現規模（後述 §2-5）では実用だが「記憶層」にはならない
  - **代替案 B:** 中央 DB を正とし文書を DB 管理に移行 → git を正とする方法論の大前提と矛盾。二重管理が発生するため却下
  - **代替案 C:** 何もしない → 今日は困らないが、蓄積が方法論の価値そのものである以上、レコード数がスケールしてからの導入は取り込み・検証コストが上がる
- **影響:**
  - Superseded GDR の詳細議論が、AI セッション文脈を汚さずに検索可能になる（GDR-META-016 の再検討条件「横断レビュー時に過去判断を参照したい頻度が高い」への先回りの答え）
  - 取り込み時の書式検査（lint）が副産物として得られ、6 フィールド書式の品質装置になる
  - DB は派生物なのでバックアップ・同期の運用は発生しない
- **再検討条件:**
  - チーム利用・Web UI の需要が発生 → サーバ型（PostgreSQL + pgvector 等）への移行を検討
  - 運用が定着せず sync が半年止まったまま → 基盤そのものの廃止を検討


**GDR-META-020: 取り込み単位は GDR レコードとし、`(project, gdr_id)` を複合キーにする**

- **status:** Proposed
- **scope:** meta, spec
- **決定:** 取り込み単位はファイルではなく **GDR レコード**（`**GDR-{PREFIX}-{番号}: {要約}**` 見出し + 6 フィールドの塊）とする。6 フィールドは blob にせず列に分解し、自然キーは `(project, gdr_id)` の複合キーとする。`_reference/`（上流スナップショット）と `INDEX.md`（1 行サマリ形式でフィールドを持たない）は取り込み除外。パースは寛容に行い、フィールド欠落・書式逸脱は警告として lint レポートに出力する。scope 略記の解決のため、各プロジェクトの前提定義書（`00_CONTEXT_DEFINITIONS.md`）の scope テーブルも取り込む
- **理由:** 起票前の実測（2026-07-02、実運用 4 リポジトリ）で設計の必然性を確認した。(1) 1 ファイルに複数レコードが存在する、(2) **全 4 リポジトリに `GDR-META-001` が正当に存在**する — GDR ID はプロジェクト内でしか一意でなく、横断 DB では複合キーが必須、(3) 単純 grep では各リポジトリの `_reference/` 内 T0 サンプルが混入して重複カウントされた — 除外ルールが実データで裏付けられた。フィールド分解は「再検討条件に『負荷』を含む Implemented を列挙」のような**二段保管レビューの実用クエリ**を可能にするため
  - **代替案:** ファイル単位 + 全文 blob → フィールド指定検索が不能、変更検知が粗くなり embedding 再計算も過剰になる。却下
- **影響:**
  - パーサが [01 §3 書式](/01_GDR/01_GENERAL_DECISION_RECORD.md#3-書式)のリファレンス実装（機械可読性の検証装置）になる
  - 書式逸脱がプロジェクト横断で可視化される
  - scope 略記がプロジェクトローカルな語彙であることが明示され、横断検索では正式名に正規化して扱える
- **再検討条件:**
  - 6 フィールド書式自体の改廃 GDR が発行された場合（パーサの追随が必要）


**GDR-META-021: 検索エンジンは SQLite + FTS5(trigram) + sqlite-vec のハイブリッドとし、embedding は差し替え可能な IF でローカル既定にする**

- **status:** Proposed
- **scope:** meta, arch
- **決定:** 単一 SQLite ファイルに FTS5（**trigram トークナイザ**）と sqlite-vec（vec0 仮想テーブル）を同居させ、BM25 と KNN の結果を RRF（Reciprocal Rank Fusion, k=60）で融合する。project / status / scope / prefix のフィルタは SQL で行う。embedding は 1 レコード 1 ベクトル（タイトル + 決定 + 理由 + 再検討条件の連結、チャンク分割なし）。Embedder は 1 インターフェースで差し替え可能とし、**既定はローカルモデル**（Ollama 経由の bge-m3 / 日本語特化の ruri 系を候補にフェーズ 2 で実測選定）
- **理由:** 個人運用・2 桁〜数千レコードの規模に対し、単一ファイル・運用ゼロ・SQL による構造化フィルタが揃う組み合わせは SQLite が最有力。**日本語対応の要点は trigram** — FTS5 標準の unicode61 は分かち書きされない日本語をトークン化できず、trigram なら「認証」「デフォルト窓」等の部分一致が成立する（MeCab / lindera 等の形態素解析はこの規模では過剰）。embedding をローカル既定にするのは、レコードが短く件数も少ないためコスト差がどの選択でも誤差であり、この規模のために API 契約と鍵管理を増やす価値が薄いため（API 派に切り替える場合は Voyage AI / OpenAI embeddings が候補。Anthropic は embeddings API を提供していない）
  - **代替案 A:** LanceDB → embedded でベクトル特化だが、SQL フィルタ・FTS の柔軟さで劣り依存も重い
  - **代替案 B:** DuckDB + vss → vss 拡張の永続化が未成熟
  - **代替案 C:** Chroma / Qdrant → サーバ運用が発生し個人規模には過剰
  - **代替案 D:** PostgreSQL + pgvector → チーム化・Web UI 化まで不要（GDR-META-019 の再検討条件に接続）
- **影響:**
  - 依存は Python + sqlite-vec 拡張 +（任意で）ローカル embedding ランタイムのみ。実装規模の見積もりは 500 行弱
  - sqlite-vec はブルートフォース KNN だが数千レコードまで実用十分
  - Embedder IF の分離により、モデル変更時は全レコード再 embed（`rebuild`）だけで移行できる
- **再検討条件:**
  - レコード数万超で KNN レイテンシが顕在化
  - trigram の日本語検索精度が実用に耐えないと判明（→ 形態素トークナイザの再検討）
  - ローカル embedding の意味検索品質が不足（→ API 埋め込みへ切替）


**GDR-META-022: 利用面は CLI + MCP サーバ（user scope）とし、`/gdr-docs` 完了処理を sync の標準トリガにする**

- **status:** Proposed
- **scope:** meta, pol
- **決定:** 利用面は 2 つ提供する。(1) CLI: `gdr-index sync / search / rebuild / lint`、(2) **MCP サーバ**（読み取り専用）: `gdr_search(query, project?, scope?, status?, k)` / `gdr_get(project, gdr_id)`（supersede チェーン込み）/ `gdr_list_projects()`。MCP は Claude Code にユーザスコープで登録し、**全プロジェクトのセッションから横断参照可能**にする。取り込みトリガは手動 `sync` を基本とし、`/gdr-docs`（完了処理）の最終ステップに sync 実行を 1 行統合する。git hook・常駐デーモンは作らない。最終形（フェーズ 4）として `/gdr-flow` 起票フェーズでの類似判断自動照会を目指す
- **理由:** 検索の価値が最大化するのは「新しい判断をする瞬間」であり、それはエディタでも Web でもなく AI セッションの中にある — MCP 統合が本命なのはこのため。起票時に過去の類似判断が自動で添えられれば、目的 3「同じ議論の繰り返しを防ぐ」が仕組みとして閉じる。トリガを完了処理に置くのは、ビルドアップサイクル（起票 → … → 完了処理）の既存の節目に相乗りする方が、hook 追加より運用負荷が低いため
  - **代替案 A:** cron による常時 sync → 導入初期には過剰。sync 忘れが頻発したら足せばよい
  - **代替案 B:** git post-commit hook → 全リポジトリへの配布・保守が発生し、明示列挙 config と二重管理になる。却下
- **影響:**
  - 既定 6 キーワード / スラッシュコマンド体系への追加はなし（`/gdr-docs` の内部拡張のみ）
  - [05_CLAUDE_CODE_SETUP](/01_GDR/guide/05_CLAUDE_CODE_SETUP.md) に MCP 登録手順（`claude mcp add --scope user gdr -- ...`）の追記が必要
  - MCP は DB への読み取り専用アクセスとし、書き込み経路は CLI に限定する
- **再検討条件:**
  - sync 忘れによるインデックス鮮度の劣化が頻発 → cron / hook の導入を検討
  - MCP ツールの応答がセッション文脈を圧迫する → 返却フォーマットの要約化・件数制限の見直し

---

## 2. 現状

1. **横断参照の手段がない** — 判断は各リポジトリの `notes/91_gdr/` に閉じており、「これ、前のプロジェクトでも決めなかったか？」に答える手段が運用者の記憶しかない。GDR の目的 3 がプロジェクト横断では未達
2. **二段保管の詳細議論への到達手段が細い** — [006 提案](/91_demo_buildup_documents.md/kaizen/06_アーカイブ機構導入提案.md)の二段保管により Superseded 本文は `notes/_archive/` へ退避されるが、参照手段は「個別ファイルの明示パス指定」のみ。パスを知らない過去判断は実質引けない
3. **字面一致検索しかない** — `rg` では「リフレッシュトークンの持ち方」という問いから `GDR-SEC-003:  refresh_tokens を device にバインド` へ到達できない。判断の検索は語彙一致ではなく意味で引きたい場面が多い
4. **書式検査の手段がない** — 6 フィールド書式の徹底は生成時の AI の注意力頼みで、逸脱を機械的に検出する装置がない
5. **現状規模（2026-07-02 実測）** — 実運用 4 リポジトリ（media_schedules / utilities / foohelpers / mono_flick）、実質 15〜20 レコード。今日の検索ニーズは `rg` で足りる規模だが、レコードの蓄積は方法論の価値そのものであり、記憶層はスケールする前に設計しておく価値がある

---

## 3. 改善案

git を正とする再構築可能な派生インデックス **gdr-index** を導入し、4 つの GDR で「位置づけ」「データモデル」「検索エンジン」「利用面」を定義する。

1. **位置づけ: 三層構造の第三層（長期記憶）**（GDR-META-019）— アクティブ GDR / INDEX 1 行 / DB オンデマンド検索
2. **データモデル: レコード単位・複合キー・フィールド分解**（GDR-META-020）— 実測で裏付けたパース仕様と lint
3. **エンジン: SQLite + FTS5(trigram) + sqlite-vec ハイブリッド**（GDR-META-021）— 日本語対応と運用ゼロの両立
4. **利用面: CLI + MCP（user scope）**（GDR-META-022）— 全セッションからの横断リコール、最終形は起票フェーズ統合

導入は 4 フェーズの段階投入（§4.6）。フェーズ 1（FTS のみ）の時点で grep に対する優位（横断集約・構造化フィルタ・archive 層・書式 lint）が成立し、vector・MCP は独立に積み増せる。

---

## 4. 詳細セクション

### 4.1. 全体像

```
[各プロジェクトの git リポジトリ]                    ← source of truth
  notes/91_gdr/gdr/*.md            (アクティブ)
  notes/91_gdr/INDEX.md            (1 行サマリ — 取り込み除外)
  notes/91_gdr/00_CONTEXT_DEFINITIONS.md (scope 語彙 — 取り込み対象)
  notes/91_gdr/_reference/         (上流スナップショット — 取り込み除外)
  notes/_archive/91_gdr/gdr/*.md   (退避済み — archived=true で取り込み)
        │
        │  gdr-index sync（冪等 / content_hash 差分検知 / lint レポート）
        ▼
[~/.gdr/gdr.db]  SQLite 1 ファイル                 ← 再構築可能な派生物
  records / scopes / links / records_fts / records_vec
        │
        ├── CLI:  gdr-index search "リフレッシュトークン" --status Implemented
        └── MCP:  gdr_search / gdr_get / gdr_list_projects
                  → 全プロジェクトの Claude Code セッションから利用
```

**AI デフォルト除外ルールとの整合:** `notes/_archive/` の除外（GDR-META-016）は「セッション開始時のトークン消費を抑える」ための規定であり、indexer によるバッチ読み取りと MCP 経由のオンデマンド参照はこの目的と衝突しない。むしろ「INDEX で置換関係を把握し、詳細は必要な瞬間だけ引く」という二段保管の設計意図を完成させる第三層になる。

### 4.2. データモデル

```sql
projects(id, name, repo_path, domain)
scopes(project_id, abbr, name, description)        -- 前提定義書の scope テーブル
records(id, project_id, gdr_id,                    -- UNIQUE(project_id, gdr_id)
        prefix, num, title, status,
        decision, reason, impact, revisit_condition,
        source_path, content_hash, archived,
        first_seen_at, last_changed_at)
links(from_record, to_record, kind)                -- supersedes / superseded_by
records_fts   -- FTS5 (tokenize='trigram'): title, decision, reason, impact, revisit_condition
records_vec   -- sqlite-vec vec0: 1 レコード 1 ベクトル
```

- **6 フィールドを列に分解**することで、`WHERE status='Implemented' AND revisit_condition LIKE '%負荷%'` のような**再検討条件レビューの実用クエリ**が成立する
- `content_hash`（正規化テキストの sha256）で変更検知し、**変更レコードのみ再 embed**。upsert は冪等
- `links` により Superseded チェーン（`Superseded by GDR-X-002` / `Supersedes GDR-X-001`）をグラフとして辿れる

### 4.3. 取り込みパイプライン

```
対象発見 → パース → 正規化 → hash 比較 → (変更分のみ) embed → upsert → lint レポート
```

| 工程 | 仕様 |
|---|---|
| 対象発見 | `~/.gdr/config.toml` に repo を明示列挙（`gdr-index add .` で追記）。自動スキャンはしない |
| 対象パス | `notes/91_gdr/**` + `notes/_archive/91_gdr/**`（archived=true）。旧慣行パスは設定で追加可能 |
| 除外 | `_reference/`（サンプル混入を実測で確認済み）、`INDEX.md`（6 フィールドを持たない） |
| パース | `^\*\*GDR-{PREFIX}-{番号}: {要約}\*\*` + 直後の `- **status:** ...` 6 フィールド。寛容パース |
| lint | フィールド欠落・status 不正値・Superseded の相互リンク欠落を警告として一覧出力 |
| 消滅検知 | ソースから消えたレコードは archive 側で再発見できれば archived=true、どこにもなければ tombstone |

**lint の副産物価値:** 取り込みのたびに全プロジェクトの書式逸脱が一覧化されるため、gdr-index は検索基盤であると同時に**書式のリファレンス実装 + 品質装置**として機能する。

### 4.4. 検索 — 日本語対応とハイブリッド

- **全文検索:** FTS5 の `trigram` トークナイザ。標準の unicode61 は日本語を分かち書きできないため、ここが日本語 FTS 成立の要。部分一致（「認証」「デフォルト窓」）が機能する
- **意味検索:** sqlite-vec の KNN。embed 対象は `タイトル + 決定 + 理由 + 再検討条件` の連結 1 ベクトル
- **融合:** RRF（`score = Σ 1/(60 + rank)`）で両者を統合し、SQL フィルタ（project / status / scope / prefix / archived）を適用

クエリ例:

```bash
gdr-index search "セッション管理 認証方式"              # 横断ハイブリッド検索
gdr-index search --project foohelpers --status Implemented --scope sec "トークン"
gdr-index search --field revisit_condition "スケール"    # 再検討条件レビュー
gdr-index show foohelpers GDR-SEC-003                    # 全文 + supersede チェーン
gdr-index lint                                           # 書式逸脱の横断レポート
```

### 4.5. MCP サーバ

```
gdr_search(query, project?, scope?, status?, k=5)  → ハイブリッド検索結果（要約形式）
gdr_get(project, gdr_id)                           → レコード全文 + supersede チェーン
gdr_list_projects()                                → プロジェクト一覧と scope/PREFIX 語彙
```

- 登録: `claude mcp add --scope user gdr -- uvx gdr-index mcp`（ユーザスコープ → 全プロジェクトのセッションで有効）
- DB へは**読み取り専用**。書き込み（sync）は CLI 経路に限定し、セッション側から DB が壊れる経路を作らない
- 返却は「gdr_id / project / title / status / scope / 決定の先頭」の要約形式とし、全文は `gdr_get` で明示的に引く（セッション文脈の圧迫を防ぐ）

**最終形（フェーズ 4）:** `/gdr-flow` の起票フェーズで `gdr_search` を自動実行し、新 GDR ドラフトに「過去の類似判断」セクションを添える。ここまで到達すると、検索基盤がビルドアップサイクルに組み込まれ、判断の質を上げるループが閉じる。

### 4.6. 段階導入

| フェーズ | 内容 | 出せる価値 | 目安 |
|---|---|---|---|
| 1 | parser + SQLite + FTS5(trigram) + CLI | 横断集約・構造化フィルタ・archive 層・書式 lint | 半日 |
| 2 | Embedder IF + sqlite-vec + RRF | 意味検索（ハイブリッド完成） | 半日 |
| 3 | MCP サーバ + user scope 登録 | 全セッションからの横断リコール | 数時間 |
| 4 | サイクル統合（起票時自動照会 / 再検討条件レビュー / INDEX 突合 lint） | ループが閉じる | 順次 |

フェーズ間に依存はあるが、各フェーズ単独でリリース可能。embedding の選定議論（§5-2）がフェーズ 1 をブロックしない構成にしてある。

---

## 5. 検討課題

1. **ツールの置き場所（本リポジトリ同居 vs 別リポジトリ）**
   - 解決策: **別リポジトリ `gdr-index` を推奨**。本リポジトリは Docsify 文書サイトであり、コードの CI・パッケージ配布（uvx 実行）と混ぜると構成が濁る。本リポジトリ側は [05. 推奨ツール導入提案](/91_demo_buildup_documents.md/kaizen/05_推奨ツール導入提案.md)の系譜として、ガイドから参照を張る（方法論の公開ストーリー「GDR at scale」はリンクで成立する）
   - → フェーズ 0 の合意事項。同居希望の場合は `tools/` 配下の構成案を再提示
2. **embedding モデルの最終選定（bge-m3 / ruri 系 / API）**
   - 解決策: Embedder IF を先に切り、フェーズ 2 で実レコードを使った日本語検索精度の実測比較で決める。モデル変更は `rebuild` 一発で移行可能な設計のため、初期選定の重みは低い
   - → フェーズ 2 のタスクとして実行計画に追加済み
3. **対象リポジトリの管理方式**
   - 解決策: config 明示列挙（`gdr-index add .`）。ディレクトリ自動スキャンは予測不能なゴミ（クローンした他人のリポジトリ等）を拾うため採用しない
   - → GDR-META-022 の仕様として確定
4. **DB の置き場**
   - 解決策: `~/.gdr/gdr.db`。派生物のため git 管理・バックアップとも不要。config（`~/.gdr/config.toml`)のみ dotfiles 管理の対象になり得る
   - → 仕様として明示
5. **旧慣行パス（`notes/gdr/` / `documents/decisions/`）への対応**
   - 解決策: 現存 4 リポジトリはすべて `notes/91_gdr/` のため、フェーズ 1 は標準パスのみ対応。対象パスは config で拡張可能にしておき、旧慣行プロジェクトが現れた時点で追加
   - → YAGNI として先送り

---

## 6. 実行計画

### 6.1. タスク一覧

| # | タスク | 根拠 GDR | 依存 | ステータス |
|---|---|---|---|---|
| 0.1 | 本提案のレビュー → 反映 → 合意（GDR 019〜022 の status 確定） | 019〜022 | — | 未着手 |
| 0.2 | `gdr-index` リポジトリ作成（置き場所合意後） | GDR-META-019 | 0.1 | 未着手 |
| 1.1 | パーサ + lint 実装（除外規則・寛容パース・6 フィールド分解） | GDR-META-020 | 0.2 | 未着手 |
| 1.2 | SQLite スキーマ + 冪等 upsert（content_hash 差分検知） | GDR-META-020 | 1.1 | 未着手 |
| 1.3 | FTS5(trigram) + search / show CLI | GDR-META-021 | 1.2 | 未着手 |
| 1.4 | config（repo 列挙）+ sync / rebuild / lint CLI | GDR-META-022 | 1.2 | 未着手 |
| 2.1 | Embedder IF + ローカル実装（Ollama 等） | GDR-META-021 | 1.4 | 未着手 |
| 2.2 | sqlite-vec 統合 + RRF ハイブリッド検索 | GDR-META-021 | 2.1 | 未着手 |
| 2.3 | embedding モデル実測比較 → 既定モデル確定 | GDR-META-021 | 2.2 | 未着手 |
| 3.1 | MCP サーバ実装（gdr_search / gdr_get / gdr_list_projects、読み取り専用） | GDR-META-022 | 1.4 | 未着手 |
| 3.2 | 05_CLAUDE_CODE_SETUP に MCP 登録手順を追記（本リポジトリ側） | GDR-META-022 | 3.1 | 未着手 |
| 4.1 | `/gdr-docs` 完了処理へ sync 統合（user-level コマンド更新） | GDR-META-022 | 1.4 | 未着手 |
| 4.2 | `/gdr-flow` 起票フェーズへ類似判断自動照会を統合 | GDR-META-022 | 3.1 | 未着手 |
| 4.3 | 再検討条件レビューコマンド（`--field revisit_condition` の定型化） | GDR-META-020 | 1.3 | 未着手 |
| 4.4 | INDEX 突合 lint（INDEX.md とレコード実体の整合検査） | GDR-META-020 | 1.4 | 未着手 |

### 6.2. フェーズ詳細

#### フェーズ 0: 合意・準備

**目的:** 文書 → レビュー → 合意の順序を守り、置き場所（§5-1）を確定してから実装に入る。

- [ ] 0.1 本提案のレビューと合意（`レビュー：` → `レビュー反映：` → 合意）
- [ ] 0.2 `gdr-index` リポジトリ作成

#### フェーズ 1: FTS 検索基盤（grep 超え）

**目的:** SQLite + FTS5(trigram) + CLI で「横断集約・構造化フィルタ・archive 層・書式 lint」を成立させる。

- [ ] 1.1 パーサ + lint — `_reference/` 除外、寛容パース、フィールド分解
- [ ] 1.2 スキーマ + 冪等 upsert — 複合キー、content_hash
- [ ] 1.3 FTS5(trigram) + search / show
- [ ] 1.4 config + sync / rebuild / lint

#### フェーズ 2: 意味検索（ハイブリッド完成）

**目的:** Embedder IF を切り、実レコードでモデルを実測選定して RRF ハイブリッドを完成させる。

- [ ] 2.1 Embedder IF + ローカル実装
- [ ] 2.2 sqlite-vec + RRF
- [ ] 2.3 モデル実測比較 → 確定

#### フェーズ 3: MCP 統合

**目的:** 全プロジェクトの Claude Code セッションから横断リコールを可能にする。

- [ ] 3.1 MCP サーバ（読み取り専用）
- [ ] 3.2 05_CLAUDE_CODE_SETUP へ登録手順追記

#### フェーズ 4: ビルドアップサイクルへの統合

**目的:** 検索基盤をサイクルに組み込み、「起票時に過去の類似判断が自動で引ける」ループを閉じる。

- [ ] 4.1 `/gdr-docs` 完了処理へ sync 統合
- [ ] 4.2 `/gdr-flow` 起票フェーズへ類似判断照会
- [ ] 4.3 再検討条件レビューの定型化
- [ ] 4.4 INDEX 突合 lint

### 6.3. 進捗サマリー

| フェーズ | タスク数 | 完了 | 残 | コミット |
|---|---|---|---|---|
| 0 | 2 | 0 | 2 | — |
| 1 | 4 | 0 | 4 | — |
| 2 | 3 | 0 | 3 | — |
| 3 | 2 | 0 | 2 | — |
| 4 | 4 | 0 | 4 | — |

---

## 7. ふりかえり

> 起票時点（2026-07-02）の記録。実装フェーズの完了ごとに追記する。

### 7.1. 観察された傾向

1. **過剰設計の圧縮** — 設計対話の初期段階で、サーバ型 DB（pgvector / Qdrant）・形態素解析トークナイザ・git hook / 常駐デーモンによる自動 sync をいずれも「現規模に対して過剰」として却下済み。embedding もローカル既定とし、API 契約を増やさない側に倒した。「小さく作って段階投入」が本提案の背骨
2. **実装からの発見（起票前の実測）** — 起票に先立つ実測で、`_reference/` サンプル混入（除外ルールの必然性）と全リポジトリでの `GDR-META-001` 重複（複合キーの必然性）を発見。**実測が仕様を作った**好例で、GDR-META-020 の理由欄に実測日付きで記録した
3. **フレームワークの自己進化** — 本提案は [006 二段保管](/91_demo_buildup_documents.md/kaizen/06_アーカイブ機構導入提案.md)（GDR-META-016/018）の再検討条件「横断レビュー時に過去判断を参照したい頻度が高い」に先回りで応答する提案であり、GDR の再検討条件が次の改善提案の起点になるという設計どおりの連鎖が起きている

### 7.2. 次回への申し送り

- 最初のブロッカーは §5-1（置き場所）の合意。レビュー時に真っ先に確定させる
- フェーズ 1 完了時に「grep との差」を実運用で体感評価し、フェーズ 2 以降の優先度を再判定する
- フェーズ 2 で trigram の日本語検索精度を実測し、不足なら GDR-META-021 の再検討条件（形態素トークナイザ）を発動
- sync 運用が半年定着しなければ GDR-META-019 の再検討条件（廃止検討）に該当することを忘れない
