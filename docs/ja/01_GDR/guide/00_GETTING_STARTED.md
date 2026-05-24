# Getting Started with GDR

GDR（General Decision Record）を最短で始めるためのガイドです。

## 前提

- AI コーディングツール（Claude Code、Cursor、GitHub Copilot など）が使える環境
- Git リポジトリが初期化済みのプロジェクト

## Step 1: リポジトリを配置する

プロジェクトに合った方法で GDR のドキュメントを参照・取り込みます。

### 方法 A: サイトを参照する（推奨）

[GDR ドキュメントサイト](https://yoshinag.github.io/general-decision-record/) を参照しながら導入を進めます。リポジトリへの取り込みは不要です。

### 方法 B: クローンして参照用に配置

```bash
git clone https://github.com/yoshinag/general-decision-record.git
```

### 方法 C: 必要なファイルだけダウンロード

テンプレート（T1/T2）とガイドを手動でコピーします。CLAUDE.md にコンテキスト短縮用キーワードを追記する場合は、本リポジトリの記述例を参照してください。

## Step 2: ローカライズ初回プロンプトを実行する

### Step 2.0: （Claude Code 利用者のみ）global config を配置する

Claude Code を使う場合、`~/.claude/` 配下に global config を置いておくと、**すべてのプロジェクトで** GDR 方法論と短縮キーワード / スラッシュコマンドが自動有効になる。一度配置すれば、以降の Step 2.1 以降は AI が GDR 文脈を把握した状態で進む。

> Cursor / GitHub Copilot などを使う場合は本節をスキップしてよい。

#### 配置するファイル（6 ファイル）

| 配置パス | 役割 |
|---|---|
| `~/.claude/CLAUDE.md` | user-level の常駐指示書。全プロジェクト横断で自動読み込み |
| `~/.claude/commands/gdr-kaizen.md` | スラッシュコマンド `/gdr-kaizen <タイトル>` の定義 |
| `~/.claude/commands/gdr-review.md` | スラッシュコマンド `/gdr-review <ファイル名>` の定義 |
| `~/.claude/commands/gdr-apply-review.md` | スラッシュコマンド `/gdr-apply-review <ファイル名>` の定義 |
| `~/.claude/commands/gdr-bug-report.md` | スラッシュコマンド `/gdr-bug-report <識別子>` の定義 |
| `~/.claude/commands/gdr-flow.md` | スラッシュコマンド `/gdr-flow <作業指示>` の定義 |

#### `~/.claude/CLAUDE.md` の仕様

最低限、以下のセクションを含める:

1. **Git 運用ルール（横断）** — commit / push の既定の挙動。プロジェクト固有の `.claude/settings.json` 側 hook と矛盾する場合はプロジェクト側を優先する旨を明記。
2. **GDR 方法論セクション** — 以下を含む:
   - **いつ提案・適用するか** — 新規リポ立ち上げ / 「設計判断」「方針決定」「ADR」等のキーワード検知 / 既存 GDR ディレクトリ検知時
   - **初回導入時の標準手順** — 本ガイド Step 1〜2 の流れ（標準ディレクトリ構成の作成、上流ファイル取得、ローカライズ初回プロンプト実施、scope/PREFIX 合意、前提定義書 / INDEX / 最初の GDR-META 生成）
   - **既定の短縮キーワード** — `改善提案：` / `レビュー：` / `レビュー反映：` / `バグレポート：` / `一気通貫：` の 5 種と、対応するスラッシュコマンドの対応表
   - **不可侵ルール** — 判断本質の変更は新 GDR + `Superseded` / scope・PREFIX 改廃は GDR-META 経由 / 文書と実装を混ぜない / 自明な実装詳細を GDR 化しない
   - **上流ドキュメントの参照先** — 導入済プロジェクトの `notes/91_gdr/_reference/` 配下にスナップショットがある旨

#### `~/.claude/commands/gdr-*.md` の仕様（共通）

Claude Code のスラッシュコマンドは markdown + frontmatter 形式で `~/.claude/commands/` 配下に置く。各ファイルの先頭に以下の frontmatter:

```yaml
---
description: コマンドの一行説明（補完 UI に表示）
argument-hint: <引数の形式>
---
```

本体は markdown で「動作 / 入力 / 出力先 / 例外 / 注意」を記述。`$ARGUMENTS` でコマンド引数を参照できる。

##### 各コマンドの仕様

| ファイル | description | argument-hint | 動作の要点 |
|---|---|---|---|
| `gdr-kaizen.md` | GDR T2 形式の改善提案を `notes/20_kaizen/` 配下に生成 | `<タイトル>` | `notes/20_kaizen/{YYYY-MM-DD}_{slug}.md` に T2 構成のドラフト生成。文書のみ生成、実装着手しない |
| `gdr-review.md` | 対象ファイルをセルフレビューし `{filename}_reviewed.md` を生成 | `<ファイル名 or 相対パス>` | 同位置に `{元ファイル名}_reviewed.md` を出力。横断レビューは `notes/91_gdr/review/` 配下。区分 A〜G で整理 |
| `gdr-apply-review.md` | `_reviewed.md` の内容を本体に統合し `_reviewed.md` を削除 | `<元ファイル名 or _reviewed.md ファイル名>` | A / D / E は必ず反映、B / C / F / G は必要に応じて。統合後 `_reviewed.md` を削除し 1 コミット |
| `gdr-bug-report.md` | バグレポートを `notes/80_bug_fix_report/` 配下に生成 | `<識別子 / ファイル名 / 症状概要>` | `notes/80_bug_fix_report/{slug}.md` に 10 項構成（メタ / 症状 / 再現 / 原因 / 影響 / 回避策 / 修正案 / 推奨 / 既知事項 / 次のアクション）で起票 |
| `gdr-flow.md` | 進行状況を確認し GDR ビルドアップサイクルをノンストップで前進 | `<作業指示 or トピック>` | 現在地（会話文脈 / `git log` / `notes/` ファイル状態）を判定し**次フェーズだけ**実行（巻き戻し禁止）。フェーズ: 起票 → セルフレビュー → レビュー反映 → 合意 → GDR 起票 → 実装 → 完了処理 |

> **キーワードとスラッシュコマンドの住み分け:** 短縮キーワード（`改善提案：` 等）は自然文中の流れで使う。スラッシュコマンド（`/gdr-kaizen` 等）は Tab 補完で発見性が必要な場面で使う。両方とも生きている。

#### 配置後: Claude Code を一度再起動する

`~/.claude/CLAUDE.md` および `~/.claude/commands/*.md` は **Claude Code の起動時に読み込まれる**。既に Claude Code セッションを開いている場合、ファイルを配置・更新しても自動では反映されない。

配置後は一度セッションを終了してから再起動する:

```
/exit
```

その後 Claude Code を起動し直すと、global config と スラッシュコマンドが有効になる（`/` 入力で `/gdr-*` 系コマンドが補完候補に出れば成功）。

### Step 2.1: ローカライズ初回プロンプトを実行する

AI に以下のプロンプトを送ります。プロジェクト情報を埋めてください。

```
GDRを導入する。以下のプロジェクト情報をもとに前提定義書を作成して。

プロジェクト名: {プロジェクト名}
ドメイン: {ソフトウェア / 製造 / 医療 / 金融 / その他}
概要: {プロジェクトの概要を1〜3文で}
主な関心事: {例: API設計、画面UI、運用ルール、コスト管理 など}
GDR出力先: notes/{01_spec,05_knowledge,10_things,20_kaizen,80_bug_fix_report,91_gdr,99_other}/
```

> **GDR出力先について:** 上記は推奨標準（`notes/` 直下に番号プレフィックス付き 7 種）。詳細と各ディレクトリの用途は [ローカライズ初回プロンプトガイド §2.2](/01_GDR/guide/03_FIRST_PROMPT_GUIDE.md) を参照。プロジェクト固有の慣行（`documents/decisions/` など）がある場合はそれを優先してよい。

AI が以下を生成・提案します:

- **前提定義書**（[T1 テンプレート](/01_GDR/templates/T1_CONTEXT_DEFINITIONS.md)ベース）
- プロジェクトに適した **scope** と **PREFIX**
- ディレクトリ構成
- CLAUDE.md の短縮キーワード設定

詳細: [ローカライズ初回プロンプトガイド](/01_GDR/guide/03_FIRST_PROMPT_GUIDE.md)

## Step 3: ビルドアップサイクルを回す

GDR ビルドアップの基本サイクル:

```
1. 要件・課題を AI に伝える
2. AI が判断を GDR として構造化（scope / 代替案 / トレードオフを明示）
3. 人間がレビュー・承認・修正
4. 実装に落とす
5. 必要に応じて GDR を更新
   └── 1 に戻る
```

## Step 4: 短縮キーワードを活用する

前提定義書で設定した短縮キーワードで効率的に運用できます。

| キーワード | 動作 |
|---|---|
| `改善提案：{タイトル}` | `notes/20_kaizen/` 配下に [T2 テンプレート](/01_GDR/templates/T2_BUILDUP_RECORD.md) に従って改善提案文書を生成 |
| `レビュー：{ファイル名}` | 同位置に `{ファイル名}_reviewed` としてレビュー文書を生成 |
| `レビュー反映：{ファイル名}` | `_reviewed` の内容を元ファイルに組み込み、`_reviewed` を削除 |
| `バグレポート：{ファイル名}` | `notes/80_bug_fix_report/` 配下にバグレポートを作成 |

> 出力先は推奨標準（[ローカライズ初回プロンプトガイド §2.2](/01_GDR/guide/03_FIRST_PROMPT_GUIDE.md)）に準拠。プロジェクト固有のディレクトリを採用している場合はそちらに読み替える。

## Step 5: 運用ルールを定義する（任意）

GDR は**意思決定の内容**を記録するフレームワークだが、AI コーディングツールとの協働では、判断ではなく**挙動レベルのルール**（コミットの粒度、push の権限、破壊的操作の扱いなど）も明文化しておくとサイクルが安定する。

### よくある運用ルール

- **commit**: 作業単位の完了時に明示指示を待たずに実施してよい / 必ず確認を取る
- **push**: 絶対に実施しない / 明示指示時のみ
- **破壊的操作**: `git reset --hard`、force push、`rm -rf` などは明示指示必須
- **依存追加**: `npm install` / `pip install` などは事前承認が必要

### CLAUDE.md への記述例

```markdown
## 運用ルール

- **commit**: 作業単位の完了時、明示指示を待たずに実施してよい。
- **push**: 絶対に実施しない。ユーザーが明示的に指示した場合のみ許可。
```

### 強制したい場合

CLAUDE.md は AI が「読むべき指示」であり、誤動作の保証はない。重要なルール（特に push 禁止のような破壊的・対外的な操作）は、**ツール側の hook / permission 機能で技術的に強制**するのが確実。

| ツール | 強制手段の例 |
|---|---|
| Claude Code | `.claude/settings.json` の `hooks.PreToolUse`（コマンド検査して deny） / `permissions.deny` |
| Cursor | `.cursor/rules/` での運用ルール記述（モデル順守） |
| GitHub Copilot | リポジトリ Instructions / IDE 側の確認設定 |

各ツールのドキュメントを参照のこと。GDR 自体はツール非依存だが、運用ルールはツールごとに最適な強制手段を選ぶ。

## GDR の書式（早見表）

```markdown
**GDR-{PREFIX}-{番号}: {決定の要約}**

- **status:** Proposed | Implemented | Superseded
- **scope:** {scope をカンマ区切り}
- **決定:** 何をするか（または何をしないか）
- **理由:** なぜその判断に至ったか（代替案との比較、トレードオフ）
- **影響:** この決定がもたらす具体的な影響
- **再検討条件:** どのような状況変化があれば判断を見直すか
```

## 参考文書

| 文書 | 内容 |
|---|---|
| [GDR 仕様](/01_GDR/01_GENERAL_DECISION_RECORD.md) | GDR の定義・目的・書式 |
| [AI-Driven GDR ビルドアップ](/01_GDR/02_AI_DRIVEN_GDR_BUILDUP.md) | ビルドアップの定義・サイクル・原則 |
| [scope ガイド](/01_GDR/guide/01_SCOPE_GUIDE.md) | scope の設計ガイドライン |
| [PREFIX ガイド](/01_GDR/guide/02_PREFIX_GUIDE.md) | PREFIX の設計ガイドライン |
| [プロンプトガイド](/01_GDR/guide/04_PROMPT_GUIDE.md) | 推奨プロンプト集 |
