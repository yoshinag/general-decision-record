# Claude Code セットアップガイド

Claude Code を使う場合、`~/.claude/` 配下に **user-level の global config** を配置すると、すべてのプロジェクトで GDR 方法論と短縮キーワード / スラッシュコマンドが自動有効になる。

本ガイドは [00. Getting Started](/01_GDR/guide/00_GETTING_STARTED.md) Step 2.0 から呼ばれる詳細仕様。Cursor / GitHub Copilot などを使う場合は不要。

## 配置するファイル（6 ファイル）

| 配置パス | 役割 |
|---|---|
| `~/.claude/CLAUDE.md` | user-level の常駐指示書。全プロジェクト横断で自動読み込み |
| `~/.claude/commands/gdr-kaizen.md` | スラッシュコマンド `/gdr-kaizen <タイトル>` の定義 |
| `~/.claude/commands/gdr-review.md` | スラッシュコマンド `/gdr-review <ファイル名>` の定義 |
| `~/.claude/commands/gdr-apply-review.md` | スラッシュコマンド `/gdr-apply-review <ファイル名>` の定義 |
| `~/.claude/commands/gdr-bug-report.md` | スラッシュコマンド `/gdr-bug-report <識別子>` の定義 |
| `~/.claude/commands/gdr-flow.md` | スラッシュコマンド `/gdr-flow <作業指示>` の定義 |

## `~/.claude/CLAUDE.md` の仕様

最低限、以下のセクションを含める:

1. **Git 運用ルール（横断）** — commit / push の既定の挙動。プロジェクト固有の `.claude/settings.json` 側 hook と矛盾する場合はプロジェクト側を優先する旨を明記。
2. **GDR 方法論セクション** — 以下を含む:
   - **いつ提案・適用するか** — 新規リポ立ち上げ / 「設計判断」「方針決定」「ADR」等のキーワード検知 / 既存 GDR ディレクトリ検知時
   - **初回導入時の標準手順** — Getting Started Step 1〜2 の流れ（標準ディレクトリ構成の作成、上流ファイル取得、ローカライズ初回プロンプト実施、scope/PREFIX 合意、前提定義書 / INDEX / 最初の GDR-META 生成）
   - **既定の短縮キーワード** — `改善提案：` / `レビュー：` / `レビュー反映：` / `バグレポート：` / `一気通貫：` の 5 種と、対応するスラッシュコマンドの対応表
   - **不可侵ルール** — 判断本質の変更は新 GDR + `Superseded` / scope・PREFIX 改廃は GDR-META 経由 / 文書と実装を混ぜない / 自明な実装詳細を GDR 化しない
   - **上流ドキュメントの参照先** — 導入済プロジェクトの `notes/91_gdr/_reference/` 配下にスナップショットがある旨

## `~/.claude/commands/gdr-*.md` の仕様（共通）

Claude Code のスラッシュコマンドは markdown + frontmatter 形式で `~/.claude/commands/` 配下に置く。各ファイルの先頭に以下の frontmatter:

```yaml
---
description: コマンドの一行説明（補完 UI に表示）
argument-hint: <引数の形式>
---
```

本体は markdown で「動作 / 入力 / 出力先 / 例外 / 注意」を記述。`$ARGUMENTS` でコマンド引数を参照できる。

### 各コマンドの仕様

| ファイル | description | argument-hint | 動作の要点 |
|---|---|---|---|
| `gdr-kaizen.md` | GDR T2 形式の改善提案を `notes/20_kaizen/` 配下に生成 | `<タイトル>` | `notes/20_kaizen/{YYYY-MM-DD}_{slug}.md` に T2 構成のドラフト生成。文書のみ生成、実装着手しない |
| `gdr-review.md` | 対象ファイルをセルフレビューし `{filename}_reviewed.md` を生成 | `<ファイル名 or 相対パス>` | 同位置に `{元ファイル名}_reviewed.md` を出力。横断レビューは `notes/91_gdr/review/` 配下。区分 A〜G で整理 |
| `gdr-apply-review.md` | `_reviewed.md` の内容を本体に統合し `_reviewed.md` を削除 | `<元ファイル名 or _reviewed.md ファイル名>` | A / D / E は必ず反映、B / C / F / G は必要に応じて。統合後 `_reviewed.md` を削除し 1 コミット |
| `gdr-bug-report.md` | バグレポートを `notes/80_bug_fix_report/` 配下に生成 | `<識別子 / ファイル名 / 症状概要>` | `notes/80_bug_fix_report/{slug}.md` に 10 項構成（メタ / 症状 / 再現 / 原因 / 影響 / 回避策 / 修正案 / 推奨 / 既知事項 / 次のアクション）で起票 |
| `gdr-flow.md` | 進行状況を確認し GDR ビルドアップサイクルをノンストップで前進 | `<作業指示 or トピック>` | 現在地（会話文脈 / `git log` / `notes/` ファイル状態）を判定し**次フェーズだけ**実行（巻き戻し禁止）。フェーズ: 起票 → セルフレビュー → レビュー反映 → 合意 → GDR 起票 → 実装 → 完了処理 |

> **キーワードとスラッシュコマンドの住み分け:** 短縮キーワード（`改善提案：` 等）は自然文中の流れで使う。スラッシュコマンド（`/gdr-kaizen` 等）は Tab 補完で発見性が必要な場面で使う。両方とも生きている。

## 配置後: Claude Code を一度再起動する

`~/.claude/CLAUDE.md` および `~/.claude/commands/*.md` は **Claude Code の起動時に読み込まれる**。既に Claude Code セッションを開いている場合、ファイルを配置・更新しても自動では反映されない。

配置後は一度セッションを終了してから再起動する:

```
/exit
```

その後 Claude Code を起動し直すと、global config とスラッシュコマンドが有効になる（`/` 入力で `/gdr-*` 系コマンドが補完候補に出れば成功）。
