# GDR（General Decision Record）

**GDR** は、ADR（Architectural Decision Record）を拡張し、アーキテクチャに限らず**あらゆる意思決定**を統一フォーマットで記録するフレームワークです。

**AI-Driven GDR ビルドアップ**は、AI との対話を通じて GDR を反復的に積み上げながらプロジェクトを前進させる開発プロセスです。

## ドキュメント

| # | 文書 | 内容 |
|---|---|---|
| 01 | [GDR 仕様](docs/01_GDR/01_GENERAL_DECISION_RECORD.md) | GDR の定義・目的・書式・scope と PREFIX |
| 02 | [AI-Driven GDR ビルドアップ](docs/01_GDR/02_AI_DRIVEN_GDR_BUILDUP.md) | ビルドアップの定義・サイクル・原則・導入方法 |
| G-01 | [scope ガイド](docs/01_GDR/guide/01_SCOPE_GUIDE.md) | scope ガイドライン（共通 + 業種別） |
| G-02 | [PREFIX ガイド](docs/01_GDR/guide/02_PREFIX_GUIDE.md) | PREFIX ガイドライン（共通 + 業種別） |
| G-03 | [ローカライズ初回プロンプト](docs/01_GDR/guide/03_FIRST_PROMPT_GUIDE.md) | 導入時の最初のプロンプト設計 |
| G-04 | [プロンプトガイド](docs/01_GDR/guide/04_PROMPT_GUIDE.md) | 推奨プロンプト集・短縮キーワード |
| T1 | [前提定義書テンプレート](docs/01_GDR/templates/T1_CONTEXT_DEFINITIONS.md) | Context Definitions テンプレート |
| T2 | [ビルドアップ記録テンプレート](docs/01_GDR/templates/T2_BUILDUP_RECORD.md) | ビルドアップ記録・改善提案テンプレート |

## クイックスタート

1. このリポジトリを配置（clone / fork / submodule / download）
2. プロジェクトに沿った内容で各 GDR 文書のローカライズを行う
   - 03_FIRST_PROMPT_GUIDE.mdを参考に最初のプロンプトを実行する
3. 「要件を伝える → AI が GDR を構造化 → レビュー → 実装」のサイクルを回す
4. [ビルドアップ記録](docs/01_GDR/templates/T2_BUILDUP_RECORD.md)にサイクルの流れを追記していく

詳細は [AI-Driven GDR ビルドアップ § 導入方法](docs/01_GDR/02_AI_DRIVEN_GDR_BUILDUP.md#9-導入方法) を参照してください。

## ディレクトリ構成

```
docs/                                      # Docsify サイト（GitHub Pages 用）
├── index.html                             # Docsify エントリポイント
├── _sidebar.md                            # Docsify サイドバー定義
├── 01_GDR/                                # GDR フレームワーク文書
│   ├── 01_GENERAL_DECISION_RECORD.md      # GDR 仕様
│   ├── 02_AI_DRIVEN_GDR_BUILDUP.md        # AI-Driven ビルドアップ
│   ├── guide/                             # ガイドライン
│   │   ├── 01_SCOPE_GUIDE.md
│   │   ├── 02_PREFIX_GUIDE.md
│   │   ├── 03_FIRST_PROMPT_GUIDE.md
│   │   └── 04_PROMPT_GUIDE.md
│   └── templates/                         # テンプレート
│       ├── T1_CONTEXT_DEFINITIONS.md      # 前提定義書
│       └── T2_BUILDUP_RECORD.md           # ビルドアップ記録・改善提案
├── 91_demo_buildup_documents.md/          # デモ・改善提案
│   └── kaizen/
```
