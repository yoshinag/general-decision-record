# 変更履歴

GDR 仕様（`docs/ja/01_GDR/` 配下の仕様・ガイド・テンプレートと、[Claude Code セットアップ仕様](docs/ja/01_GDR/guide/05_CLAUDE_CODE_SETUP.md) が定める user-level config）の版を記録する。

- **版の付け方:** `vMAJOR.MINOR`。導入先が採用するときに**必須の移行項目がある**変更（書式違反化、既存の値の意味の変更）は MAJOR、ない変更は MINOR。移行作業が生じない文言修正等では版を上げない（[kaizen 010](docs/ja/91_demo_buildup_documents.md/kaizen/10_GDR仕様の版管理と最新版通知提案.md) GDR-META-031）
- **各版の記載項目:** 互換性 / 要約と根拠 / 導入先の移行項目（必須・推奨・任意）/ user-level config の更新要否
- **導入先での採用:** 前提定義書の `GDR 仕様: vX.Y` 行で宣言し、版の変更は GDR-META として記録する。`/gdr-upgrade` で差分と移行項目を確認できる

---

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
