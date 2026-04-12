# CLAUDE.md

## プロジェクト概要

GDR（General Decision Record）を説明するための文書管理リポジトリ。

## ディレクトリ構成

```
documents/
├── 01_GDR/markdown/          # GDR フレームワーク文書
│   ├── 01_GENERAL_DECISION_RECORD.md   # GDR 仕様
│   ├── 02_AI_DRIVEN_GDR_BUILDUP.md     # AI-Driven ビルドアップ
│   ├── _sidebar.md                      # Docsify サイドバー定義
│   ├── guide/                           # ガイドライン
│   │   ├── 01_SCOPE_GUIDE.md
│   │   └── 02_PREFIX_GUIDE.md
│   ├── templates/                       # テンプレート
│   │   ├── T1_CONTEXT_DEFINITIONS.md
│   │   └── T2_BUILDUP_RECORD.md
├── 91_demo/                   # デモ・改善提案
│   └── kaizen/
docs/                          # Docsify サイト（GitHub Pages 用）
└── index.html
```

## GDR 書式

GDR レコードは以下の 5 フィールドを**すべて**含めること:

```markdown
**GDR-{PREFIX}-{番号}: {決定の要約}**

- **scope:** {scope の略記をカンマ区切り}
- **決定:** 何をするか（または何をしないか）
- **理由:** なぜその判断に至ったか（代替案との比較、トレードオフ）
- **影響:** この決定がもたらす具体的な影響
- **再検討条件:** どのような状況変化があれば判断を見直すか
```

## 採番ルール

- **ファイル名:** `{連番}_{タイトル}.md`（連番は 2 桁ゼロ埋め: `01_`, `02_`）。テンプレートは `T{番号}_` 形式
- **GDR レコード ID:** `GDR-{PREFIX}-{番号}`（番号は PREFIX 内の 3 桁ゼロ埋め連番: `001`, `002`）
- **サブセクション:** `{ファイル連番}.{枝番}`（例: `001.1`, `001.2`）
- **リネーム時の連動更新:** ファイルをリネーム・採番変更した場合、以下をすべて更新すること:
  - ファイル内の見出し番号
  - 他ドキュメントからの相互リンク
  - `README.md` のインデックス
  - `documents/01_GDR/markdown/_sidebar.md`

## Docsify 運用

- `docs/index.html` が Docsify のエントリポイント。markdown は `documents/01_GDR/markdown/` から直接読み込む
- markdown ファイルの**追加・削除・リネーム**時は `documents/01_GDR/markdown/_sidebar.md` を必ず同期更新する

## コミット規約

- コミットメッセージは**英語**で記述する

## コンテキスト短縮用キーワード

1. **"改善提案\[：|；\][タイトル]":** 「GDR → 実行計画 → ふりかえり」の 3 部構成で文書を生成する。T2 の 1〜4 章（プロジェクト概要・前提定義書・GDR_INDEX 配置先・サイクル記録）は省略する。
2. **"レビュー\[：|；\][ファイル名]":** 同位置にファイル名_reviewedという形式でレビュー内容を保存する。
3. **"レビュー反映\[：|；\][ファイル名|]":** 元のファイル名+_reviewedという形式の文書の内容を把握、検討、整理して元のファイルに組み込む。反映後に_reviewedファイルは削除する。
4. **"バグレポート\[：|；\][ファイル名|]":** documents/bug_fix_report/ 配下に直近のバグ内容を整理したレポート文書を作成する
