# 変更履歴

GDR 仕様（`docs/ja/01_GDR/` 配下の仕様・ガイド・テンプレートと、[Claude Code セットアップ仕様](docs/ja/01_GDR/guide/05_CLAUDE_CODE_SETUP.md) が定める user-level config）の版を記録する。

- **版の付け方:** `vMAJOR.MINOR`。導入先が採用するときに**必須の移行項目がある**変更（書式違反化、既存の値の意味の変更）は MAJOR、ない変更は MINOR。移行作業が生じない文言修正等では版を上げない（[kaizen 010](docs/ja/91_demo_buildup_documents.md/kaizen/10_GDR仕様の版管理と最新版通知提案.md) GDR-META-031）
- **各版の記載項目:** 互換性 / 要約と根拠 / 導入先の移行項目（必須・推奨・任意）/ user-level config の更新要否
- **導入先での採用:** 前提定義書の `GDR 仕様: vX.Y` 行で宣言し、版の変更は GDR-META として記録する。`/gdr-upgrade` で差分と移行項目を確認できる

---

## v2.0 — 2026-09-28

- **互換性:** MAJOR（`Proposed` の意味が「合意に至っていない」に狭まる。互換モードにより、前提定義書の宣言を v2.0 に更新するまでは v1.x の解釈で動く）
- **要約:**
  - status を 5 値化（`Accepted` / `Rejected` を追加）。有効 / 失効の区分、遷移、置換の記法（`Superseded by` / `(supersedes …)`）と切替時点（旧の失効 = 新の `Accepted`、旧の退避 = 新の `Implemented`）、撤回時の復帰
  - AI の参照の規律（失効 GDR を根拠にしない・後継を末端までたどる・`Rejected` は採らない理由としてのみ引用）
  - 任意フィールド「理由の出所」（`human` / `ai-reviewed` / `ai`。AI 起票時は必須、不明な理由を補完しない）
  - 仕様の版管理（本 CHANGELOG・タグ）、前提定義書での版の宣言、互換モード、`/gdr-upgrade`
  - 根拠: [kaizen 009](docs/ja/91_demo_buildup_documents.md/kaizen/09_GDR信頼性強化提案.md)（GDR-META-028〜030）、[kaizen 010](docs/ja/91_demo_buildup_documents.md/kaizen/10_GDR仕様の版管理と最新版通知提案.md)（GDR-META-031〜034）、[バグレポート 02](docs/ja/bug_fix_report/02_status_5値化の配備による旧版導入先の互換性破れ.md)
- **導入先の移行項目:**
  - 必須: `Proposed` のまま残っている GDR の棚卸し（合意済み → `Accepted`、不採用 → `Rejected`）。**完了後に**前提定義書の `GDR 仕様` 行を v2.0 に更新する
  - 推奨: `_reference/` を v2.0 で取り直す（`/gdr-upgrade`）/ プロジェクト直下 `CLAUDE.md` の GDR 書式の status 行を 5 値に更新
  - 任意: 既存 GDR への「理由の出所」の記入
- **user-level config:** 更新必要 — `CLAUDE.md`（不可侵ルール・§6 版と互換モード・現行版 v2.0）、`commands/gdr-flow.md` / `gdr-docs.md` / `gdr-kaizen.md` / `gdr-map.md`、`commands/gdr-upgrade.md`（新設）。[05 セットアップガイド](docs/ja/01_GDR/guide/05_CLAUDE_CODE_SETUP.md) を参照

## v1.0 — 2026-07-15

版管理導入前の到達点（`0eea056`）。遡及して付けた初版。

- **互換性:** —（初版）
- **要約:**
  - GDR 仕様（6 必須フィールド / status 3 値: Proposed / Implemented / Superseded / scope と PREFIX）と AI-Driven GDR ビルドアップ（サイクル / 3 原則）
  - ガイド: Getting Started / scope / PREFIX / 初回プロンプト / プロンプト / Claude Code セットアップ / 可視化
  - テンプレート: T0 最初の GDR サンプル / T1 前提定義書 / T2 ビルドアップ記録
  - 短縮キーワード 6 種と `/gdr-*` スラッシュコマンド（kaizen 001〜003, 005）
  - `notes/` 標準ディレクトリ構成、`notes/_archive/` による二段保管（kaizen 006）
  - 任意フィールド「日時」「関連」、代替案記法、`§N-M` 参照記法、可視化ガイドと `/gdr-map`（kaizen 008）
  - 根拠: kaizen 001〜008（横断検索基盤 007 は提案段階で、仕様には含まない）
- **導入先の移行項目:** —（初版。版の宣言がない導入先は v1.0 として扱う）
- **user-level config:** —

## 2026-04-16

公開
