#!/usr/bin/env python3
"""GDR の系譜を 3D で俯瞰する単一 HTML を生成する。Python 3.7 以上の標準ライブラリだけで動く。

系譜の定義は上流（general-decision-record リポジトリ）の GDR 仕様 01 §3.1「系譜（先祖・子孫）の規則」。
この版が前提にする GDR 仕様: v2.6（SPEC_VERSION）。上流の docs/ja/01_GDR/tools/ に置く任意の補助ツールで、
GDR 仕様の版の対象外（取得リストに入れない。要る導入先が main の最新を取得し、この SPEC_VERSION と TOOL_UPDATED で
対応する版と更新日を確かめる。_reference/ には入れない）。取得の例:
  curl -fsSL https://raw.githubusercontent.com/yoshinag/general-decision-record/main/docs/ja/01_GDR/tools/gdr_lineage_3d.py -o ~/.local/share/gdr/gdr_lineage_3d.py

使い方:
  python3 gdr_lineage_3d.py [ディレクトリ ...] [-o lineage_3d.html] [--demo]

  ディレクトリ   GDR を含む Markdown の置き場（既定: notes/91_gdr）。1 つが 1 データセットになる
                 （`ラベル=ディレクトリ` でラベルを付けられる。既定のラベルはディレクトリ名）。下の階層も読む。
                 `_archive` / `_reference` / `review` と `*_reviewed.md` は読まない
  --demo         架空の GDR（系譜・前提・違反の見本）をデータセットに加える
  -o             出力先（既定: lineage_3d.html）。どこに出し、コミットするかは使う人が決める（上流の /gdr-lineage は
                 save のときだけ notes/tools/ に保存してコミットする。GDR-META-041）

読み方:
  - GDR の始まり: 太字の行（**GDR-X-NNN: 要約**）または見出しの行（## GDR-X-NNN: 要約）
  - 親子（系譜）: 置換（status 行の Superseded by / supersedes）・refines・GDR を指す derived-from
  - 前提: depends-on と refines を推移的にたどる（波及チェックと同じ範囲）。relates-to は弱い関連
  - 不変条件: 親子は閉路を持たない / 置換と GDR 向き derived-from では親の日時 <= 子の日時
    （「日時」だけで比べる。日付のみ・オフセットの無い時刻が片方にあれば日付で比べ、同日は違反としない。
    読めない日時の端は比べない。refines は日時を比べない）
  - 警告: 異なる GDR ID に同じ uid / 形式を満たさない uid / 同じ ID が複数の文書にあって uid が違う
  - 「## 1. GDR」節を持つ文書（改善提案）はその節の GDR だけを、それ以外は文書全体の GDR を読む。コードブロック内は読まない
  - 縦の位置は 日時 > uid の時刻 > ファイルの git 追加日（推定）の順で決める（位置にだけ使い、判定には使わない）
  - 読めなかったもの（status・日時・型の無い関連・知らない型・GDR らしいのに読めなかった行）は件数を出す
  - 画面で scope / PREFIX を選ぶと、当てはまる GDR と、そこから表示中のリンクを指定の段数（1 段・2 段・すべて）
    たどった GDR だけを描く。表示数の上限も選べる（既定 50。超えたら、絞り込み中は当てはまる GDR → 近い段の順、
    絞り込みなしは日時の新しい順に残す）。URL の `#0?scope=arch&prefix=ARCH&depth=1&limit=50` でも指定できる
  - status の既定は Proposed（無ければすべて）、scope・PREFIX の既定はすべて。URL で検索ワード・scope・PREFIX・status・
    GDR ID のどれかを指定したときは、指定しなかったものは「すべて」になる
  - 検索ワード（空白区切りで AND。GDR ID・要約・scope・本文を大文字小文字を区別せずに探す）も絞り込みに使える。scope / PREFIX と
    併せると、すべてに当てはまる GDR が起点になる。URL では `q=`
  - status でも絞り込める（すべて・有効・失効・各 status。既定は Proposed）。検索ワード・scope・PREFIX の起点と関連の段数でたどった
    GDR のうち、当てはまる status のものだけを描く。URL では `status=`
  - GDR を選ぶと、絞り込み（status・scope・PREFIX・検索ワード・上限）の外にある先祖・子孫・前提・被前提も一時的に描き足す
    （選択を解くと戻る）
  - GDR を選んでいない間は、右に目次を出す（表示中の GDR を文書ごとに並べる。絞り込み・段数・上限・線のない GDR を隠す、に従う。
    絞り込み中は当てはまる GDR を太字、たどった関連を薄字にする）。項目をクリックするとその GDR を選ぶ

表示には CDN（3d-force-graph / marked / DOMPurify。版を固定し SRI 付き）を使うので、開くときにネット接続が要る。
対応するブラウザは Chrome だけ（ほかのブラウザでの表示は確かめず、合わせない）。
確かめ方（直したら毎回）: `python3 gdr_lineage_3d.py --demo -o 一時ファイル` で「GDR 17 件・違反 1 件・警告 0 件」と出ること、
Chrome で開いて件数の欄が埋まること。
"""
import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

SPEC_VERSION = "v2.6"
TOOL_UPDATED = "2026-11-26"

GID = r"GDR-[A-Z][A-Z0-9]*-\d{3,}"
REC_RE = re.compile(rf"^(?:\*\*({GID}):\s*(.+?)\*\*|#{{1,6}}\s+({GID}):\s*(.+?))\s*$")
GDR_LIKE_RE = re.compile(rf"^(?:\*\*|#{{1,6}}\s+)\s*`?{GID}")
FIELD_RE = re.compile(r"^- \*\*(status|scope|日時|関連|uid)(?::\*\*|\*\*:)\s*(.*)$")
ID_RE = re.compile(GID)
UID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")
STATUSES = ("Proposed", "Accepted", "Implemented", "Superseded", "Rejected")
REL_TYPES = ("depends-on", "refines", "relates-to", "derived-from")
LINEAGE = {"supersedes", "refines", "derived-from"}
DATED = {"supersedes", "derived-from"}  # 日時の順を課すのは因果の 2 種だけ
SKIP_DIRS = {"_archive", "_reference", "review", ".git", "node_modules"}


def git_out(args, cwd):
    try:
        return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError, NotADirectoryError):
        return ""


def git_added_date(path: Path):
    out = git_out(["log", "--diff-filter=A", "--format=%aI", "--", path.name], path.parent).split()
    return out[-1] if out else None


def uid_time(uid):
    if not uid or not UID_RE.match(uid):
        return None
    ms = int(uid.replace("-", "")[:12], 16)
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat()


def md_files(d: Path):
    for f in sorted(d.rglob("*.md")):
        rel = f.relative_to(d).parts
        if any(p in SKIP_DIRS for p in rel[:-1]) or f.name.endswith("_reviewed.md"):
            continue
        yield f


def new_stats():
    return {"issue_refs": 0, "unreadable_status": 0, "unreadable_date": 0, "untyped_refs": 0,
            "unknown_types": 0, "unread_gdr_lines": 0, "copies": 0}


def parse_status(val, rid, edges, stats):
    plain = val.replace("*", "").strip()
    head = re.match(r"[A-Za-z]+", plain)
    status = head.group(0) if head and head.group(0) in STATUSES else "Unreadable"
    if status == "Unreadable":
        stats["unreadable_status"] += 1
    if re.match(r"Superseded\s+by\b", plain):
        for t in ID_RE.findall(plain):
            edges.append((rid, t, "supersedes"))
    m = re.search(r"\bsupersedes\b(.*)", plain)
    if m:
        for t in ID_RE.findall(m.group(1)):
            edges.append((t, rid, "supersedes"))
    return status


def parse_relations(val, rid, edges, stats):
    # 「関連」はカンマ区切り。括弧の中のカンマでは切らない
    for part in re.split(r",(?![^（(]*[)）])", val):
        p = part.strip()
        if not p:
            continue
        m = re.match(r"`?([a-z]+(?:-[a-z]+)*)`?\s+(.*)", p)
        if m and m.group(1) in REL_TYPES:
            typ, rest = m.group(1), m.group(2).strip().strip("`")
            if rest.startswith("§"):
                stats["issue_refs"] += 1  # 課題（§N-M）への参照。系譜の外
                continue
            t = ID_RE.search(rest)  # 注記・リンク・バッククォートが付いていても最初の GDR ID を拾う
            if t:
                edges.append((t.group(0), rid, typ))  # 内部の向き: 親 → 子 / 前提 → 依存側（表示では逆向き）
            else:
                stats["untyped_refs"] += 1
        elif m and "-" in m.group(1) and ID_RE.search(p):
            stats["unknown_types"] += 1
        elif ID_RE.search(p):
            stats["untyped_refs"] += 1  # 型の無い GDR ID。種類が分からないので線にしない


def parse_text(name, text, est, records, edges, stats, dups):
    lines = text.splitlines()
    has_sec1 = any(re.match(r"## 1\.\s*GDR", l) for l in lines)
    in_sec = not has_sec1
    in_code = False
    cur = None
    found = 0
    for line in lines:
        if line.startswith("```"):
            in_code = not in_code
            if cur:
                cur["_body"].append(line)
            continue
        if in_code:
            if cur:
                cur["_body"].append(line)
            continue
        m = REC_RE.match(line) if in_sec else None
        if m:
            rid, title = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
            cur = {"id": rid, "title": title, "file": name, "status": "Proposed", "scope": "", "date": None,
                   "uid": None, "uidDate": None, "estDate": est, "_body": [line]}
            found += 1
            if rid in records:
                dups.append((records[rid], cur))  # 写しか衝突かは uid を読んだ後で判定する
            else:
                records[rid] = cur
            continue
        if in_sec and GDR_LIKE_RE.match(line):
            stats["unread_gdr_lines"] += 1  # GDR らしいのに読めなかった行
        if line.startswith("## ") or line.startswith("# "):
            if has_sec1:
                in_sec = bool(re.match(r"## 1\.\s*GDR", line))
            cur = None
            continue
        if not in_sec or not cur:
            continue
        cur["_body"].append(line)
        fm = FIELD_RE.match(line)
        if not fm:
            continue
        key, val = fm.groups()
        if key == "status":
            cur["status"] = parse_status(val, cur["id"], edges, stats)
        elif key == "scope":
            cur["scope"] = val
        elif key == "日時":
            cur["date"] = val.strip() or None
        elif key == "uid":
            cur["uid"] = val.strip()
            cur["uidDate"] = uid_time(cur["uid"])
        elif key == "関連":
            parse_relations(val, cur["id"], edges, stats)
    return found


def parse_sources(sources):
    """sources: [(name, text, estDate)]"""
    records, edges, stats, files, warnings, dups = {}, [], new_stats(), {}, [], []
    for name, text, est in sources:
        if parse_text(name, text, est, records, edges, stats, dups):
            files[name] = text  # GDR を 1 件以上読めた文書だけを埋め込む
    for prev, d in dups:  # 同じ ID が複数の文書にある: uid が同じ（か両方に無い）なら写し、違えば採番の衝突の疑い
        if (d["uid"] or None) == (prev["uid"] or None):
            stats["copies"] += 1
        else:
            warnings.append({"kind": "id-conflict", "id": d["id"], "files": [prev["file"], d["file"]]})
    seen, uniq = set(), []
    for e in edges:  # 置換は両側に書かれ、写しも同じリンクを持つので重ねない
        if e not in seen:
            seen.add(e)
            uniq.append(e)
    for s, t, _ in uniq:
        for n in (s, t):
            if n not in records:
                records[n] = {"id": n, "title": "（この集合に本文なし。退避済みか別の集合）", "file": "",
                              "status": "Unknown", "scope": "", "date": None, "uid": None,
                              "uidDate": None, "estDate": None, "_body": []}
    by_uid = {}
    for r in records.values():
        if r["uid"]:
            if not UID_RE.match(r["uid"]):
                warnings.append({"kind": "uid-format", "id": r["id"], "uid": r["uid"]})
            by_uid.setdefault(r["uid"], []).append(r["id"])
        body = r.pop("_body")
        while body and body[-1].strip() in ("", "---"):
            body.pop()
        r["md"] = "\n".join(body)
    for u, ids in by_uid.items():
        if len(ids) > 1:
            warnings.append({"kind": "uid-dup", "uid": u, "ids": ids})
    return records, uniq, stats, files, warnings


def parse_when(s, stats):
    """「日時」を (値, 日付で比べるか) にする。読めなければ None"""
    s = s.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return s, True
    s2 = re.sub(r"([+-]\d{2})(\d{2})$", r"\1:\2", s.replace("Z", "+00:00"))
    try:
        dt = datetime.fromisoformat(s2)
    except ValueError:
        stats["unreadable_date"] += 1
        return None
    if dt.tzinfo is None:  # オフセットの無い時刻は日付で比べる
        return dt.date().isoformat(), True
    return dt, False


def older_or_same(p, c):
    if p[1] or c[1]:  # どちらかが日付で比べるもの → 日付で比べ、同日は違反にしない
        pd = p[0] if p[1] else p[0].date().isoformat()
        cd = c[0] if c[1] else c[0].date().isoformat()
        return pd <= cd
    return p[0] <= c[0]


def check(records, edges, stats):
    lin = [(s, t, k) for s, t, k in edges if k in LINEAGE]
    when = {}
    for r in records.values():
        when[r["id"]] = parse_when(r["date"], stats) if r["date"] else None
    violations = []
    for s, t, k in lin:
        if k not in DATED:
            continue
        p, c = when[s], when[t]
        if p and c and not older_or_same(p, c):
            violations.append({"kind": "date", "parent": s, "child": t, "type": k})
    adj = {}
    for s, t, _ in lin:
        adj.setdefault(s, []).append(t)
    color = {}

    def dfs(u, stack):
        color[u] = 1
        stack.append(u)
        for v in adj.get(u, []):
            if color.get(v) == 1:
                violations.append({"kind": "cycle", "path": stack[stack.index(v):] + [v]})
            elif not color.get(v):
                dfs(v, stack)
        stack.pop()
        color[u] = 2

    for n in list(adj):
        if not color.get(n):
            dfs(n, [])
    return violations


def build(name, sources, commit=""):
    records, edges, stats, files, warnings = parse_sources(sources)
    violations = check(records, edges, stats)
    bad = set()
    for v in violations:
        if v["kind"] == "date":
            bad.add((v["parent"], v["child"], v["type"]))
        else:
            for a, b in zip(v["path"], v["path"][1:]):
                for k in LINEAGE:
                    bad.add((a, b, k))
    links = [{"source": s, "target": t, "type": k, "violation": (s, t, k) in bad} for s, t, k in edges]
    counts = {}
    for l in links:
        counts[l["type"]] = counts.get(l["type"], 0) + 1
    real = [r for r in records.values() if r["status"] != "Unknown"]
    return {"name": name, "commit": commit, "files": files, "nodes": list(records.values()), "links": links,
            "violations": violations, "warnings": warnings,
            "stats": {"records": len(real), "dated": sum(1 for r in real if r["date"]),
                      "edgeCounts": counts, **stats}}


def dir_sources(d: Path):
    return [(str(f.relative_to(d)), f.read_text(encoding="utf-8"), git_added_date(f)) for f in md_files(d)]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("dirs", nargs="*", help="GDR の置き場（ラベル=ディレクトリ も可）")
    ap.add_argument("-o", "--out", default="lineage_3d.html")
    ap.add_argument("--demo", action="store_true", help="架空の GDR の見本を加える")
    a = ap.parse_args()
    specs = a.dirs or ([] if a.demo else ["notes/91_gdr"])
    datasets = []
    for spec in specs:
        label, sep, p = spec.partition("=")
        if not sep:
            p = spec
        d = Path(p).expanduser()
        if not d.is_dir():
            ap.error(f"ディレクトリがありません: {p}")
        if not sep:
            label = d.resolve().name  # 絶対パス（利用者名を含む）を HTML に入れない
        datasets.append(build(label, dir_sources(d), git_out(["rev-parse", "--short", "HEAD"], d)))
    if a.demo:
        datasets.insert(0, build("demo: 架空の GDR（系譜・前提・違反の見本）",
                                 [("demo/架空プロジェクトのGDR.md", DEMO_MD, None)]))
    data = json.dumps(datasets, ensure_ascii=False).replace("<", "\\u003c")
    names = " / ".join(f"{ds['name']}{'@' + ds['commit'] if ds['commit'] else ''}" for ds in datasets)
    header = (f"<!-- 生成物・手編集禁止。gdr_lineage_3d.py（GDR 仕様 {SPEC_VERSION} 向け、{TOOL_UPDATED} 版）が "
              f"{datetime.now().astimezone().isoformat(timespec='seconds')} に生成。データ: {names}"
              f"{'（--demo）' if a.demo else ''} -->\n").replace("--", "‐‐").replace("<!‐‐", "<!--").replace("‐‐>", "-->")
    html = TEMPLATE.replace("/*__DATA__*/[]", data).replace("__SPEC__", SPEC_VERSION).replace("__UPDATED__", TOOL_UPDATED)
    Path(a.out).write_text(header + html, encoding="utf-8")
    for ds in datasets:
        s = ds["stats"]
        unread = {k: s[k] for k in ("unreadable_status", "unreadable_date", "untyped_refs", "unknown_types",
                                    "unread_gdr_lines") if s[k]}
        print(f"{ds['name']}: GDR {s['records']} 件 / リンク {s['edgeCounts']} / 違反 {len(ds['violations'])} 件 / "
              f"警告 {len(ds['warnings'])} 件" + (f" / 読めなかったもの {unread}" if unread else ""))
    print(f"→ {a.out}")


DEMO_MD = r'''
# 架空プロジェクトの GDR（系譜ビューの見本）

> 見本で示すもの: 置換の連鎖（ARCH-002 → 009、ARCH-003 → 010）、細分化と派生が合流する GDR（ARCH-012）、前提（depends-on）の連鎖、
> 日時が無く、縦の位置を uid の時刻で決める GDR（UI-007。uid は見本のために作った値で、写さない）、不変条件の違反（UI-006 は派生元 UI-004 より古い日時）、
> refines では日時が逆でも違反にしないこと（ARCH-013 は親 ARCH-011 より古い日時）

## 1. GDR（General Decision Record）

**GDR-INFRA-001: 基盤に AWS を採用する**

- **status:** Implemented
- **scope:** infra
- **日時:** 2026-02-15T10:00:00+09:00

**GDR-INFRA-002: アプリの実行環境は ECS on Fargate にする**

- **status:** Implemented
- **scope:** infra
- **日時:** 2026-03-20T10:00:00+09:00
- **関連:** refines GDR-INFRA-001

**GDR-ARCH-001: モノリスで始める**

- **status:** Implemented
- **scope:** arch
- **日時:** 2026-03-01T10:00:00+09:00

**GDR-UI-001: フロントエンドは SPA にする**

- **status:** Implemented
- **scope:** ui
- **日時:** 2026-03-05T10:00:00+09:00
- **関連:** depends-on GDR-ARCH-001

**GDR-ARCH-002: セッションストアを Memcached にする**

- **status:** Superseded by GDR-ARCH-009
- **scope:** arch, perf
- **日時:** 2026-04-10T10:00:00+09:00
- **関連:** depends-on GDR-INFRA-001

**GDR-ARCH-003: ログは各サーバーのファイルに出す**

- **status:** Superseded by GDR-ARCH-010
- **scope:** arch, ops
- **日時:** 2026-04-12T10:00:00+09:00

**GDR-ARCH-005: API を GraphQL に統一する**

- **status:** Rejected
- **scope:** arch
- **日時:** 2026-05-01T10:00:00+09:00
- **関連:** refines GDR-ARCH-001

**GDR-UI-004: 設定画面をモーダルに統合する**

- **status:** Rejected
- **scope:** ui
- **日時:** 2026-06-01T10:00:00+09:00
- **関連:** refines GDR-UI-001

**GDR-UI-006: 設定画面を専用ページにする**

- **status:** Implemented
- **scope:** ui
- **決定:** 設定画面は専用のページにする（モーダルにはしない）
- **理由:** 項目が多く、モーダルではスクロールが二重になる。却下したモーダル案（UI-004）の検討から生まれた
- **影響:** 設定へのリンクを各画面のヘッダに置く
- **再検討条件:** 設定項目が 5 個以下に減る
- **日時:** 2026-05-20T10:00:00+09:00
- **関連:** derived-from GDR-UI-004

**GDR-UI-007: 設定画面をタブで分割する**

- **status:** Accepted
- **scope:** ui
- **関連:** refines GDR-UI-006
- **uid:** 019f1b30-a280-7a3c-9b1e-44d2f08c6a15

**GDR-ARCH-010: ログは CloudWatch Logs に集約する**

- **status:** Accepted (supersedes GDR-ARCH-003)
- **scope:** arch, ops
- **日時:** 2026-07-05T10:00:00+09:00
- **関連:** depends-on GDR-INFRA-001

**GDR-ARCH-009: セッションストアを Redis に統一する**

- **status:** Implemented (supersedes GDR-ARCH-002)
- **scope:** arch, perf
- **決定:** セッションストアを Memcached から Redis に移す
- **理由:** 永続化とレプリケーションが要るようになった。Memcached では再起動でセッションが消える
- **影響:** ARCH-002 は失効。キー命名（ARCH-011）と運用（INFRA-004）を決め直す
- **再検討条件:** セッションを持たない認証方式に移る
- **日時:** 2026-11-02T10:00:00+09:00
- **関連:** depends-on GDR-INFRA-001

**GDR-INFRA-004: Redis は ElastiCache で運用する**

- **status:** Accepted
- **scope:** infra
- **日時:** 2026-08-20T10:00:00+09:00
- **関連:** refines GDR-INFRA-002, depends-on GDR-ARCH-009

**GDR-ARCH-011: Redis のキー命名規則を定める**

- **status:** Accepted
- **scope:** arch
- **日時:** 2026-09-01T10:00:00+09:00
- **関連:** refines GDR-ARCH-009, depends-on GDR-INFRA-001

**GDR-ARCH-013: Redis のキーの TTL を用途別に定める**

- **status:** Proposed
- **scope:** arch, perf
- **日時:** 2026-08-25T10:00:00+09:00
- **関連:** refines GDR-ARCH-011, relates-to GDR-INFRA-004

**GDR-ARCH-012: 画面向けの集約 API を BFF 層に置く**

- **status:** Proposed
- **scope:** arch
- **日時:** 2026-12-10T10:00:00+09:00
- **関連:** derived-from GDR-ARCH-005, refines GDR-ARCH-009, depends-on GDR-UI-001

**GDR-META-001: GDR を notes/91_gdr/ に置く**

- **status:** Implemented
- **scope:** meta
- **日時:** 2026-02-01T10:00:00+09:00
'''

TEMPLATE = r'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GDR 系譜 3D</title>
<style>
  :root { --bg:#0b0f19; --panel:rgba(15,23,42,.92); --line:#334155; --fg:#e2e8f0; --mut:#94a3b8; --acc:#38bdf8; --bad:#ef4444; }
  html,body { margin:0; height:100%; background:var(--bg); color:var(--fg); font:13px/1.55 system-ui,-apple-system,"Hiragino Sans",sans-serif; overflow:hidden; }
  #graph { position:absolute; inset:0; }
  .panel { position:absolute; z-index:10; background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:12px 14px; }
  #hud { top:12px; left:12px; width:290px; max-height:calc(100% - 24px); overflow:auto; }
  #detail { top:12px; right:12px; width:360px; max-height:calc(100% - 24px); overflow:auto; display:none; }
  h1 { margin:0 0 6px; font-size:15px; color:var(--acc); }
  h2 { margin:12px 0 4px; font-size:12px; color:var(--mut); font-weight:600; }
  label { display:block; cursor:pointer; }
  input[type=search] { width:100%; box-sizing:border-box; background:#1e293b; color:var(--fg); border:1px solid var(--line); border-radius:4px; padding:4px 6px; font:inherit; }
  select { width:100%; background:#1e293b; color:var(--fg); border:1px solid var(--line); border-radius:4px; padding:3px; }
  .row { display:flex; align-items:center; gap:6px; }
  .dot { width:10px; height:10px; border-radius:50%; flex:none; }
  .bar { width:18px; height:3px; flex:none; }
  .mut { color:var(--mut); font-size:12px; }
  .v { color:#fca5a5; cursor:pointer; font-size:12px; }
  .v:hover { text-decoration:underline; }
  pre { margin:6px 0 0; white-space:pre-wrap; font:12px/1.6 ui-monospace,Menlo,monospace; }
  .id { color:var(--acc); cursor:pointer; }
  .id:hover { text-decoration:underline; }
  button { background:#1e293b; color:var(--fg); border:1px solid var(--line); border-radius:4px; padding:2px 8px; cursor:pointer; float:right; }
  #detail { width:420px; }
  #toc { top:12px; right:12px; width:340px; max-height:calc(100% - 24px); overflow:auto; }
  #toc h1 { font-size:14px; }
  #toc details { margin-top:8px; }
  #toc summary { cursor:pointer; color:var(--mut); font-size:12px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
  #toc .ti { display:flex; gap:6px; align-items:baseline; padding:2px 4px; border-radius:4px; cursor:pointer; font-size:12px; }
  #toc .ti:hover { background:#1e293b; }
  #toc .ti .dot { transform:translateY(1px); }
  #toc .ti .tid { color:var(--acc); flex:none; }
  #toc .ti .tt { overflow:hidden; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; }
  #toc .ti.rel { opacity:.7; }
  #toc .ti.seed .tt { font-weight:600; }
  .tabs { display:flex; gap:4px; margin:8px 0 6px; border-bottom:1px solid var(--line); }
  .tabs b { padding:4px 10px; cursor:pointer; color:var(--mut); font-weight:500; border-bottom:2px solid transparent; }
  .tabs b.on { color:var(--fg); border-color:var(--acc); }
  .md { font-size:13px; line-height:1.7; }
  .md h1 { font-size:18px; color:var(--fg); margin:0 0 10px; }
  .md h2 { font-size:15px; color:var(--fg); margin:22px 0 8px; padding-bottom:4px; border-bottom:1px solid var(--line); }
  .md h3,.md h4 { font-size:14px; color:var(--fg); margin:16px 0 6px; }
  .md p { margin:6px 0; }
  .md ul,.md ol { margin:4px 0; padding-left:20px; }
  .md table { border-collapse:collapse; margin:8px 0; font-size:12px; display:block; overflow-x:auto; }
  .md th,.md td { border:1px solid var(--line); padding:4px 8px; vertical-align:top; }
  .md th { background:#1e293b; }
  .md code { background:#1e293b; padding:1px 4px; border-radius:3px; font-size:12px; }
  .md pre { background:#111827; border:1px solid var(--line); border-radius:6px; padding:8px 10px; overflow-x:auto; white-space:pre; }
  .md pre code { background:none; padding:0; }
  .md blockquote { margin:8px 0; padding:2px 12px; border-left:3px solid var(--line); color:var(--mut); }
  .md a { color:var(--acc); }
  .md hr { border:none; border-top:1px solid var(--line); margin:16px 0; }
  .md .gid { color:var(--acc); cursor:pointer; border-bottom:1px dotted var(--acc); }
  .md .gid.missing { color:inherit; cursor:default; border:none; }
  .md .here { background:rgba(56,189,248,.08); outline:1px solid rgba(56,189,248,.4); border-radius:6px; padding:2px 8px; margin:0 -8px; }
  #reader { position:absolute; z-index:20; inset:24px max(24px, calc(50% - 460px)); display:none; flex-direction:column; padding:0; }
  #reader header { display:flex; align-items:center; gap:8px; padding:10px 14px; border-bottom:1px solid var(--line); }
  #reader header span { flex:1; color:var(--acc); font-weight:600; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
  #reader header button { float:none; }
  #readerBody { overflow:auto; padding:16px 24px 40px; }
  button.lnk { float:none; margin-top:8px; }
  @media (max-width:700px) { #reader { inset:8px; } }
  @media (max-width:700px){ #hud{ width:calc(100% - 52px); max-height:40%; } #detail,#toc{ top:auto; bottom:12px; left:12px; width:auto; max-height:45%; } }
</style>
<!-- 版を上げたら integrity を計算しなおす（CDN と npm のパッケージの両方で突き合わせる） -->
<script src="https://cdn.jsdelivr.net/npm/3d-force-graph@1.80.1/dist/3d-force-graph.min.js" integrity="sha384-i98VDQKdpyVrtyuFn0fjUWJBLBmxnqHqOANcvYe9HLJUgT2wPixa4ZkLd7Dh3VEk" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js" integrity="sha384-/TQbtLCAerC3jgaim+N78RZSDYV7ryeoBCVqTuzRrFec2akfBkHS7ACQ3PQhvMVi" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/dompurify@3.5.0/dist/purify.min.js" integrity="sha384-DOUwTXbuiiQxlONuue5N42674XXDfjIJ/LTPtJMZ2ZV1Ir4NRQ3OnM/yM505YQAc" crossorigin="anonymous"></script>
</head>
<body>
<div id="graph"></div>

<div id="hud" class="panel">
  <h1>GDR 系譜 3D</h1>
  <div class="mut">系譜の定義は上流の GDR 仕様 01 §3.1（このツールは __SPEC__ 向け、__UPDATED__ 版）。縦は日時で<b>上ほど古い</b>（親・前提が上）。矢印は関係ビュー（06 §4）と同じ向き</div>
  <h2>データ</h2>
  <select id="ds"></select>
  <div id="stats" class="mut" style="margin-top:4px"></div>
  <h2>絞り込み（検索ワード / scope / PREFIX / status）</h2>
  <input id="fWord" type="search" placeholder="検索ワード（ID・要約・scope・本文。空白区切りで AND）" style="margin-bottom:4px">
  <select id="fScope"></select>
  <select id="fPrefix" style="margin-top:4px"></select>
  <select id="fStatus" style="margin-top:4px"></select>
  <label class="row" style="margin-top:4px">関連の段数 <select id="fDepth" style="width:auto"><option value="1">1 段</option><option value="2">2 段</option><option value="all" selected>すべて</option></select></label>
  <label class="row" style="margin-top:4px">表示数の上限 <select id="fLimit" style="width:auto"><option value="all">なし</option><option value="20">20</option><option value="50" selected>50</option><option value="100">100</option><option value="200">200</option></select></label>
  <div id="fInfo" class="mut"></div>
  <h2>表示</h2>
  <label><input type="checkbox" id="showDep" checked> 前提（depends-on）も描く（refines は親子として常に描く）</label>
  <label><input type="checkbox" id="showRel"> 弱い関連（relates-to）も描く</label>
  <label><input type="checkbox" id="hideIso"> 線のない GDR を隠す</label>
  <h2>status</h2>
  <div id="legStatus"></div>
  <h2>リンク（矢印は子 → 親・新 → 旧）</h2>
  <div id="legLink"></div>
  <h2>不変条件の違反・警告</h2>
  <div id="viol"></div>
  <h2>読めなかったもの</h2>
  <div id="unread" class="mut"></div>
  <div class="mut" style="margin-top:10px">左ドラッグ: 回転 / ホイール: ズーム / 右ドラッグ: 移動<br>クリック: 先祖と子孫を強調 / 背景クリック: 解除<br>右の目次（GDR を選んでいない間）: 表示中の GDR を文書ごとに並べる。クリックで選ぶ</div>
</div>

<div id="detail" class="panel"><button id="close">×</button><div id="detailHead"></div>
  <div class="tabs"><b data-tab="md" class="on">GDR 本文</b><b data-tab="lin">系譜</b></div>
  <div id="tabMd" class="md"></div><div id="tabLin" style="display:none"></div>
  <button id="openDoc" class="lnk">元の文書を読む</button></div>
<div id="toc" class="panel"><h1>目次</h1><div id="tocInfo" class="mut"></div><div id="tocBody"></div></div>
<div id="reader" class="panel"><header><span id="readerTitle"></span><button id="readerClose">閉じる（Esc）</button></header><div id="readerBody" class="md"></div></div>

<script>
const DATASETS = /*__DATA__*/[];

const STATUS = {
  // 色相は関係ビュー（06 §4）にそろえる。暗い背景なので明るさは上げている
  Proposed:    { c:'#60a5fa', l:'Proposed（未確定）' },
  Accepted:    { c:'#2dd4bf', l:'Accepted（合意済み）' },
  Implemented: { c:'#22c55e', l:'Implemented' },
  Superseded:  { c:'#9ca3af', l:'Superseded（失効）' },
  Rejected:    { c:'#8b6b6b', l:'Rejected（失効。灰に赤み）' },
  Unreadable:  { c:'#eab308', l:'status が読めない' },
  Unknown:     { c:'#475569', l:'本文なし（集合の外・退避済み）' },
};
const LINK = {
  'supersedes':   { c:'#f8fafc', l:'supersedes（新 → 旧）親子', lin:true },
  'refines':      { c:'#22d3ee', l:'refines（細分化 → 親）親子', lin:true },
  'derived-from': { c:'#fb923c', l:'derived-from（派生 → 元）親子', lin:true },
  'depends-on':   { c:'#64748b', l:'depends-on（依存側 → 前提）前提', lin:false },
  'relates-to':   { c:'#1e293b', l:'relates-to（弱い関連）', lin:false },
};
const BAD = '#ef4444', DIM = '#1f2937';
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const day = s => s ? s.slice(0,10) : '';

document.getElementById('legStatus').innerHTML = Object.values(STATUS)
  .map(s => `<div class="row"><span class="dot" style="background:${s.c}"></span>${s.l}</div>`).join('');
document.getElementById('legLink').innerHTML = Object.values(LINK)
  .map(s => `<div class="row"><span class="bar" style="background:${s.c};${s.c==='#1e293b'?'outline:1px solid #475569':''}"></span>${s.l}</div>`).join('')
  + `<div class="row"><span class="bar" style="background:${BAD}"></span>不変条件の違反（閉路・置換と派生の日時の逆転）</div>`;

let base = { nodes:[], links:[] }, extended = 0;
let cur, sel = null, hl = { nodes:new Set(), links:new Set() }, seeds = new Set();

if (typeof ForceGraph3D === 'undefined' || typeof marked === 'undefined' || typeof DOMPurify === 'undefined') {
  document.getElementById('stats').textContent = 'CDN からライブラリを読み込めませんでした（オフライン、または integrity の不一致）。';
  throw new Error('libraries not loaded');
}
const Graph = ForceGraph3D()(document.getElementById('graph'))
  .backgroundColor('#0b0f19')
  .nodeRelSize(5)
  .nodeVal(n => n.status === 'Unknown' ? 0.4 : seeds.has(n.id) ? 2.2 : 1)
  .nodeColor(n => (sel && !hl.nodes.has(n.id)) ? DIM : STATUS[n.status]?.c || '#64748b')
  .nodeLabel(n => `<div style="background:rgba(15,23,42,.95);padding:8px 10px;border:1px solid #475569;border-radius:6px;max-width:340px">
      <div style="color:#38bdf8;font-size:11px">${esc(n.id)} · ${esc(n.scope)}</div>
      <div style="font-weight:600;margin:3px 0">${esc(n.title)}</div>
      <div style="font-size:11px;color:#94a3b8">${esc(n.status)} · ${esc(dateLabel(n))}${n.file ? ' · ' + esc(n.file) : ''}</div>${n.uid ? `<div style="font-size:10px;color:#64748b">uid ${esc(n.uid)}</div>` : ''}</div>`)
  .linkColor(l => {
      if (sel && !hl.links.has(l.k)) return DIM;
      return l.violation ? BAD : LINK[l.type].c; })
  .linkWidth(l => l.violation ? 2.5 : LINK[l.type].lin ? 1.2 : 0.3)
  .linkDirectionalArrowLength(l => LINK[l.type].lin ? 5 : 2.5)
  .linkDirectionalArrowRelPos(1)
  .onNodeClick(focusNode)
  .onBackgroundClick(clearSel);

const sid = x => typeof x === 'object' ? x.id : x;
const scopesOf = n => String(n.scope || '').split(',').map(x => x.trim()).filter(Boolean);
const prefixOf = id => (/^GDR-([A-Z][A-Z0-9]*)-/.exec(id) || [])[1] || '';
const dateLabel = n => n.date ? day(n.date) : n.uidDate ? day(n.uidDate) + '（uid の時刻。位置だけ）' : n.estDate ? day(n.estDate) + '（推定: ファイル追加日。位置だけ）' : '日時なし';

function placeY(ds) {
  const t = n => { for (const s of [n.date, n.uidDate, n.estDate]) { const v = s ? Date.parse(s) : NaN; if (Number.isFinite(v)) return v; } return null; };
  const vals = ds.nodes.map(t).filter(v => v != null);
  if (!vals.length) return;
  const lo = Math.min(...vals), hi = Math.max(...vals), H = 60 + 22 * Math.sqrt(ds.nodes.length);
  ds.nodes.forEach(n => { const v = t(n);
    n.fy = (v == null || hi === lo) ? undefined : H - 2 * H * (v - lo) / (hi - lo); });
}

function render() {
  const showDep = document.getElementById('showDep').checked;
  const showRel = document.getElementById('showRel').checked;
  const hideIso = document.getElementById('hideIso').checked;
  let links = cur.links.filter(l => LINK[l.type].lin || (l.type === 'depends-on' && showDep) || (l.type === 'relates-to' && showRel))
    .map(l => ({ ...l, source: l.target, target: l.source }));
  // scope / PREFIX の絞り込み: 当てはまる GDR から、表示中のリンクを向きを問わず指定の段数たどる
  const fs = document.getElementById('fScope').value, fp = document.getElementById('fPrefix').value;
  const fw = document.getElementById('fWord').value.trim(), words = fw.toLowerCase().split(/\s+/).filter(Boolean);
  const hit = n => { const t = [n.id, n.title, n.scope, n.md].join('\n').toLowerCase(); return words.every(w => t.includes(w)); };
  const dv = document.getElementById('fDepth').value, depth = dv === 'all' ? Infinity : +dv;
  const lv = document.getElementById('fLimit').value, limit = lv === 'all' ? Infinity : +lv;
  let nodes = cur.nodes, order = null;
  seeds = new Set();
  if (fs || fp || words.length) {
    seeds = new Set(cur.nodes.filter(n => n.status !== 'Unknown' && (!fs || scopesOf(n).includes(fs)) && (!fp || prefixOf(n.id) === fp) && hit(n)).map(n => n.id));
    const adj = {}; links.forEach(l => { (adj[l.source] ||= []).push(l.target); (adj[l.target] ||= []).push(l.source); });
    const keep = new Set(seeds); let front = [...seeds]; order = [...seeds];
    for (let d = 0; d < depth && front.length; d++) {
      const next = []; front.forEach(id => (adj[id] || []).forEach(v => { if (!keep.has(v)) { keep.add(v); next.push(v); } })); front = next;
      order.push(...next);
    }
    nodes = cur.nodes.filter(n => keep.has(n.id));
    document.getElementById('fInfo').textContent = `当てはまる GDR ${seeds.size} 件（大きい点）＋ 関連 ${keep.size - seeds.size} 件`;
  } else document.getElementById('fInfo').textContent = '';
  // status の絞り込み: 起点とたどった関連のうち、当てはまる status の GDR だけを描く（関連は GDR を選ぶと一時的に足す）
  const fst = document.getElementById('fStatus').value;
  if (fst) { const before = nodes.length; nodes = nodes.filter(n => statusOk(n, fst));
    document.getElementById('fInfo').textContent += `${document.getElementById('fInfo').textContent ? ' / ' : ''}status で ${before - nodes.length} 件を隠す`; }
  // 表示数の上限: 絞り込み中は当てはまる GDR → 近い段の順、絞り込みなしは日時の新しい順（本文なしの点は後ろ）に残す
  if (nodes.length > limit) {
    const total = nodes.length;
    if (!order) { const t = n => { const v = Date.parse(n.date || n.uidDate || n.estDate || ''); return Number.isFinite(v) ? v : -Infinity; };
      order = [...nodes].sort((a, b) => (a.status === 'Unknown') - (b.status === 'Unknown') || t(b) - t(a)).map(n => n.id); }
    const top = new Set(order.slice(0, limit));
    nodes = nodes.filter(n => top.has(n.id));
    document.getElementById('fInfo').textContent += `${document.getElementById('fInfo').textContent ? ' / ' : ''}上限 ${limit} 件を表示（全 ${total} 件）`;
  }
  const shown = new Set(nodes.map(n => n.id));
  links = links.filter(l => shown.has(l.source) && shown.has(l.target));
  const used = new Set(links.flatMap(l => [l.source, l.target]));
  if (hideIso) nodes = nodes.filter(n => used.has(n.id));
  base = { nodes, links }; extended = 0;
  Graph.graphData(base);
  renderToc(nodes, fs, fp, fw, fst);
}

// 目次: 表示中の GDR（絞り込み・段数・上限・線のない GDR を隠す、を反映）を文書ごとに並べる。GDR を選んでいない間だけ右に出す
const STATUS_GROUPS = { active:['Proposed','Accepted','Implemented'], inactive:['Superseded','Rejected'] };
const statusOk = (n, v) => n.status !== 'Unknown' && (STATUS_GROUPS[v] ? STATUS_GROUPS[v].includes(n.status) : n.status === v);
// 描いているリンク（render と同じ規則）に、強調中のリンク（keys）を足したもの。ids の GDR どうしに限る
function linksFor(ids, keys) {
  const showDep = document.getElementById('showDep').checked, showRel = document.getElementById('showRel').checked;
  return cur.links.filter(l => (LINK[l.type].lin || (l.type === 'depends-on' && showDep) || (l.type === 'relates-to' && showRel) || keys.has(l.k))
      && ids.has(sid(l.source)) && ids.has(sid(l.target)))
    .map(l => ({ ...l, source: sid(l.target), target: sid(l.source) }));
}

function renderToc(nodes, fs, fp, fw, fst) {
  const pos = new Map(cur.nodes.map((n, i) => [n.id, i]));
  const groups = new Map();
  [...nodes].sort((a, b) => pos.get(a.id) - pos.get(b.id)).forEach(n => {
    const k = n.status === 'Unknown' || !n.file ? '' : n.file; (groups.get(k) || groups.set(k, []).get(k)).push(n); });
  const keys = [...groups.keys()].filter(k => k).sort().concat(groups.has('') ? [''] : []);
  const stl = fst && document.querySelector(`#fStatus option[value="${fst}"]`)?.textContent;
  const cond = [fw && `「${fw}」`, fs && 'scope: ' + fs, fp && 'PREFIX: ' + fp, stl].filter(Boolean).join(' / ');
  const nReal = nodes.filter(n => n.status !== 'Unknown').length;
  document.getElementById('tocInfo').innerHTML = esc(cond ? `${cond} の表示中 ${nReal} 件` : `表示中 ${nReal} 件（絞り込みなし）`)
    + (seeds.size ? '<br>太字: 当てはまる GDR / 薄字: たどった関連' : '') + (nodes.length ? '' : '<br>表示中の GDR はありません');
  const item = n => `<div class="ti${seeds.size ? (seeds.has(n.id) ? ' seed' : ' rel') : ''}" data-id="${esc(n.id)}" title="${esc(n.id + ': ' + n.title + '（' + n.status + '）')}">`
    + `<span class="dot" style="background:${STATUS[n.status]?.c || '#64748b'}"></span><span class="tid">${esc(n.id)}</span>`
    + `<span class="tt">${esc(String(n.title || '').replace(/\*\*|`/g, ''))}</span></div>`;
  document.getElementById('tocBody').innerHTML = keys.map(k => { const g = groups.get(k);
    return `<details open><summary title="${esc(k)}">${esc(k || '本文なし（集合の外・退避済み）')}（${g.length}）</summary>${g.map(item).join('')}</details>`; }).join('');
  document.getElementById('toc').style.display = sel ? 'none' : '';
}

function fillFilters() {
  const opt = (v, l) => `<option value="${esc(v)}">${esc(l)}</option>`;
  const real = cur.nodes.filter(n => n.status !== 'Unknown');
  const sc = [...new Set(real.flatMap(scopesOf))].sort(), px = [...new Set(real.map(n => prefixOf(n.id)).filter(Boolean))].sort();
  document.getElementById('fScope').innerHTML = opt('', 'scope: すべて') + sc.map(v => opt(v, 'scope: ' + v)).join('');
  document.getElementById('fPrefix').innerHTML = opt('', 'PREFIX: すべて') + px.map(v => opt(v, 'PREFIX: ' + v)).join('');
  const st = Object.keys(STATUS).filter(k => real.some(n => n.status === k));
  document.getElementById('fStatus').innerHTML = opt('', 'status: すべて') + opt('active', 'status: 有効（Proposed / Accepted / Implemented）')
    + opt('inactive', 'status: 失効（Superseded / Rejected）') + st.map(v => opt(v, 'status: ' + v)).join('');
}

function loadDataset(i, f) {
  cur = DATASETS[i]; clearSel(); fillFilters();
  document.getElementById('fWord').value = f?.get('q') || '';
  // status の既定は Proposed（未確定の GDR に絞ると初回の表示件数を抑えられる。Proposed が無いデータセットではすべて）。
  // scope・PREFIX の既定はすべて。URL で検索ワード・scope・PREFIX・status・GDR ID のどれかを指定したときは、
  // 指定しなかったものを「すべて」のままにする
  if (!f || !['q','scope','prefix','status','id'].some(k => f.get(k))) {
    const fstEl = document.getElementById('fStatus');
    if ([...fstEl.options].some(o => o.value === 'Proposed')) fstEl.value = 'Proposed';
  }
  if (f) { for (const [k, id] of [['scope','fScope'],['prefix','fPrefix'],['status','fStatus'],['depth','fDepth'],['limit','fLimit']]) { const v = f.get(k); if (v != null && [...document.getElementById(id).options].some(o => o.value === v)) document.getElementById(id).value = v; } }
  if (!cur._placed) { placeY(cur); cur.links.forEach((l, i) => l.k = i); cur._placed = true; }
  const s = cur.stats, ec = s.edgeCounts;
  const lin = (ec['supersedes']||0) + (ec['refines']||0) + (ec['derived-from']||0);
  document.getElementById('stats').innerHTML =
    `GDR ${s.records} 件（日時あり ${s.dated}）<br>系譜のリンク ${lin}（置換 ${ec['supersedes']||0} / refines ${ec['refines']||0} / derived-from ${ec['derived-from']||0}）<br>`+
    `系譜の外: depends-on ${ec['depends-on']||0} / relates-to ${ec['relates-to']||0} / 課題への derived-from ${s.issue_refs}`;
  const W = { 'uid-dup': w => `uid の重複: ${esc(w.ids.join(' / '))}`, 'uid-format': w => `uid の形式が UUID v7 でない: ${esc(w.id)}`,
    'id-conflict': w => `同じ ID で uid が違う（採番の衝突の疑い）: ${esc(w.id)}（${esc(w.files.join(' / '))}）` };
  const vs = cur.violations.map(v => v.kind === 'date'
      ? `<div class="v" data-id="${esc(v.child)}">日時の逆転: ${esc(v.child)} → ${esc(v.parent)}（${esc(v.type)}。子の日時が親より古い）</div>`
      : `<div class="v" data-id="${esc(v.path[0])}">閉路: ${esc(v.path.join(' → '))}</div>`)
    .concat(cur.warnings.map(w => `<div class="v" data-id="${esc(w.id || w.ids[0])}">警告: ${W[w.kind](w)}</div>`));
  document.getElementById('viol').innerHTML = vs.length ? vs.join('') : '<div class="mut">なし</div>';
  const U = { unreadable_status:'status', unreadable_date:'日時', untyped_refs:'型の無い・対象の読めない関連', unknown_types:'知らない型の関連', unread_gdr_lines:'GDR らしいのに読めなかった行' };
  const ur = Object.entries(U).filter(([k]) => s[k]).map(([k, l]) => `${l} ${s[k]}`);
  document.getElementById('unread').innerHTML = (ur.length ? ur.join(' / ') : 'なし') + (s.copies ? `<br>同じ GDR の写し ${s.copies} 件を 1 件にまとめた` : '');
  render();
  setTimeout(() => Graph.zoomToFit(600, 40), 1500);
}

function lineageMaps() {
  const up = {}, down = {}, pre = {}, preOf = {};
  cur.links.forEach(l => { const s = sid(l.source), t = sid(l.target);
    if (LINK[l.type].lin) { (up[t] ||= []).push([s, l]); (down[s] ||= []).push([t, l]); }
    if (l.type === 'depends-on' || l.type === 'refines') { (pre[t] ||= []).push([s, l]); (preOf[s] ||= []).push([t, l]); } });
  return { up, down, pre, preOf };
}

function tree(id, map, depth, seen, out) {
  for (const [nid, l] of (map[id] || [])) {
    hl.nodes.add(nid); hl.links.add(l.k);
    const n = byId(nid);
    const label = ' — ' + l.type;
    out.push(`${'  '.repeat(depth)}<span class="id" data-id="${esc(nid)}">${esc(nid)}</span>（${esc(n.status)}, ${esc(dateLabel(n))}）${label}${l.violation ? ' <span style="color:#fca5a5">⚠ 日時の逆転</span>' : ''}`);
    if (!seen.has(nid)) { seen.add(nid); tree(nid, map, depth + 1, seen, out); }
  }
  return out;
}
const byId = id => cur.nodes.find(n => n.id === id);

function focusNode(node) {
  sel = node.id; hl = { nodes:new Set([node.id]), links:new Set() };
  const m = lineageMaps();
  const anc = tree(node.id, m.up, 1, new Set(), []);
  const desc = tree(node.id, m.down, 1, new Set(), []);
  const pre = tree(node.id, m.pre, 1, new Set(), []);
  const preOf = tree(node.id, m.preOf, 1, new Set(), []);
  // 絞り込みの外にある関連（先祖・子孫・前提・被前提）を一時的に描き足す。選択を解くと戻す
  const shownIds = new Set(base.nodes.map(n => n.id));
  const extra = [...hl.nodes].filter(id => !shownIds.has(id)).map(byId).filter(Boolean);
  if (extra.length || extended) {
    const ids = new Set([...shownIds, ...extra.map(n => n.id)]);
    Graph.graphData({ nodes:[...base.nodes, ...extra], links:linksFor(ids, hl.links) });
    extended = extra.length;
  }
  const role = !m.up[node.id] && !m.down[node.id] ? '（系譜のリンクなし）' : !m.up[node.id] ? '（起点）' : !m.down[node.id] ? '（末端）' : '';
  document.getElementById('detailHead').innerHTML =
    `<div style="color:#38bdf8;font-size:12px">${esc(node.id)} · ${esc(node.scope)} · ${esc(node.file)}</div>
     <div style="font-weight:600;margin:4px 0 0" class="md">${DOMPurify.sanitize(marked.parseInline(node.title), PURIFY)}</div>`
    + (extended ? `<div class="mut" style="margin-top:4px">絞り込みの外にある関連 ${extended} 件を一時的に表示中（選択を解くと戻る）</div>` : '');
  const mdEl = document.getElementById('tabMd');
  if (node.md) renderMd(mdEl, node.md); else mdEl.innerHTML = '<p class="mut">この集合に本文がありません。</p>';
  document.getElementById('openDoc').style.display = node.file ? '' : 'none';
  document.getElementById('openDoc').onclick = () => openReader(node.file, node.id);
  document.getElementById('tabLin').innerHTML = `<pre>${esc(node.id)}（${esc(node.status)}, ${esc(dateLabel(node))}）${role}
先祖:
${anc.length ? anc.join('\n') : '  なし（起点）'}
子孫:
${desc.length ? desc.join('\n') : '  なし（末端）'}
前提:
${pre.length ? pre.join('\n') : '  なし'}
被前提:
${preOf.length ? preOf.join('\n') : '  なし'}</pre>`;
  document.getElementById('detail').style.display = 'block';
  document.getElementById('toc').style.display = 'none';
  refresh();
  const cam = () => { const d = 90, r = 1 + d / Math.hypot(node.x || 1, node.y || 1, node.z || 1);
    Graph.cameraPosition({ x:(node.x || 0) * r, y:(node.y || 0) * r, z:(node.z || 0) * r }, node, 900); };
  if (node.x == null) setTimeout(cam, 800); else cam();
}
function clearSel() { sel = null; hl = { nodes:new Set(), links:new Set() };
  if (extended) { Graph.graphData(base); extended = 0; }
  document.getElementById('detail').style.display = 'none'; document.getElementById('toc').style.display = ''; refresh(); }
function refresh() { Graph.nodeColor(Graph.nodeColor()).linkColor(Graph.linkColor()); }

const ID_RE = /GDR-[A-Z][A-Z0-9]*-\d{3,}/g;
// 本文の生の HTML で、表示を壊したり偽ったりできるものを通さない
const PURIFY = { FORBID_TAGS:['style','form','input','textarea','select','button'], FORBID_ATTR:['id','name','style'] };
// 日本語の約物（「」（）など）に隣接する **太字** を CommonMark が閉じない問題の補正
marked.use({ tokenizer: { emStrong(src) {
  const m = /^\*\*(?=\S)([^*\n]*?\S)\*\*/.exec(src);
  return m ? { type:'strong', raw:m[0], text:m[1], tokens:this.lexer.inlineTokens(m[1]) } : false;
} } });
function renderMd(el, src) {
  el.innerHTML = DOMPurify.sanitize(marked.parse(src, { gfm:true }), PURIFY);
  el.querySelectorAll('a[href]').forEach(a => { a.target = '_blank'; a.rel = 'noopener'; });
  // 本文中の GDR ID をクリックでその GDR へ移動できるようにする
  const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
  const texts = []; while (walker.nextNode()) texts.push(walker.currentNode);
  for (const t of texts) {
    if (!ID_RE.test(t.nodeValue)) continue; ID_RE.lastIndex = 0;
    const frag = document.createDocumentFragment(); let last = 0;
    t.nodeValue.replace(ID_RE, (m, i) => {
      frag.append(t.nodeValue.slice(last, i));
      const sp = document.createElement('span');
      const ok = cur.nodes.some(n => n.id === m);
      sp.className = ok ? 'gid' : 'gid missing'; if (ok) sp.dataset.id = m; sp.textContent = m;
      frag.append(sp); last = i + m.length;
    });
    frag.append(t.nodeValue.slice(last)); t.replaceWith(frag);
  }
}
function openReader(file, id) {
  const src = cur.files?.[file]; if (src == null) return;
  document.getElementById('readerTitle').textContent = file;
  const body = document.getElementById('readerBody');
  renderMd(body, src);
  document.getElementById('reader').style.display = 'flex';
  // 対象の GDR の始まり（**GDR-…: …** の段落か ## GDR-…: の見出し）を探して強調・スクロール
  const p = [...body.querySelectorAll('p, h1, h2, h3, h4, h5, h6')].find(p => (p.tagName !== 'P' || p.firstElementChild?.tagName === 'STRONG') && p.textContent.trim().startsWith(id + ':'));
  if (p) { p.classList.add('here'); requestAnimationFrame(() => p.scrollIntoView({ block:'start' })); } else body.scrollTop = 0;
}
function closeReader() { document.getElementById('reader').style.display = 'none'; }
document.getElementById('readerClose').onclick = closeReader;
document.addEventListener('keydown', e => { if (e.key === 'Escape') { if (document.getElementById('reader').style.display === 'flex') closeReader(); else clearSel(); } });
document.querySelectorAll('.tabs b').forEach(b => b.onclick = () => {
  document.querySelectorAll('.tabs b').forEach(x => x.classList.toggle('on', x === b));
  document.getElementById('tabMd').style.display = b.dataset.tab === 'md' ? '' : 'none';
  document.getElementById('tabLin').style.display = b.dataset.tab === 'lin' ? '' : 'none';
});
document.addEventListener('click', e => { const id = e.target.closest?.('[data-id]')?.dataset.id; if (!id) return;
  const n = Graph.graphData().nodes.find(n => n.id === id) || cur.nodes.find(n => n.id === id);
  if (!n) return; closeReader(); focusNode(n); });
document.getElementById('close').onclick = clearSel;
let wordTimer; document.getElementById('fWord').oninput = () => { clearTimeout(wordTimer); wordTimer = setTimeout(() => { clearSel(); render(); }, 250); };
['showDep','showRel','hideIso','fScope','fPrefix','fStatus','fDepth','fLimit'].forEach(id => document.getElementById(id).onchange = () => { clearSel(); render(); });
const dsSel = document.getElementById('ds');
dsSel.innerHTML = DATASETS.map((d, i) => `<option value="${i}">${esc(d.name)}</option>`).join('');
dsSel.onchange = () => loadDataset(+dsSel.value);
window.addEventListener('resize', () => Graph.width(innerWidth).height(innerHeight));
// URL の # で開く GDR と絞り込みを指定できる（# の後は データセットの番号（0 から）/ GDR ID / doc ? q=…&scope=…&prefix=…&status=Proposed|…|active|inactive&depth=1|2|all&limit=20|50|100|200。
// 例: #1/GDR-META-040、#0/GDR-ARCH-012/doc、#0?scope=ui&depth=1、#0?limit=50）
let hash = ''; try { hash = decodeURIComponent(location.hash.slice(1)); } catch (e) {}
const [hPath, hQs] = hash.split('?');
const [hDs, hId, hDoc] = hPath.split('/');
const hFilter = new URLSearchParams(hQs || '');
const hIdx = /^\d+$/.test(hDs || '') && +hDs < DATASETS.length ? +hDs : 0;
if (hId) hFilter.set('id', hId);
dsSel.value = hIdx; loadDataset(hIdx, hFilter);
if (hId) setTimeout(() => { const n = cur.nodes.find(n => n.id === hId); if (!n) return;
  focusNode(n); if (hDoc === 'doc' && n.file) openReader(n.file, n.id); }, 2500);
</script>
</body>
</html>
'''


if __name__ == "__main__":
    main()
