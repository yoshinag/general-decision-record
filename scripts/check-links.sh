#!/bin/bash
# markdown 内のローカルリンクを検証する（GNU/BSD 両対応、コードブロック除外）
set -euo pipefail

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

    # インラインコード（`...`）を除去してからリンクを抽出
    local cleaned
    cleaned=$(echo "$line" | sed 's/`[^`]*`//g')
    echo "$cleaned" | sed -n 's/.*\[.*\](\([^)#]*\)).*/\1/p' | while read -r link; do
      [ -z "$link" ] && continue
      case "$link" in http://*|https://*) continue ;; esac

      local target="$dir/$link"
      if [ ! -f "$target" ]; then
        echo "BROKEN: $file -> $link"
      fi
    done
  done < "$file"
}

# 対象ファイルを検証
find documents -type f -name '*.md' -print0 | while IFS= read -r -d '' file; do
  check_file "$file"
done
for file in README.md CLAUDE.md; do
  [ -f "$file" ] && check_file "$file"
done
