# Getting Started with GDR

> 前提知識: [01. GDR とは](/01_GDR/01_GENERAL_DECISION_RECORD.md)（書式と基本概念）/ [02. AI-Driven GDR ビルドアップ](/01_GDR/02_AI_DRIVEN_GDR_BUILDUP.md)（サイクルと原則）。本ガイドは規範文書を読まずに最短で導入したい読者向けの実践導線。

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

---

> **以降の説明は方法 A（サイト参照）を前提とする。**
> Step 2.0 の配置プロンプトおよび Step 2.1 の完全版プロンプトは、AI が
> `https://yoshinag.github.io/general-decision-record/` 上のドキュメントを
> 直接フェッチできることを前提に書かれている。方法 B / C を選んだ場合は、
> URL 参照部分をローカルファイルパス（クローン先 / コピー先）に読み替えること。

## Step 2: ローカライズ初回プロンプトを実行する

### Step 2.0: （Claude Code 利用者のみ）global config を配置する

Claude Code を使う場合、`~/.claude/` 配下に user-level の global CLAUDE.md と 5 つの `gdr-*` スラッシュコマンドを置くと、すべてのプロジェクトで GDR 方法論と短縮キーワード / スラッシュコマンドが自動有効になる。Step 2.1 以降は AI が GDR 文脈を把握した状態で進む。

> Cursor / GitHub Copilot などを使う場合は本節をスキップしてよい。

#### 配置プロンプト

新規 Claude Code セッションで以下をそのまま送る:

```
GDR の Claude Code セットアップを行う。以下の仕様に従って ~/.claude/ 配下に
user-level の global config を配置して。

参照: https://yoshinag.github.io/general-decision-record/#/ja/01_GDR/guide/05_CLAUDE_CODE_SETUP

配置対象:
- ~/.claude/CLAUDE.md（既存があれば GDR 方法論セクションを追記）
- ~/.claude/commands/gdr-kaizen.md
- ~/.claude/commands/gdr-review.md
- ~/.claude/commands/gdr-apply-review.md
- ~/.claude/commands/gdr-bug-report.md
- ~/.claude/commands/gdr-flow.md

要件:
- 各ファイルは 05_CLAUDE_CODE_SETUP.md の仕様（frontmatter / 動作 /
  出力先 / 注意）を満たすこと
- ~/.claude/CLAUDE.md に既存内容がある場合は上書きせず、GDR 方法論
  セクションを末尾に追記。Git 運用ルールが既にあれば重複させない
- 配置後、ファイル一覧と各ファイルの先頭 5 行を表示して確認させて

完了したら「/exit して再起動してください」と教えて。
```

配置後は `/exit` で Claude Code を一度再起動する（global config と スラッシュコマンドは**起動時にのみ**読み込まれる）。再起動後、`/` 入力で `/gdr-*` が補完候補に出れば成功。

各ファイルの詳細仕様は **[05. Claude Code セットアップ](/01_GDR/guide/05_CLAUDE_CODE_SETUP.md)** を参照。

### Step 2.1: ローカライズ初回プロンプトを実行する

AI に以下のプロンプトを送ります。プロジェクト情報を埋めてください。

> **前提:** このプロンプトは AI が GDR 方法論を把握していることを前提にしている。
> - **Step 2.0 を実施した Claude Code 利用者:** global CLAUDE.md で AI が常時 GDR を把握しているため、以下のプロンプトをそのまま送ってよい
> - **それ以外（Step 2.0 未実施 / Cursor / Copilot 等）:** プロンプト冒頭の参照 URL を AI に読ませる必要がある。下記の **完全版プロンプト** を使うこと

#### 短縮版（Step 2.0 実施済み Claude Code 向け）

```
GDRを導入する。以下のプロジェクト情報をもとに前提定義書を作成して。

プロジェクト名: {プロジェクト名}
ドメイン: {ソフトウェア / 製造 / 医療 / 金融 / その他}
概要: {プロジェクトの概要を1〜3文で}
主な関心事: {例: API設計、画面UI、運用ルール、コスト管理 など}
GDR出力先: notes/{01_spec,05_knowledge,10_things,20_kaizen,80_bug_fix_report,91_gdr,99_other}/
```

#### 完全版（Step 2.0 未実施 / 他ツール向け）

冒頭で GDR 仕様を AI に読み込ませてから本題に入る:

```
GDR (General Decision Record) をこのプロジェクトに導入したい。
まず以下のドキュメントを読んで GDR 方法論を把握して。

- GDR 仕様: https://yoshinag.github.io/general-decision-record/#/ja/01_GDR/01_GENERAL_DECISION_RECORD
- ローカライズ初回プロンプトガイド: https://yoshinag.github.io/general-decision-record/#/ja/01_GDR/guide/03_FIRST_PROMPT_GUIDE
- T1 前提定義書テンプレート: https://yoshinag.github.io/general-decision-record/#/ja/01_GDR/templates/T1_CONTEXT_DEFINITIONS
- scope ガイド: https://yoshinag.github.io/general-decision-record/#/ja/01_GDR/guide/01_SCOPE_GUIDE
- PREFIX ガイド: https://yoshinag.github.io/general-decision-record/#/ja/01_GDR/guide/02_PREFIX_GUIDE

その上で、以下のプロジェクト情報をもとに T1 テンプレートに従って前提定義書
（notes/91_gdr/00_CONTEXT_DEFINITIONS.md）を作成して。

プロジェクト名: {プロジェクト名}
ドメイン: {ソフトウェア / 製造 / 医療 / 金融 / その他}
概要: {プロジェクトの概要を1〜3文で}
主な関心事: {例: API設計、画面UI、運用ルール、コスト管理 など}
GDR出力先: notes/{01_spec,05_knowledge,10_things,20_kaizen,80_bug_fix_report,91_gdr,99_other}/

合わせて以下も提案して:
- プロジェクトに適した scope（影響領域の分類）と PREFIX（ドメイン識別子）
- 短縮キーワード設定（改善提案：/レビュー：/レビュー反映：/バグレポート：）
- リポジトリ直下の CLAUDE.md ドラフト
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
