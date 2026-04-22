# Getting Started with GDR

GDR（General Decision Record）を最短で始めるためのガイドです。

## 前提

- AI コーディングツール（Claude Code、Cursor、GitHub Copilot など）が使える環境
- Git リポジトリが初期化済みのプロジェクト

## Step 1: リポジトリを配置する

プロジェクトに合った方法で GDR のドキュメントを参照・取り込みます。

**方法 A: サイトを参照する（推奨）**

[GDR ドキュメントサイト](https://yoshinag.github.io/general-decision-record/) を参照しながら導入を進めます。リポジトリへの取り込みは不要です。

```bash
# 方法 B: クローンして参照用に配置
git clone https://github.com/yoshinag/general-decision-record.git

# 方法 C: 必要なファイルだけダウンロード
# テンプレートとガイドを手動でコピー
```

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

- **前提定義書**（[T1 テンプレート](../templates/T1_CONTEXT_DEFINITIONS.md)ベース）
- プロジェクトに適した **scope** と **PREFIX**
- ディレクトリ構成
- CLAUDE.md の短縮キーワード設定

詳細: [ローカライズ初回プロンプトガイド](03_FIRST_PROMPT_GUIDE.md)

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
| `改善提案：{タイトル}` | [T2 テンプレート](../templates/T2_BUILDUP_RECORD.md)に従って改善提案文書を生成 |
| `レビュー：{ファイル名}` | 同位置に `{ファイル名}_reviewed` としてレビュー文書を生成 |
| `レビュー反映：{ファイル名}` | `_reviewed` の内容を元ファイルに組み込み、`_reviewed` を削除 |
| `バグレポート：{ファイル名}` | `bug_fix_report/` 配下にバグレポートを作成 |

## GDR の書式（早見表）

```markdown
**GDR-{PREFIX}-{番号}: {決定の要約}**

- **status:** Proposed | Approved | Implemented | Superseded
- **scope:** {scope をカンマ区切り}
- **決定:** 何をするか（または何をしないか）
- **理由:** なぜその判断に至ったか（代替案との比較、トレードオフ）
- **影響:** この決定がもたらす具体的な影響
- **再検討条件:** どのような状況変化があれば判断を見直すか
```

## 参考文書

| 文書 | 内容 |
|---|---|
| [GDR 仕様](../01_GENERAL_DECISION_RECORD.md) | GDR の定義・目的・書式 |
| [AI-Driven GDR ビルドアップ](../02_AI_DRIVEN_GDR_BUILDUP.md) | ビルドアップの定義・サイクル・原則 |
| [scope ガイド](01_SCOPE_GUIDE.md) | scope の設計ガイドライン |
| [PREFIX ガイド](02_PREFIX_GUIDE.md) | PREFIX の設計ガイドライン |
| [プロンプトガイド](04_PROMPT_GUIDE.md) | 推奨プロンプト集 |
