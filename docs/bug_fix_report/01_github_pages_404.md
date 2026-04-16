# バグレポート: GitHub Pages で 404 / サイドバー非表示

## 概要

Docsify サイトを GitHub Pages にデプロイしたところ、404 エラーおよびサイドバーが表示されない問題が発生した。

## 発生状況

- **環境:** GitHub Pages（`docs/` フォルダをソースに指定）
- **URL:** `https://yoshinag.github.io/general-decision-record/`
- **症状:**
  1. 初回: 404 - Not Found
  2. basePath 修正後: サイドバーが空欄のまま表示されない

## 原因

### 原因 1: basePath の不一致

`docs/index.html` の Docsify 設定で `basePath: '../documents/'` と指定していたが、`documents/` は `docs/` の外にあるため GitHub Pages からアクセスできなかった。

- **ローカル:** ファイルシステム上で `../documents/` が解決できるため動作する
- **GitHub Pages:** `docs/` がルートとして配信されるため `../` は配信範囲外

### 原因 2: Jekyll による `_sidebar.md` の無視

GitHub Pages はデフォルトで Jekyll を通してファイルを配信する。Jekyll は `_`（アンダースコア）で始まるファイル・ディレクトリを無視するため、`_sidebar.md` が配信されなかった。

## 対応

| # | 対応内容 | コミット |
|---|---|---|
| 1 | `documents/` の中身を `docs/` に移動し、markdown と index.html を同階層に統合 | `dae74df` |
| 2 | `basePath` を `/general-decision-record/`（GitHub Pages のサブパス）に設定 | `f0b648d` |
| 3 | `docs/.nojekyll` を追加し、Jekyll のビルドをスキップ | `ef3a28d` |

## 再発防止

- GitHub Pages で Docsify を使う場合、`docs/` 配下に全ファイルを同居させる
- `_` で始まるファイルを使う場合は `.nojekyll` を必ず配置する
- `basePath` はリポジトリ名のサブパス（`/{repo-name}/`）を指定する
