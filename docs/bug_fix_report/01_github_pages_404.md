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

### 原因 3: ドキュメント間リンクのパス解決

Docsify は `relativePath: true` を設定しない限り、markdown 内のリンクを basePath ルートからの絶対パスとして解決する。`guide/01_SCOPE_GUIDE.md` のような相対パスはルートの `#/` にフォールバックし、リンク先が見つからなかった。

さらに、絶対パスでも `/` プレフィックスがないとルーティングが正しく動作しなかった。

### 原因 4: Docsify の README.md フォールバック

Docsify は `homepage` を設定していても、一部のルートで `README.md` をフォールバックとして読み込む。リポジトリルートの `README.md` は GitHub 用のリンク（`docs/01_GDR/...`）を使用しており、Docsify のルーティングでは解決できないため 404 になった。

## 対応

| # | 対応内容 | コミット |
|---|---|---|
| 1 | `documents/` の中身を `docs/` に移動し、markdown と index.html を同階層に統合 | `dae74df` |
| 2 | `basePath` を `/general-decision-record/`（GitHub Pages のサブパス）に設定 | `f0b648d` |
| 3 | `docs/.nojekyll` を追加し、Jekyll のビルドをスキップ | `ef3a28d` |
| 4 | 全ドキュメントのリンクを `/01_GDR/...` 形式の絶対パスに統一 | `9f4441d` |
| 5 | `docs/README.md` を追加し、Docsify フォールバック時にトップページへ案内 | `8f2ecda` |

## 再発防止

- GitHub Pages で Docsify を使う場合、`docs/` 配下に全ファイルを同居させる
- `_` で始まるファイルを使う場合は `.nojekyll` を必ず配置する
- `basePath` はリポジトリ名のサブパス（`/{repo-name}/`）を指定する
- ドキュメント間リンクは `/` プレフィックス付きの絶対パス（`/01_GDR/...`）を使用する
- `docs/README.md` を配置し、Docsify のフォールバック表示を制御する
