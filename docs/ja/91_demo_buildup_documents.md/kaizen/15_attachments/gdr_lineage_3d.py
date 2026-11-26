#!/usr/bin/env python3
"""GDR の系譜（GDR-META-040）を 3D で俯瞰する単一 HTML を生成する。Python 3 の標準ライブラリだけで動く。

使い方:
  python3 gdr_lineage_3d.py [ディレクトリ ...] [-o lineage_3d.html] [--demo]

  ディレクトリ   GDR を含む Markdown の置き場（既定: notes/91_gdr）。1 つが 1 データセットになる
                 （`ラベル=ディレクトリ` でラベルを付けられる）。下の階層も読む。`_archive` / `_reference` と
                 `*_reviewed.md` は読まない（notes/_archive/ は明示指定時のみ読む規則に合わせる）
  --demo         架空の GDR（系譜・前提・違反の見本）をデータセットに加える
  -o             出力先（既定: lineage_3d.html）。生成物は既定ではコミットしない（GDR-META-026）

読み方:
  - 親子（系譜）: 置換（status 行の Superseded by / supersedes）・refines・GDR を指す derived-from
  - 前提: depends-on（親子とは別に、同じ重みで並べる）。relates-to は弱い関連
  - 不変条件: 親子は閉路を持たない / 置換と GDR 向き derived-from では親の日時 <= 子の日時
    （日付のみのときは日付で比べ、同日は違反としない。「日時」が無い端は uid の時刻で代える。refines は日時を比べない）
  - 「## 1.」節を持つ文書（改善提案）はその節の GDR だけを、それ以外は文書全体の GDR を読む。コードブロック内は読まない
  - 縦の位置は 日時 > uid の時刻 > ファイルの git 追加日（推定。位置にだけ使う）の順で決める

表示には CDN（3d-force-graph / marked / DOMPurify）を使うので、開くときにネット接続が要る。
"""
import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REC_RE = re.compile(r"^\*\*(GDR-[A-Z]+-\d{3}):\s*(.+?)\*\*\s*$")
FIELD_RE = re.compile(r"^- \*\*(status|scope|日時|関連|uid):\*\*\s*(.*)$")
ID_RE = re.compile(r"GDR-[A-Z]+-\d{3}")
UID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")
LINEAGE = {"supersedes", "refines", "derived-from"}
DATED = {"supersedes", "derived-from"}  # 日時の順を課すのは因果の 2 種だけ
SKIP_DIRS = {"_archive", "_reference", ".git", "node_modules"}


def git_added_date(path: Path):
    try:
        out = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%aI", "--", path.name],
            cwd=path.parent, capture_output=True, text=True, check=True,
        ).stdout.split()
        return out[-1] if out else None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


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


def parse_text(name, text, est, records, edges, stats):
    has_sec1 = any(l.startswith("## 1.") for l in text.splitlines())
    in_sec = not has_sec1
    in_code = False
    cur = None
    for line in text.splitlines():
        if line.startswith("```"):
            in_code = not in_code
            if cur:
                cur["_body"].append(line)
            continue
        if in_code:
            if cur:
                cur["_body"].append(line)
            continue
        if line.startswith("## ") or line.startswith("# "):
            if has_sec1:
                in_sec = line.startswith("## 1.")
            cur = None
            continue
        if not in_sec:
            continue
        m = REC_RE.match(line)
        if m:
            cur = {"id": m.group(1), "title": m.group(2), "file": name, "status": "Proposed",
                   "scope": "", "date": None, "uid": None, "uidDate": None,
                   "estDate": est, "_body": [line]}
            records[cur["id"]] = cur
            continue
        if not cur:
            continue
        cur["_body"].append(line)
        fm = FIELD_RE.match(line)
        if not fm:
            continue
        key, val = fm.groups()
        if key == "status":
            cur["status"] = val.split()[0] if val.split() else "Proposed"
            if val.startswith("Superseded by"):
                for t in ID_RE.findall(val):
                    edges.append((cur["id"], t, "supersedes"))
            for t in re.findall(r"supersedes\s+(GDR-[A-Z]+-\d{3})", val):
                edges.append((t, cur["id"], "supersedes"))
        elif key == "scope":
            cur["scope"] = val
        elif key == "日時":
            cur["date"] = val.strip() or None
        elif key == "uid":
            cur["uid"] = val.strip()
            cur["uidDate"] = uid_time(cur["uid"])
        elif key == "関連":
            for part in val.split(","):
                bits = part.strip().split()
                if len(bits) < 2:
                    continue
                typ, target = bits[0], bits[1]
                if not ID_RE.fullmatch(target):
                    stats["issue_refs"] += 1  # 課題（§N-M）への derived-from など。系譜の外
                    continue
                if typ in ("refines", "derived-from", "depends-on", "relates-to"):
                    # 内部の向き: 親 → 子 / 前提 → 依存側 / 相手 → 書いた側（表示では逆向きに描く）
                    edges.append((target, cur["id"], typ))


def parse_sources(sources):
    """sources: [(name, text, estDate)]"""
    records, edges, stats, files = {}, [], {"issue_refs": 0}, {}
    for name, text, est in sources:
        files[name] = text
        parse_text(name, text, est, records, edges, stats)
    seen, uniq = set(), []
    for e in edges:  # 置換は両側に書かれるので重ねない
        if e not in seen:
            seen.add(e)
            uniq.append(e)
    for s, t, _ in uniq:
        for n in (s, t):
            if n not in records:
                records[n] = {"id": n, "title": "（この集合に本文なし。退避済みか別の集合）", "file": "",
                              "status": "Unknown", "scope": "", "date": None, "uid": None,
                              "uidDate": None, "estDate": None, "_body": []}
    for r in records.values():
        body = r.pop("_body")
        while body and body[-1].strip() in ("", "---"):
            body.pop()
        r["md"] = "\n".join(body)
    return records, uniq, stats, files


def when(r):
    """不変条件に使う時刻: (値, 日付のみか)。日時 > uid の時刻"""
    s = r["date"] or r["uidDate"]
    if not s:
        return None
    s = s.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return s, True
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")), False
    except ValueError:
        return s[:10], True


def older_or_same(p, c):
    if p[1] or c[1]:  # どちらかが日付のみ → 日付で比べ、同日は違反にしない
        pd = p[0] if p[1] else p[0].date().isoformat()
        cd = c[0] if c[1] else c[0].date().isoformat()
        return pd <= cd
    a, b = p[0], c[0]
    if (a.tzinfo is None) != (b.tzinfo is None):
        a, b = a.replace(tzinfo=None), b.replace(tzinfo=None)
    return a <= b


def check(records, edges):
    lin = [(s, t, k) for s, t, k in edges if k in LINEAGE]
    violations = []
    for s, t, k in lin:
        if k not in DATED:
            continue
        p, c = when(records[s]), when(records[t])
        if p and c and not older_or_same(p, c):
            violations.append({"kind": "date", "source": s, "target": t, "type": k})
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


def build(name, sources):
    records, edges, stats, files = parse_sources(sources)
    violations = check(records, edges)
    bad = {(v["source"], v["target"]) for v in violations if v["kind"] == "date"}
    links = [{"source": s, "target": t, "type": k, "violation": (s, t) in bad} for s, t, k in edges]
    counts = {}
    for l in links:
        counts[l["type"]] = counts.get(l["type"], 0) + 1
    real = [r for r in records.values() if r["status"] != "Unknown"]
    return {"name": name, "files": files, "nodes": list(records.values()), "links": links,
            "violations": violations,
            "stats": {"records": len(real), "dated": sum(1 for r in real if r["date"]),
                      "edgeCounts": counts, **stats}}


def dir_sources(d: Path):
    out = []
    for f in md_files(d):
        out.append((str(f.relative_to(d)), f.read_text(encoding="utf-8"), git_added_date(f)))
    return out


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
            label, p = spec, spec
        d = Path(p).expanduser()
        if not d.is_dir():
            ap.error(f"ディレクトリがありません: {p}")
        datasets.append(build(label, dir_sources(d)))
    if a.demo:
        datasets.insert(0, build("demo: 架空の GDR（系譜・前提・違反の見本）",
                                 [("demo/架空プロジェクトのGDR.md", DEMO_MD, None)]))
    data = json.dumps(datasets, ensure_ascii=False).replace("</", "<\\/")
    Path(a.out).write_text(TEMPLATE.replace("/*__DATA__*/[]", data), encoding="utf-8")
    for ds in datasets:
        print(f"{ds['name']}: GDR {ds['stats']['records']} 件 / リンク {ds['stats']['edgeCounts']} / "
              f"違反 {len(ds['violations'])} 件")
    print(f"→ {a.out}")


DEMO_MD = r'''
# 架空プロジェクトの GDR（系譜ビューの見本）

> 見本で示すもの: 置換の連鎖（ARCH-002 → 009、ARCH-003 → 010）、細分化と派生が合流する GDR（ARCH-012）、前提（depends-on）の連鎖、
> 日時が無く uid の時刻で補う GDR（UI-007）、不変条件の違反（UI-006 は派生元 UI-004 より古い日時）、
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
- **日時:** 2026-08-15T10:00:00+09:00
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
- **関連:** refines GDR-ARCH-009

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
  @media (max-width:700px){ #hud{ width:calc(100% - 52px); max-height:40%; } #detail{ top:auto; bottom:12px; left:12px; width:auto; max-height:45%; } }
</style>
<script src="https://cdn.jsdelivr.net/npm/3d-force-graph@1.80.1/dist/3d-force-graph.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/dompurify@3.1.6/dist/purify.min.js"></script>
</head>
<body>
<div id="graph"></div>

<div id="hud" class="panel">
  <h1>GDR 系譜 3D</h1>
  <div class="mut">系譜の定義は GDR-META-040。縦は日時で<b>上ほど古い</b>（親・前提が上）。矢印は関係ビュー（06 §4）と同じ向き</div>
  <h2>データ</h2>
  <select id="ds"></select>
  <div id="stats" class="mut" style="margin-top:4px"></div>
  <h2>表示</h2>
  <label><input type="checkbox" id="showDep" checked> 前提（depends-on）も描く</label>
  <label><input type="checkbox" id="showRel"> 弱い関連（relates-to）も描く</label>
  <label><input type="checkbox" id="hideIso"> 線のない GDR を隠す</label>
  <h2>status</h2>
  <div id="legStatus"></div>
  <h2>リンク（矢印は子 → 親・新 → 旧）</h2>
  <div id="legLink"></div>
  <h2>不変条件の違反</h2>
  <div id="viol"></div>
  <div class="mut" style="margin-top:10px">左ドラッグ: 回転 / ホイール: ズーム / 右ドラッグ: 移動<br>クリック: 先祖と子孫を強調 / 背景クリック: 解除</div>
</div>

<div id="detail" class="panel"><button id="close">×</button><div id="detailHead"></div>
  <div class="tabs"><b data-tab="md" class="on">GDR 本文</b><b data-tab="lin">系譜</b></div>
  <div id="tabMd" class="md"></div><div id="tabLin" style="display:none"></div>
  <button id="openDoc" class="lnk">元の文書を読む</button></div>
<div id="reader" class="panel"><header><span id="readerTitle"></span><button id="readerClose">閉じる（Esc）</button></header><div id="readerBody" class="md"></div></div>

<script>
const DATASETS = /*__DATA__*/[];

const STATUS = {
  Proposed:    { c:'#94a3b8', l:'Proposed（未確定）' },
  Accepted:    { c:'#38bdf8', l:'Accepted（合意済み）' },
  Implemented: { c:'#22c55e', l:'Implemented' },
  Superseded:  { c:'#a16207', l:'Superseded（失効）' },
  Rejected:    { c:'#a855f7', l:'Rejected（失効）' },
  Unknown:     { c:'#475569', l:'本文なし（集合の外）' },
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
  + `<div class="row"><span class="bar" style="background:${BAD}"></span>不変条件の違反（置換・派生の日時の逆転）</div>`;

let cur, sel = null, hl = { nodes:new Set(), links:new Set() };

const Graph = ForceGraph3D()(document.getElementById('graph'))
  .backgroundColor('#0b0f19')
  .nodeRelSize(5)
  .nodeVal(n => n.status === 'Unknown' ? 0.4 : 1)
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
  .linkDirectionalParticles(l => LINK[l.type].lin ? 2 : 0)
  .linkDirectionalParticleSpeed(0.006)
  .linkDirectionalParticleWidth(1.8)
  .onNodeClick(focusNode)
  .onBackgroundClick(clearSel);

const sid = x => typeof x === 'object' ? x.id : x;
const dateLabel = n => n.date ? day(n.date) : n.uidDate ? day(n.uidDate) + '（uid の時刻）' : n.estDate ? day(n.estDate) + '（推定: ファイル追加日）' : '日時なし';

function placeY(ds) {
  const t = n => { const s = n.date || n.uidDate || n.estDate; return s ? Date.parse(s) : null; };
  const vals = ds.nodes.map(t).filter(v => v != null);
  const lo = Math.min(...vals), hi = Math.max(...vals), H = 60 + 22 * Math.sqrt(ds.nodes.length);
  ds.nodes.forEach(n => { const v = t(n);
    n.fy = (v == null || hi === lo) ? undefined : H - 2 * H * (v - lo) / (hi - lo); });
}

function render() {
  const showDep = document.getElementById('showDep').checked;
  const showRel = document.getElementById('showRel').checked;
  const hideIso = document.getElementById('hideIso').checked;
  const links = cur.links.filter(l => LINK[l.type].lin || (l.type === 'depends-on' && showDep) || (l.type === 'relates-to' && showRel))
    .map(l => ({ ...l, source: l.target, target: l.source }));
  const used = new Set(links.flatMap(l => [l.source, l.target]));
  const nodes = hideIso ? cur.nodes.filter(n => used.has(n.id)) : cur.nodes;
  Graph.graphData({ nodes, links });
}

function loadDataset(i) {
  cur = DATASETS[i]; clearSel();
  if (!cur._placed) { placeY(cur); cur.links.forEach((l, i) => l.k = i); cur._placed = true; }
  const s = cur.stats, ec = s.edgeCounts;
  const lin = (ec['supersedes']||0) + (ec['refines']||0) + (ec['derived-from']||0);
  document.getElementById('stats').innerHTML =
    `GDR ${s.records} 件（日時あり ${s.dated}）<br>系譜のリンク ${lin}（置換 ${ec['supersedes']||0} / refines ${ec['refines']||0} / derived-from ${ec['derived-from']||0}）<br>`+
    `系譜の外: depends-on ${ec['depends-on']||0} / relates-to ${ec['relates-to']||0} / 課題への derived-from ${s.issue_refs}`;
  document.getElementById('viol').innerHTML = cur.violations.length ? cur.violations.map(v => v.kind === 'date'
      ? `<div class="v" data-id="${esc(v.target)}">日時の逆転: ${esc(v.source)} → ${esc(v.target)}（${esc(v.type)}）</div>`
      : `<div class="v" data-id="${esc(v.path[0])}">閉路: ${esc(v.path.join(' → '))}</div>`).join('')
    : '<div class="mut">なし</div>';
  render();
  setTimeout(() => Graph.zoomToFit(600, 40), 1500);
}

function lineageMaps() {
  const up = {}, down = {}, pre = {}, preOf = {};
  cur.links.forEach(l => { const s = sid(l.source), t = sid(l.target);
    if (LINK[l.type].lin) { (up[t] ||= []).push([s, l]); (down[s] ||= []).push([t, l]); }
    else if (l.type === 'depends-on') { (pre[t] ||= []).push([s, l]); (preOf[s] ||= []).push([t, l]); } });
  return { up, down, pre, preOf };
}

function tree(id, map, depth, seen, out) {
  for (const [nid, l] of (map[id] || [])) {
    hl.nodes.add(nid); hl.links.add(l.k);
    const n = byId(nid);
    const label = l.type === 'depends-on' ? '' : ' — ' + l.type;
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
  const role = !m.up[node.id] && !m.down[node.id] ? '（系譜のリンクなし）' : !m.up[node.id] ? '（起点）' : !m.down[node.id] ? '（末端）' : '';
  document.getElementById('detailHead').innerHTML =
    `<div style="color:#38bdf8;font-size:12px">${esc(node.id)} · ${esc(node.scope)} · ${esc(node.file)}</div>
     <div style="font-weight:600;margin:4px 0 0" class="md">${DOMPurify.sanitize(marked.parseInline(node.title))}</div>`;
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
  refresh();
  const d = 90, r = 1 + d / Math.hypot(node.x || 1, node.y || 1, node.z || 1);
  Graph.cameraPosition({ x:node.x * r, y:node.y * r, z:node.z * r }, node, 900);
}
function clearSel() { sel = null; hl = { nodes:new Set(), links:new Set() };
  document.getElementById('detail').style.display = 'none'; refresh(); }
function refresh() { Graph.nodeColor(Graph.nodeColor()).linkColor(Graph.linkColor()); }

const ID_RE = /GDR-[A-Z]+-\d{3}/g;
// 日本語の約物（「」（）など）に隣接する **太字** を CommonMark が閉じない問題の補正
marked.use({ tokenizer: { emStrong(src) {
  const m = /^\*\*(?=\S)([^*\n]*?\S)\*\*/.exec(src);
  return m ? { type:'strong', raw:m[0], text:m[1], tokens:this.lexer.inlineTokens(m[1]) } : false;
} } });
function renderMd(el, src) {
  el.innerHTML = DOMPurify.sanitize(marked.parse(src, { gfm:true }));
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
  // 対象の GDR 見出し（**GDR-…: …** の段落）を探して強調・スクロール
  const p = [...body.querySelectorAll('p')].find(p => p.firstElementChild?.tagName === 'STRONG' && p.textContent.trim().startsWith(id + ':'));
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
document.addEventListener('click', e => { const id = e.target.dataset?.id; if (!id) return;
  const n = Graph.graphData().nodes.find(n => n.id === id) || cur.nodes.find(n => n.id === id);
  if (!n) return; closeReader(); focusNode(n); });
document.getElementById('close').onclick = clearSel;
['showDep','showRel','hideIso'].forEach(id => document.getElementById(id).onchange = render);
const dsSel = document.getElementById('ds');
dsSel.innerHTML = DATASETS.map((d, i) => `<option value="${i}">${esc(d.name)}</option>`).join('');
dsSel.onchange = () => loadDataset(+dsSel.value);
window.addEventListener('resize', () => Graph.width(innerWidth).height(innerHeight));
// URL の # で開く GDR を指定できる（# の後は データセットの番号（0 から）/ GDR ID / doc。例: #1/GDR-META-040、#0/GDR-ARCH-012/doc）
const [hDs, hId, hDoc] = decodeURIComponent(location.hash.slice(1)).split('/');
const hIdx = /^\d+$/.test(hDs || '') && +hDs < DATASETS.length ? +hDs : 0;
dsSel.value = hIdx; loadDataset(hIdx);
if (hId) setTimeout(() => { const n = cur.nodes.find(n => n.id === hId); if (!n) return;
  focusNode(n); if (hDoc === 'doc' && n.file) openReader(n.file, n.id); }, 2500);
</script>
</body>
</html>
'''


if __name__ == "__main__":
    main()
