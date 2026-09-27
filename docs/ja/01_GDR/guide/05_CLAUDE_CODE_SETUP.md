# Claude Code セットアップガイド

> 前提知識: [00. Getting Started](/01_GDR/guide/00_GETTING_STARTED.md) Step 2.0 / [04. プロンプトガイドライン §6 コンテキスト短縮キーワード](/01_GDR/guide/04_PROMPT_GUIDE.md#6-コンテキスト短縮キーワードclaudemd-連携)

Claude Code を使う場合、`~/.claude/` 配下に **user-level の global config** を配置すると、すべてのプロジェクトで GDR 方法論と短縮キーワード / スラッシュコマンドが自動有効になる。

本ガイドは [00. Getting Started](/01_GDR/guide/00_GETTING_STARTED.md) Step 2.0 から呼ばれる詳細仕様。Cursor / GitHub Copilot などを使う場合は不要。

## 配置するファイル（9 ファイル + 任意 1 ファイル）

| 配置パス | 役割 |
|---|---|
| `~/.claude/CLAUDE.md` | user-level の常駐指示書。全プロジェクト横断で自動読み込み |
| `~/.claude/commands/gdr-kaizen.md` | スラッシュコマンド `/gdr-kaizen <タイトル>` の定義 |
| `~/.claude/commands/gdr-review.md` | スラッシュコマンド `/gdr-review <ファイル名>` の定義 |
| `~/.claude/commands/gdr-apply-review.md` | スラッシュコマンド `/gdr-apply-review <ファイル名>` の定義 |
| `~/.claude/commands/gdr-bug-report.md` | スラッシュコマンド `/gdr-bug-report [<識別子>]` の定義（引数有無で 2 モード切替） |
| `~/.claude/commands/gdr-flow.md` | スラッシュコマンド `/gdr-flow <作業指示>` の定義 |
| `~/.claude/commands/gdr-archive.md` | スラッシュコマンド `/gdr-archive <パス>` の定義 |
| `~/.claude/commands/gdr-docs.md` | スラッシュコマンド `/gdr-docs` の定義（**実装後の文書整理**、引数なし専用） |
| `~/.claude/commands/gdr-upgrade.md` | スラッシュコマンド `/gdr-upgrade [<目標版>]` の定義（**GDR 仕様の版の更新** — 差分提示・採用記録。短縮キーワードなし） |
| `~/.claude/commands/gdr-map.md` | **（任意）** スラッシュコマンド `/gdr-map [<対象>]` の定義（**可視化** — [06_VISUALIZATION_GUIDE.md](/01_GDR/guide/06_VISUALIZATION_GUIDE.md) 準拠。既定 6 キーワード体系の外） |

## `~/.claude/CLAUDE.md` の仕様

最低限、以下のセクションを含める:

1. **Git 運用ルール（横断）** — commit / push の既定の挙動。プロジェクト固有の `.claude/settings.json` 側 hook と矛盾する場合はプロジェクト側を優先する旨を明記。
2. **GDR 方法論セクション** — 以下を含む:
   - **いつ提案・適用するか** — 新規リポ立ち上げ / 「設計判断」「方針決定」「ADR」等のキーワード検知 / 既存 GDR ディレクトリ検知時
   - **初回導入時の標準手順** — Getting Started Step 1〜2 の流れ（標準ディレクトリ構成の作成、上流ファイル取得、ローカライズ初回プロンプト実施、scope/PREFIX 合意、前提定義書（`GDR 仕様` 行に採用版を宣言）/ INDEX / 最初の GDR-META 生成）
   - **既定の短縮キーワード** — `改善提案：` / `レビュー：` / `レビュー反映：` / `バグレポート：` / `一気通貫：` / `アーカイブ：` の 6 種と、対応するスラッシュコマンドの対応表
   - **不可侵ルール** — 判断本質の変更は新 GDR + `Superseded`（旧の失効は新の `Accepted` 時点、退避は新の `Implemented` 時点）/ status 5 値と参照の規律（失効 GDR を根拠にしない）/ AI 起票時の「理由の出所」記入 / scope・PREFIX 改廃は GDR-META 経由 / 文書と実装を混ぜない / 自明な実装詳細を GDR 化しない
   - **上流ドキュメントの参照先** — 導入済プロジェクトの `notes/91_gdr/_reference/` 配下にスナップショットがある旨
   - **GDR 仕様の版（検出・互換モード）** — 以下を含む（経緯: [010 提案](/91_demo_buildup_documents.md/kaizen/10_GDR仕様の版管理と最新版通知提案.md) GDR-META-033 / 034）:
     - `GDR 仕様の現行版: vX.Y` の 1 行（上流で版が上がったら**この行も更新する** — 忘れると導入先への通知が出ない）
     - 解釈版の読み取り: 短縮キーワード / `/gdr-*` コマンドの実行時に前提定義書の `GDR 仕様` 行をセッション内で 1 回読む（未宣言は v1.0、上流リポジトリ自身は現行版）
     - 通知: 解釈版が現行版より古い / 未宣言なら、セッション内で 1 回だけ `/gdr-upgrade` を案内する。自動移行はしない
     - 版条件付きの規則表: 版で意味が変わる規則（status の値と解釈・完了処理・置換・参照の規律・理由の出所）を版ごとに併記する。保持は直前の MAJOR まで

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
| `gdr-kaizen.md` | GDR T2 形式の改善提案を `notes/20_kaizen/` 配下に生成 | `<タイトル>` | `notes/20_kaizen/{YYYY-MM-DD}_{slug}.md` に T2 構成のドラフト生成。文書のみ生成、実装着手しない。GDR は `Proposed` で起票し「理由の出所」を付ける |
| `gdr-review.md` | 対象ファイルをセルフレビューし `{filename}_reviewed.md` を生成（引数有無で 2 モード） | `[<ファイル名 or 相対パス>]` | **引数あり:** 指定ファイルをレビュー。**引数なし:** 直近会話で言及されたファイル / `git status` の modified / `git log --name-only -3` から自動特定。候補複数なら AskUserQuestion。同位置に `{元ファイル名}_reviewed.md` を出力（横断レビューは `notes/91_gdr/review/` 配下）。区分 A〜G で整理 |
| `gdr-apply-review.md` | `_reviewed.md` の内容を本体に統合し `_reviewed.md` を削除（引数有無で 2 モード） | `[<元ファイル名 or _reviewed.md ファイル名>]` | **引数あり:** 指定の `_reviewed.md` を統合。**引数なし:** `find . -name '*_reviewed.md'` の候補から更新日時で最新を第一候補にし、複数あれば AskUserQuestion で確認。A / D / E は必ず反映、B / C / F / G は必要に応じて。統合後 `_reviewed.md` を削除し 1 コミット |
| `gdr-bug-report.md` | バグレポートを `notes/80_bug_fix_report/` 配下に生成（引数有無で 2 モード） | `[<識別子 / ファイル名 / 症状概要>]` | **引数あり:** 任意識別子から書き起こす（外部報告 / 後日まとめ向き）。**引数なし:** **現セッションの内容**（tool 失敗 / stderr / 試行錯誤 / Classifier deny 等）を自動抽出し、末尾に「**セッションログ抜粋**」セクション（AI が試したアプローチの時系列・判断転換点・deny 原文）を残して**経緯保存**する。両モードとも 10 項構成（メタ / 症状 / 再現 / 原因 / 影響 / 回避策 / 修正案 / 推奨 / 既知事項 / 次のアクション） |
| `gdr-flow.md` | 進行状況を確認し GDR ビルドアップサイクルをノンストップで前進（引数有無で 2 モード） | `[<作業指示 or トピック>]` | **引数あり:** 指定作業の現在地（会話文脈 / `git log` / `notes/` ファイル状態）を判定し**次フェーズだけ**実行（巻き戻し禁止）。**引数なし:** **セッション全体を概観**し進行中の作業を自動特定（直近会話 / `git log -10` / 未コミット差分 / 最近変更された `notes/` 配下）、作業の核を 1 文で言語化してから現在地判定 → 完走。曖昧時は AskUserQuestion で確認。フェーズ: 起票 → セルフレビュー → レビュー反映 → 合意 → GDR 起票 → 実装 → 完了処理。合意時に `Proposed → Accepted`・出所 `ai → ai-reviewed`・置換対象の旧を `Superseded`、完了処理で `Accepted → Implemented`・旧の退避。全フェーズで「GDR 参照の規律」（失効 GDR を根拠にしない）を適用 |
| `gdr-archive.md` | 対象ファイル / ディレクトリを `notes/_archive/` 配下へ退避（AI デフォルト除外領域） | `<ファイル or ディレクトリのパス>` | `git mv` で `notes/_archive/{元のパス}` に退避し 1 コミット。同名既存ファイル時はエラー終了。ディレクトリ指定時はディレクトリごと退避。物理削除はユーザー手動 (`rm`) |
| `gdr-docs.md` | **実装後の文書整理**（GDR status 更新 / ふりかえり追記 / INDEX 更新 / spec 最終化）。整理対象がなければ無音 | （引数なし） | `git log -10 --name-only` で実装系コミットを特定 → 関連文書（GDR / 改善提案 / `INDEX` / `spec`）を整合状態に更新 → 整理単位ごとに別コミット。`/gdr-flow` のフェーズ 7「完了処理」を独立コマンド化したショートカット。GDR status は `Accepted → Implemented`（`Proposed` のままなら合意漏れとして警告）、置換された旧 GDR の退避も行う（v1.x の導入先では `Proposed → Implemented`）。上流リポジトリでは仕様変更を含む kaizen の完了時に**版の判定**（MAJOR / MINOR / 上げない）も行う。**該当なしなら無音で終了** |
| `gdr-upgrade.md` | 導入先の GDR 仕様の版を確認し、最新版との差分・移行項目を提示して採用を記録（自動移行はしない） | `[<目標版>]` | 前提定義書の宣言版（未宣言は v1.0）と上流の最新タグ（`gh api` / 未認証時は raw の CHANGELOG）を比較、user-level config の現行版が古ければ報告 → CHANGELOG の差分（互換性・移行項目）を提示 → 採否を AskUserQuestion → `_reference/` を目標版タグで取り直し → GDR-META 起票 → 必須移行がなければ宣言行を更新（ある場合は移行完了後に更新）→ 1 コミット |
| `gdr-map.md`（任意） | GDR の蓄積を Mermaid で可視化（関係ビュー = 型付き有向グラフ / 構造ビュー = mindmap）。既定はセッション内提示のみ | `[<scope / PREFIX / GDR-ID / ファイルパス>] [構造] [save]` | **引数あり:** 指定対象（scope / PREFIX / GDR-ID の近傍 / 文書内）に絞ったビューを生成。**引数なし:** `notes/91_gdr/` を走査して全景の関係ビューを生成、破綻しそうな規模なら AskUserQuestion で絞り込みを提案。`save` 指定時のみ `notes/91_gdr/map/` に生成物ヘッダ付きで保存（図はキャッシュ、正は GDR 文書）。詳細は [06_VISUALIZATION_GUIDE.md](/01_GDR/guide/06_VISUALIZATION_GUIDE.md) |

> **キーワードとスラッシュコマンドの住み分け:** 短縮キーワード（`改善提案：` 等）は自然文中の流れで使う。スラッシュコマンド（`/gdr-kaizen` 等）は Tab 補完で発見性が必要な場面で使う。両方とも生きている。

## コマンドの 2 モード対応パターン（共通ガイドライン）

スラッシュコマンドは原則 1 つの動作モードを持つが、以下の条件を満たす場合は**引数の有無で 2 モード対応**にする:

- **モード A（引数あり）** = 対象を明示する従来動作
- **モード B（引数なし）** = **セッション文脈 / `git` 状態 / 最近変更された `notes/` 配下から対象を自動特定**して同じ流れを実行する

両モードに運用上の意義がある場合のみ拡張する。AI が「自動特定」する内容が曖昧になりうるコマンド（破壊的操作 / 引数依存度が高い操作）は 1 モードに留める。

### 現在 2 モード対応のコマンド

| コマンド | モード A（引数あり） | モード B（引数なし） |
|---|---|---|
| `/gdr-bug-report` | 任意識別子から書き起こす（外部報告 / 後日まとめ向き） | 現セッションのエラー / 試行錯誤 / Classifier deny を抽出して**経緯保存**。末尾に「セッションログ抜粋」を追加 |
| `/gdr-flow` | 指定作業の現在地を判定して次フェーズだけ実行 | セッション全体を概観し進行中の作業を自動特定 → 作業の核を 1 文で言語化 → 現在地判定 → 完走 |
| `/gdr-review` | 指定ファイルをセルフレビュー | 直近会話言及 / `git status` modified / `git log --name-only -3` から対象を自動特定。複数候補なら AskUserQuestion |
| `/gdr-apply-review` | 指定 `_reviewed.md` を本体に統合 | `find . -name '*_reviewed.md'` の候補から更新日時で最新を第一候補にし、複数あれば AskUserQuestion |
| `/gdr-map`（任意） | 指定対象（scope / PREFIX / GDR-ID の近傍 / 文書内）に絞ったビューを生成 | `notes/91_gdr/` 走査で全景の関係ビューを生成。破綻しそうな規模なら AskUserQuestion で絞り込みを提案 |

### 2 モード対応の書き方

- `argument-hint` は `[<...>]` のように角括弧で省略可を示唆する
- 本体は「## モード A: ...」「## モード B: ...」のサブセクションで分ける
- 両モードで共通の振る舞いは「## 共通の振る舞い」として別出し
- モード B では「対象が曖昧 / 複数候補が拮抗 / そもそも進行中の作業が無い」場合に **AskUserQuestion で確認**する旨を必ず明記
- モード B の中止条件（自動特定が確信を持って行えない）を 1 行で書く

### 2 モード化の判定（将来コマンド追加時）

| コマンド | 適合性 | 備考 |
|---|---|---|
| `gdr-kaizen` | 1 モード（引数あり前提） | タイトル指定が本質的に必要。引数なしで「セッションから改善案を提案」は提案責任が AI に偏りすぎ |
| `gdr-archive` | 1 モード（引数あり前提） | 退避という破壊的操作で対象を AI が自動特定するリスクが高い。常に明示パス指定とする |
| `gdr-docs` | 1 モード（**引数なし専用**） | セッション全体と直近コミットから整理対象を自動判定。引数を許す意味が薄く、対象がなければ無音で終了する設計のため引数あり / なしで挙動を分ける必要がない |

現状の運用:

- **2 モード対応:** `/gdr-bug-report` `/gdr-flow` `/gdr-review` `/gdr-apply-review` の 4 コマンド（+ 任意導入の `/gdr-map`）
- **1 モード（引数あり前提）:** `/gdr-kaizen` `/gdr-archive` の 2 コマンド
- **1 モード（引数なし専用）:** `/gdr-docs` の 1 コマンド（**「該当時のみ動作、無ければ無音」が前提のため引数を取らない**）

### モード B の誤特定時のロールバック

モード B で AI が「自動特定」を誤った場合、いずれのコマンドも **1 コミット単位で完結している**ため、`git revert HEAD` で安全に元に戻せる。退避（`/gdr-archive`）と統合（`/gdr-apply-review`）も `git mv` / `_reviewed.md` 削除を含めて 1 コミットになるよう設計されているため、巻き戻し手順は共通。

- 誤特定が明らかになった時点で速やかに `git revert` する（隠さない）
- revert 後、引数ありモード（モード A）で再実行する
- 同種の誤特定が複数回繰り返される場合は、本ガイドラインの判定基準（破壊的操作 / 引数依存度）を再評価する

### `gdr-archive.md` 内容例

```markdown
---
description: 対象を notes/_archive/ 配下へ退避（AI デフォルト除外領域）
argument-hint: <ファイル or ディレクトリのパス>
---

# /gdr-archive $ARGUMENTS

`$ARGUMENTS` で指定された対象を `notes/_archive/{元のパス}` に退避する。

## 動作

1. 対象の存在を確認
2. 退避先 `notes/_archive/{元のディレクトリ}/{元のファイル名}` を計算し、必要なディレクトリを自動作成
3. `git mv` で移動（履歴保持）
4. 1 コミット（メッセージ例: `docs(archive): move {元のファイル名}`）

## 例外

- **同名既存ファイル時:** エラー終了。ユーザーが既存を確認・退避先を変更してから再実行
- **ディレクトリ指定時:** ディレクトリごと `git mv` で再帰的に退避（サブディレクトリ含む）
- **物理削除:** AI は触らない。ユーザーが手動 `rm` で行う

## 復元

```bash
git mv notes/_archive/{元のディレクトリ}/{元のファイル名} {元のディレクトリ}/
```

退避時のパス構造を反転するだけで戻る。
```

## 上流で版を発行する手順（メンテナ向け）

GDR 仕様（`docs/ja/01_GDR/` / 本セットアップ仕様 / user-level config）を変える kaizen の完了時に行う（経緯: [010 提案](/91_demo_buildup_documents.md/kaizen/10_GDR仕様の版管理と最新版通知提案.md) §4.5）:

1. 版を上げるか・どちらの桁かを判定する — 導入先の採用時に**必須の移行項目がある**（書式違反化・既存の値の意味の変更）なら MAJOR、ないなら MINOR、移行作業が生じないなら上げない
2. user-level config の版依存の規則に版条件を付け、旧版の規則を直前の MAJOR まで保持する（互換モード）
3. リポジトリ直下の `CHANGELOG.md` にエントリを追加する（互換性 / 要約と根拠 / 移行項目の必須・推奨・任意 / user-level config の更新要否）
4. `git tag -a vX.Y`（公開は push）
5. user-level config の `GDR 仕様の現行版` の行を更新する（**忘れると導入先への通知が出ない**）
6. 本ガイドのコマンド仕様を同期する

## 補足: `.claude/settings.json` での技術的強制（任意）

CLAUDE.md の明記だけでは AI が読み込んでしまう懸念がある場合、`.claude/settings.json` の `hooks.PreToolUse` で `notes/_archive/` への `Read` を deny する雛形を追加できる:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "[ \"${CLAUDE_TOOL_INPUT_file_path##*notes/_archive/}\" = \"$CLAUDE_TOOL_INPUT_file_path\" ] && exit 0 || { echo 'notes/_archive/ is excluded by default. Specify the explicit file path with user intent.' >&2; exit 2; }"
          }
        ]
      }
    ]
  }
}
```

> 上記は概念例。実環境のスクリプト構文・hook 仕様は Claude Code バージョンに合わせて調整すること。CLAUDE.md 明記のみで運用上問題なければ本設定は不要。

## 配置後: Claude Code を一度再起動する

`~/.claude/CLAUDE.md` および `~/.claude/commands/*.md` は **Claude Code の起動時に読み込まれる**。既に Claude Code セッションを開いている場合、ファイルを配置・更新しても自動では反映されない。

配置後は一度セッションを終了してから再起動する:

```
/exit
```

その後 Claude Code を起動し直すと、global config とスラッシュコマンドが有効になる（`/` 入力で `/gdr-*` 系コマンドが補完候補に出れば成功）。
