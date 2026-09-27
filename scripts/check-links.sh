#!/bin/bash
# markdown 内のローカルリンクを検証する（GNU/BSD 両対応、コードブロック除外）
#
# リンクの解決規則:
#   - `/` で始まるリンク → Docsify のルート（docs/ja/）からの絶対パス
#   - それ以外             → リンク元ファイルのディレクトリからの相対パス
#   - `#` 以降（アンカー）は無視、http(s):// と mailto: は対象外
set -euo pipefail

DOCSIFY_ROOT="docs/ja"
status=0

check_file() {
  local file="$1"
  local dir
  dir=$(dirname "$file")

  local in_code=0
  while IFS= read -r line; do
    # コードブロック（```）のトグル
    case "$line" in
      '```'*) in_code=$(( 1 - in_code )); continue ;;
    esac
    [ "$in_code" -eq 1 ] && continue

    # インラインコード（`...`）を除去してから、1 行内のすべてのリンクを抽出
    local cleaned
    cleaned=$(printf '%s\n' "$line" | sed 's/`[^`]*`//g')
    while read -r link; do
      [ -z "$link" ] && continue
      link="${link%%#*}"
      [ -z "$link" ] && continue
      case "$link" in http://*|https://*|mailto:*) continue ;; esac

      local target
      case "$link" in
        /*) target="$DOCSIFY_ROOT$link" ;;
        *)  target="$dir/$link" ;;
      esac
      if [ ! -e "$target" ]; then
        echo "BROKEN: $file -> $link"
        status=1
      fi
    done < <(printf '%s\n' "$cleaned" | grep -oE '\]\([^)]+\)' | sed -E 's/^\]\((.*)\)$/\1/' || true)
  done < "$file"
}

# 対象ファイルを検証（Docsify サイト + リポジトリ直下の主要文書）
while IFS= read -r -d '' file; do
  check_file "$file"
done < <(find docs -type f -name '*.md' -print0)
for file in README.md CLAUDE.md CHANGELOG.md; do
  [ -f "$file" ] && check_file "$file"
done

exit "$status"
