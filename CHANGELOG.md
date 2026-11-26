# 変更履歴

GDR 仕様（`docs/ja/01_GDR/` 配下の仕様・ガイド・テンプレートと、[Claude Code セットアップ仕様](docs/ja/01_GDR/guide/05_CLAUDE_CODE_SETUP.md) が定める user-level config）の版を記録する。`docs/ja/01_GDR/tools/` は任意の補助ツールで、版の対象外とする（追加・削除と、読む書式・系譜の定義に関わる変更だけを各版の要約に書く。ツール自身が対応する版と更新日を持つ）。

- **版の付け方:** `vMAJOR.MINOR`。導入先が採用するときに**必須の移行項目がある**変更（書式違反化、既存の値の意味の変更）は MAJOR、ない変更は MINOR。移行作業が生じない文言修正等では版を上げない（[kaizen 010](docs/ja/91_demo_buildup_documents.md/kaizen/10_GDR仕様の版管理と最新版通知提案.md) GDR-META-031）
- **各版の記載項目:** 互換性 / 要約と根拠 / 導入先の移行項目（必須・推奨・任意）/ user-level config の更新要否
- **導入先での採用:** 前提定義書の `GDR 仕様: vX.Y` 行で宣言し、版の変更は GDR-META として記録する。`/gdr-upgrade` で差分と移行項目を確認できる

---

## v2.9 — 2026-11-26

- **互換性:** MINOR（任意のコマンド `/gdr-lineage` に `upgrade` を足し、`/gdr-review`・`レビュー：` に実行者・レビュアーのモデル・effort の引数を足した。GDR の書式・status 値・規則は変わらない。必須の移行なし）。**解釈版によらず適用**する。**user-level config を更新すると、`/gdr-lineage` は上流のツールの更新を自動では取り込まなくなる**（手元の写しを使い、`upgrade` を付けたときと写しが無いときだけ取得する。`save` の前に、写しがコミット済みの HTML の版より古ければ保存しない）。`/gdr-review` は引数を付けなければ従来どおり
- **要約:**
  - **`/gdr-lineage upgrade`:** ツールは `~/.local/share/gdr/` の写しを使い、毎回は取りに行かない。`upgrade` で main の最新を一時ファイルに取得し、`SPEC_VERSION` の行と構文を確かめてから置き換え、結果を `TOOL_FETCH=replaced|unchanged|failed` で報告する。失敗しても写しで続ける。`save` の前に写しの更新日とコミット済みの HTML の版を比べ、写しが古ければ保存しない（日付の粒度なので同じ日の新旧は見分けない）（[05](docs/ja/01_GDR/guide/05_CLAUDE_CODE_SETUP.md)、[06 §4](docs/ja/01_GDR/guide/06_VISUALIZATION_GUIDE.md)）
  - **v2.7 の訂正:** 「`curl -z` で main の更新だけ取り直す」は事実と違っていた。raw.githubusercontent.com は `Last-Modified` を返さず、毎回取得していた
  - **レビューの引数:** `/gdr-review`・`レビュー：` に、実行者（`main` / `sub`）・レビュアーのモデル（Agent ツールのエイリアス）・effort の段階を指定できる。指定しなければ従来どおり（`gdr-reviewer` の frontmatter で決まる）。指定はその回だけ。両端から連続して並ぶ語だけを読み、既定でない指定は委任の前に 1 行示す。`main` はメインセッションが `_reviewed.md` を書いて反映せず止める。指定した呼び出しが失敗したら代替に進まず止める。`_reviewed.md` の冒頭に「レビューの実行」の 1 行を書く（[05 §3](docs/ja/01_GDR/guide/05_CLAUDE_CODE_SETUP.md)）
  - 根拠: [kaizen 017](docs/ja/91_demo_buildup_documents.md/kaizen/17_系譜ビューアの取得をupgradeに限る提案.md)（GDR-META-042。`refines` GDR-META-040。040 の文は上書きしない）、[kaizen 018](docs/ja/91_demo_buildup_documents.md/kaizen/18_レビューの実行者とモデルの引数指定提案.md)（GDR-META-043。`refines` GDR-META-039 で、039 の 3 か所に注記）
  - ツール側の変更（版の対象外。記録のため）: 3D の系譜ビューアの status の既定を Proposed に、scope・PREFIX の既定を「すべて」にした。status の頭文字（色に頼らない）、失効の網目、視点を戻す、目次からの文書全体の表示、2D の描き方（`view=2d`）を追加
- **導入先の移行項目:**
  - 必須: なし
  - 推奨: なし
  - 任意: `commands/gdr-lineage.md` を更新したら、1 回 `/gdr-lineage upgrade` でツールを取り直す。プロジェクトに `.claude/agents/gdr-reviewer.md` を置いている導入先は写しを取り直す（丸ごと置き換わるため。取り直さなくても「レビューの実行」の 1 行は呼び出し側が渡すので書かれる）。`/gdr-review` の引数の `model` / `effort` は、プロジェクトの定義の frontmatter よりも優先される（その回だけ）
- **user-level config:** 更新必要 — `CLAUDE.md`（モデルの役割分担・§3 の `レビュー：` とコマンド表・現行版 v2.9）、`commands/gdr-lineage.md`（`upgrade`・取得・版の比較）、`commands/gdr-map.md`（「3D」で `upgrade` も渡す）、`commands/gdr-review.md`（引数・`main`・記録）、`commands/gdr-apply-review.md`（止まる条件・報告）、`commands/gdr-flow.md`（セルフレビューは既定で委ねる・合意前の提示）、`agents/gdr-reviewer.md`（記録の 1 行・保守メモ）。`gdr-review.md`・`gdr-apply-review.md`・`agents/gdr-reviewer.md` は同時に更新する

## v2.8 — 2026-11-26

- **互換性:** MINOR（任意のコマンド `/gdr-lineage` に `save` を足し、06 §4 の「生成した HTML はコミットしない」を「`save` のとき以外はコミットしない」に改めた。GDR の書式・status 値・規則は変わらない。必須の移行なし）。**解釈版によらず適用**する。**user-level config を更新すると、`/gdr-lineage save` が生成した HTML を `notes/tools/gdr_lineage.html` に保存してコミットするようになる**（`save` を付けなければ従来どおりリポジトリの外に出してコミットしない）
- **要約:**
  - **`/gdr-lineage save`（共有のため）:** 読む範囲に未コミット・追跡外・`.gitignore` した Markdown が無いときだけ `notes/tools/gdr_lineage.html` に生成し、文書が変わっていれば（ヘッダ行と対応するコミットを除いて比べる）HTML だけをパスを指定して 1 コミットする。当たったときは保存せずリポジトリの外の HTML を使う。GDR-META-026 の「生成物の永続化は明示指定時のみ」に従う形で、`/gdr-map save` と同じ（[05](docs/ja/01_GDR/guide/05_CLAUDE_CODE_SETUP.md)、[06 §4](docs/ja/01_GDR/guide/06_VISUALIZATION_GUIDE.md)）
  - **出力先を戻す:** `save` なしの出力はリポジトリの外（v2.7 の直後に一時 `.gitignore` した `notes/tools/` に出していたのを戻す）
  - ツール側の変更（版の対象外。記録のため）: 3D の系譜ビューアに、GDR を選んでいない間の目次（右ペイン）、検索ワード・status の絞り込み、選んだ GDR の絞り込みの外にある関連の一時表示を追加。scope・PREFIX の既定をリストの 1 番目にした
  - 根拠: [kaizen 016](docs/ja/91_demo_buildup_documents.md/kaizen/16_系譜ビューアの生成物のコミット提案.md)（GDR-META-041。GDR-META-040 の 2 つの文を `refines` で改め、040 に注記）
- **導入先の移行項目:**
  - 必須: なし
  - 推奨: なし
  - 任意: `commands/gdr-lineage.md` を更新する（`commands/gdr-map.md` の「3D」も `save` を渡す）。旧い `/gdr-lineage` が作った `notes/tools/.gitignore` は、`save` の初回に外れる
- **user-level config:** 更新必要 — `CLAUDE.md`（コマンド表の `/gdr-lineage`・現行版 v2.8）、`commands/gdr-lineage.md`（`save`・出力先・`status=` / `q=`）、`commands/gdr-map.md`（「3D」で `save` を渡す）

## v2.7 — 2026-11-26

- **互換性:** MINOR（user-level config に任意のコマンドを足しただけ。GDR の書式・status 値・規則は変わらない。必須の移行なし）
- **要約:**
  - **任意のコマンド `/gdr-lineage`:** 3D の系譜ビューア（`tools/gdr_lineage_3d.py`）を取得（`~/.local/share/gdr/` に置き、main の更新だけ取り直す）・生成（`notes` を読み、リポジトリの外に出力）し、Chrome で開く。引数の scope / PREFIX / GDR-ID・段数・表示数の上限を URL の `#` に変える。`/gdr-map … 3D` も同じ（[05](docs/ja/01_GDR/guide/05_CLAUDE_CODE_SETUP.md)、[06 §4](docs/ja/01_GDR/guide/06_VISUALIZATION_GUIDE.md)）
  - **取得の仕方の訂正:** ツールは版の対象外なので、タグではなく main の最新を取得し、スクリプト冒頭の `SPEC_VERSION` と更新日で確かめる（v2.6 の移行項目の記述を訂正）
  - ツール側の変更（版の対象外。記録のため）: 3D の系譜ビューアに scope / PREFIX の絞り込みと関連の段数、表示数の上限（既定 50）を追加。対応するブラウザを Chrome だけにした
  - 根拠: [kaizen 015](docs/ja/91_demo_buildup_documents.md/kaizen/15_GDRの系譜の明確化とUUIDv7の検討提案.md)（GDR-META-040）の発行後の追補。新しい GDR は起票していない（任意ツールの使い方の追加で、判断の本質は変わらないため）
- **導入先の移行項目:**
  - 必須: なし
  - 推奨: なし
  - 任意: 3D の系譜ビューアを使うなら `commands/gdr-lineage.md` を置く（`commands/gdr-map.md` の「3D」も使うなら同時に更新）
- **user-level config:** 更新必要 — `CLAUDE.md`（コマンド表に `/gdr-lineage`・現行版 v2.7）、新規 `commands/gdr-lineage.md`（任意）、`commands/gdr-map.md`（「3D」）

## v2.6 — 2026-11-26

- **互換性:** MINOR（任意フィールド `uid` の追加と、推奨・警告だけ。書式・status 値・型の語彙・既存の値の意味は変わらない。必須の移行なし）。**解釈版によらず適用**する（v1.x には `Rejected` が無く却下案からの派生が生じないだけで、読み替えは要らない）。**user-level config を更新すると、AI は GDR を起票するたびに親・日時・`uid` を書き、`uid` の生成に `python3` を 1 回実行するようになる**（実行の許可を求められることがある）
- **要約:**
  - **系譜（先祖・子孫）:** GDR の親子を、置換・`refines`・GDR を指す `derived-from` の 3 種のリンクで定義する。`depends-on` は親子ではなく前提で、前提の連鎖（`depends-on` と `refines`）を親子と並べてたどる。型の選び分けの目安、不変条件（閉路なし・置換と派生では親の日時 ≤ 子の日時。`refines` は日時を比べない）、起票時に親を書く推奨。後継としてたどるのは置換リンクだけ（参照の規律は変えない）
  - **`uid`（任意フィールド）:** GDR レコード 1 件の変わらない識別子として UUID v7 を持たせる。GDR ID は人が読む ID としてそのまま使い、リンクの対象も GDR ID のまま。`uid` は 01 §3.1 の 1 行のコマンド（Python 3.7 以上）で生成し、手で書かない。採番しなおしても変えない。AI 起票時は `uid` と日時を書く（推奨）
  - **たどる手段:** プロンプト `系譜 [GDR-ID]`（04 §5）、`/gdr-map … 系譜`（06 §4 の関係ビューの絞り込み）
  - **3D の系譜ビューア（任意の補助ツール）:** `docs/ja/01_GDR/tools/gdr_lineage_3d.py` と見本（架空の GDR）を追加。版の対象外・取得リスト外。既定の可視化（Mermaid・生成物を永続化しない。GDR-META-026）は変えない
  - [01 §3・§3.1](docs/ja/01_GDR/01_GENERAL_DECISION_RECORD.md)、[02 §6](docs/ja/01_GDR/02_AI_DRIVEN_GDR_BUILDUP.md)、[04 §4・§5](docs/ja/01_GDR/guide/04_PROMPT_GUIDE.md)、[06 §4・§5](docs/ja/01_GDR/guide/06_VISUALIZATION_GUIDE.md)、[05](docs/ja/01_GDR/guide/05_CLAUDE_CODE_SETUP.md)、[T2](docs/ja/01_GDR/templates/T2_BUILDUP_RECORD.md)、[00](docs/ja/01_GDR/guide/00_GETTING_STARTED.md) を更新。03・T0・T1・図は変更なし
  - 根拠: [kaizen 015](docs/ja/91_demo_buildup_documents.md/kaizen/15_GDRの系譜の明確化とUUIDv7の検討提案.md)（GDR-META-040）。UUID v7 を GDR ID そのものに採ることは退けた（親子を表さず、人が読めず、MAJOR になるため）
- **導入先の移行項目:**
  - 必須: なし
  - 推奨: user-level config を更新する（`CLAUDE.md`・`commands/gdr-kaizen.md`・`commands/gdr-flow.md`・`commands/gdr-map.md`・`agents/gdr-reviewer.md`）。更新後に `系譜`（引数なし）で不変条件の違反を一度確かめる
  - 任意: `_reference/` の 01・02・04・06・T2 を v2.6 で取り直す。既存の GDR に親や `uid` を遡って書く（軽微な追記）。3D の系譜ビューアを使うなら `tools/` から取得し、リポジトリの外で実行する（発行後の訂正: 取得はタグではなく main の最新。ツールは版の対象外で、冒頭の `SPEC_VERSION` と更新日で確かめる。06 §4）
- **user-level config:** 更新必要 — `CLAUDE.md`（不可侵ルールに系譜と `uid`・現行版 v2.6）、`commands/gdr-kaizen.md`・`commands/gdr-flow.md`（起票時に親・日時・`uid`。GDR 起票では `uid` を写す）、`commands/gdr-map.md`（`系譜` / `前提`）、`agents/gdr-reviewer.md`（親の記入漏れ・型の選び方・`uid` の確認）

## v2.5 — 2026-11-26

- **互換性:** MINOR（GDR の書式・status 値・遷移・理由の出所の規則は変わらない。必須の移行なし）。**ただし user-level config を更新すると、`レビュー：` / `/gdr-review` が確認を挟まずに本体を編集・コミットするようになる**（止めるときは「レビューのみ」）。**解釈版によらず適用**する。v1.x の導入先では、反映の対象に `Proposed` の GDR があるとき、合意済みかどうかを反映の前に 1 回確かめる
- **要約:**
  - **レビューの委任:** レビューは起票した文脈から独立した文脈で、レビュアーのモデル（上位モデル）に書かせる。Claude Code ではレビュー用サブエージェント `~/.claude/agents/gdr-reviewer.md` に委ね、レビュアーのモデルと推論の強さの指定は定義の frontmatter の 1 か所に書く（プロジェクトの `.claude/agents/` で上書き可）
  - **レビューと反映のワンセット:** レビューに続けて確認を挟まず反映まで行う。人の確認は「判断が要ると印の付いた指摘への回答」と「合意」に移る。代わりに、記録と取り消し（`_reviewed` をコミットしてから反映し、反映を別コミットにする）・止める条件・対象の絞り込み（確定済み GDR の軽微な訂正は聞いて反映、それ以外は置換 GDR の候補として報告）・指摘の印（【そのまま反映可】／【要ユーザー判断】）・合意との境界（反映時の回答は合意ではない）をそろえる
  - [02 §5.2](docs/ja/01_GDR/02_AI_DRIVEN_GDR_BUILDUP.md) に原則、[05](docs/ja/01_GDR/guide/05_CLAUDE_CODE_SETUP.md) に `gdr-reviewer.md` の仕様と「レビュー反映の規則」、[04](docs/ja/01_GDR/guide/04_PROMPT_GUIDE.md) §3・§6 と [00](docs/ja/01_GDR/guide/00_GETTING_STARTED.md) の説明・配置プロンプトを更新。03・テンプレート・図は変更なし
  - 根拠: [kaizen 014](docs/ja/91_demo_buildup_documents.md/kaizen/14_レビューの上位モデル委任と反映のワンセット化提案.md)（GDR-META-039）
- **導入先の移行項目:**
  - 必須: なし
  - 推奨: user-level config を更新する — `agents/gdr-reviewer.md` を新しく置く。`commands/gdr-review.md` と `commands/gdr-apply-review.md` は**必ず同時に**更新する（`gdr-review.md` だけ新しくすると、止める条件も印も無い旧い反映の規則のまま確認なしで反映が走る）
  - 任意: `_reference/02_AI_DRIVEN_GDR_BUILDUP.md` / `_reference/guide/04_PROMPT_GUIDE.md` を v2.5 で取り直す
- **user-level config:** 更新必要 — `CLAUDE.md`（レビューの委任・`レビュー：` のワンセット・現行版 v2.5）、`commands/gdr-review.md`、`commands/gdr-apply-review.md`、`commands/gdr-flow.md`（フェーズ 2〜3 の判定・フェーズ 4）、新規 `agents/gdr-reviewer.md`

## v2.4 — 2026-11-12

- **互換性:** MINOR（図の追加と、`_reference/` に図を取り込む手順の追加のみ。規則・書式・解釈は変わらない）
- **要約:**
  - 仕様を読む助けとして SVG の図 4 枚を追加（`docs/ja/01_GDR/assets/`。ライト / ダークの配色に追従）
    - [01 §3](docs/ja/01_GDR/01_GENERAL_DECISION_RECORD.md): status と遷移（有効 / 失効、撤回時の復帰、二段保管の退避時点）
    - [02 §4](docs/ja/01_GDR/02_AI_DRIVEN_GDR_BUILDUP.md): ビルドアップのサイクルと PDCA（Plan = 起票〜合意、Do = GDR 起票と実装、Check = 実装と再検討条件による検証、Act = 置換・撤回・退避）。ASCII のサイクル図はテキスト版として残す
    - 02 §5.2: 置換のときの新 GDR・旧 GDR・波及先の 3 本の時間軸と波及チェック
    - 02 §6: 参照の規律（前向きにたどる・逆向きに見直す）
  - `_reference/` の取得対象に `assets/*.svg` を追加（[05 セットアップガイド](docs/ja/01_GDR/guide/05_CLAUDE_CODE_SETUP.md)）
- **導入先の移行項目:**
  - 必須: なし
  - 推奨: `_reference/01_GENERAL_DECISION_RECORD.md` / `_reference/02_AI_DRIVEN_GDR_BUILDUP.md` を v2.4 で取り直し、あわせて `_reference/assets/*.svg` を取得する（取り直さないと、新しい 01 / 02 の図のリンクが切れる）
  - 任意: なし
- **user-level config:** 更新必要 — `CLAUDE.md`（初回導入の取得リストに `assets/*.svg`・現行版 v2.4）、`commands/gdr-upgrade.md`（取り直しで図も取得）

## v2.3 — 2026-11-12

- **互換性:** MINOR（置換・撤回の手順と AI の振る舞いの追加のみ。既存の GDR の書式・status 値・遷移・解釈は変わらない）。**解釈版によらず適用**する。v1.x の導入先では、判定と「関連」の付け替えを新 GDR の発行時（旧を `Superseded` にする時点）にまとめて行う
- **要約:**
  - **波及チェック:** 置換・合意後の撤回で失効する GDR を「関連」の `depends-on` / `refines` で前提にしている有効な GDR を、① 起票時に列挙（新 GDR の「影響」に「波及候補」）→ ② 合意時に人間が 1 件ずつ判定（影響なし: 付け替える / 外す / `relates-to` に弱める、影響あり: その GDR を置換する GDR を起票）→ ③ 新が `Implemented` になった時点で付け替える。AI は波及先を一括で書き換えない。scope の一致は基準にしない
  - **不変条件:** 失効した GDR を `depends-on` / `refines` で指す有効な GDR が残っている間は、その GDR を退避しない（二段保管の退避時点はこれを満たしてから）。未解決の依存は「失効 GDR を指す有効な GDR」として検出できる
  - [01 §3](docs/ja/01_GDR/01_GENERAL_DECISION_RECORD.md) に規則と退避の条件、[02 §5.2 / §6](docs/ja/01_GDR/02_AI_DRIVEN_GDR_BUILDUP.md) に手順と参照の規律の逆向きの確認、[04 §5](docs/ja/01_GDR/guide/04_PROMPT_GUIDE.md) にプロンプト `波及チェック [GDR-ID]`、[05](docs/ja/01_GDR/guide/05_CLAUDE_CODE_SETUP.md) に config の同期。テンプレートは変更なし
  - 根拠: [kaizen 013](docs/ja/91_demo_buildup_documents.md/kaizen/13_GDR置換時の波及チェック提案.md)（GDR-META-038）
- **導入先の移行項目:**
  - 必須: なし
  - 推奨: 導入済みの GDR について、不変条件の違反（退避済みの失効 GDR を `depends-on` / `refines` で指す有効な GDR）を一度確認する（`波及チェック` を引数なしで実行）
  - 任意: `_reference/01_GENERAL_DECISION_RECORD.md` / `_reference/02_AI_DRIVEN_GDR_BUILDUP.md` / `_reference/guide/04_PROMPT_GUIDE.md` を v2.3 で取り直す
- **user-level config:** 更新必要 — `CLAUDE.md`（不可侵ルールに波及チェックを追加・現行版 v2.3）、`commands/gdr-flow.md`（フェーズ 1・4・7 と版条件）、`commands/gdr-docs.md`（旧 GDR の退避と版条件）、`commands/gdr-archive.md`（GDR 本文の退避前の確認）

## v2.2 — 2026-10-16

- **互換性:** MINOR（プロンプトと AI の振る舞いの追加のみ。既存の GDR の書式・解釈は変わらない）
- **要約:**
  - 「目標は上げてから検討し、縮めるのは明示的な判断としてだけ」を AI への依頼の指針とした。`最適解を` / `過剰じゃない？` は手段を縮める道具であり、手段の圧縮の副作用で目標を縮めない
  - [04 プロンプトガイド §2.1](docs/ja/01_GDR/guide/04_PROMPT_GUIDE.md) に目標を上げるプロンプト 5 個（高度 / 深さ / 幅）、適用場面、野心的な目標を GDR にするときの書き方（撤退基準を再検討条件に、届かなければ `Rejected`）を追加。§7 に「上げてから縮める」
  - [02 §6](docs/ja/01_GDR/02_AI_DRIVEN_GDR_BUILDUP.md) に振る舞い「目標の引き上げ」、§3.3 に留意点「目標の縮小」を追加。01 仕様とテンプレートは変更なし
  - 根拠: [kaizen 012](docs/ja/91_demo_buildup_documents.md/kaizen/12_AIへの野心度を上げる指針の導入提案.md)（GDR-META-037）
- **導入先の移行項目:**
  - 必須: なし
  - 推奨: なし
  - 任意: `_reference/guide/04_PROMPT_GUIDE.md` と `_reference/02_AI_DRIVEN_GDR_BUILDUP.md` を v2.2 で取り直す
- **user-level config:** 更新必要 — `CLAUDE.md`（不可侵ルールの過剰設計の検出に「圧縮は手段に向け、目標を縮めるときは理由を残す」を追加・現行版 v2.2）

## v2.1 — 2026-10-06

- **互換性:** MINOR（新しい書き方の規則の追加のみ。既存の GDR の書式・解釈は変わらない）
- **要約:**
  - 共有される文書に環境依存の絶対パスを書かない。手元で読むリポジトリ外の資料は論理名（リポジトリ名 + リポジトリ相対パス）で参照し、各環境での場所は共有しないローカル対応表（既定 `PATHS.local.md`）に置く。AI は場所を推測しない。混入は `git grep` で確認する
  - 規則は [03 初回プロンプトガイド §2.4](docs/ja/01_GDR/guide/03_FIRST_PROMPT_GUIDE.md)、確認コマンドとツール別の実装例は [05 セットアップガイド](docs/ja/01_GDR/guide/05_CLAUDE_CODE_SETUP.md)。01 仕様と T1 テンプレートは変更なし
  - 根拠: [kaizen 011](docs/ja/91_demo_buildup_documents.md/kaizen/11_環境依存パスの論理参照化提案.md)（GDR-META-035）
- **導入先の移行項目:**
  - 必須: なし
  - 推奨: 共有される文書に残る絶対パスを論理名に置き換え、場所をローカル対応表へ移す（外部資料を参照しているプロジェクトのみ）
  - 任意: 前提定義書に「外部資料」節を追加する
- **user-level config:** 更新必要 — `CLAUDE.md`（不可侵ルールに参照の規則を追加・現行版 v2.1）、`commands/gdr-docs.md`（整理観点「環境依存パス」）

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
