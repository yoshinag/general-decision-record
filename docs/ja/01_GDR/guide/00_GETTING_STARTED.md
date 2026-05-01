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

AI に以下のプロンプトを送ります。プロジェクト情報を埋めてください。

```
GDRを導入する。以下のプロジェクト情報をもとに前提定義書を作成して。

プロジェクト名: {プロジェクト名}
ドメイン: {ソフトウェア / 製造 / 医療 / 金融 / その他}
概要: {プロジェクトの概要を1〜3文で}
主な関心事: {例: API設計、画面UI、運用ルール、コスト管理 など}
GDR出力先: {例: documents/decisions/ documents/kaizen/}
```

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
| `改善提案：{タイトル}` | [T2 テンプレート](/01_GDR/templates/T2_BUILDUP_RECORD.md)に従って改善提案文書を生成 |
| `レビュー：{ファイル名}` | 同位置に `{ファイル名}_reviewed` としてレビュー文書を生成 |
| `レビュー反映：{ファイル名}` | `_reviewed` の内容を元ファイルに組み込み、`_reviewed` を削除 |
| `バグレポート：{ファイル名}` | `bug_fix_report/` 配下にバグレポートを作成 |

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
