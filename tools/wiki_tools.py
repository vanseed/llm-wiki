#!/usr/bin/env python3
"""Utility CLI for the local Obsidian LLM Wiki.

The tool intentionally treats raw/ as immutable: it only lists raw paths and
never reads or writes raw file contents.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import math
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable


WIKILINK_RE = re.compile(r"\[\[([^\]\n]+)\]\]")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
TOKEN_RE = re.compile(r"[0-9a-zA-Z\u4e00-\u9fff]+")
VALID_MANIFEST_STATUSES = {"pending", "ingested", "path_mismatch", "conflict_paused"}
VALID_TRANSLATION_STATUSES = {"pending", "translated", "needs_review", "skipped"}
WIKI_TYPES = {"concept", "entity", "source", "synthesis"}
EXCLUDED_WIKI_NAMES = {"index.md", "log.md"}


@dataclass(frozen=True)
class WikiPage:
    name: str
    path: Path
    rel_path: str
    page_type: str
    links: tuple[str, ...]
    sources: tuple[str, ...]


@dataclass(frozen=True)
class ManifestRow:
    raw_path: str
    status: str
    source_page: str
    output_pages: tuple[str, ...]
    last_ingested: str
    notes: str


@dataclass(frozen=True)
class TranslationManifestRow:
    raw_path: str
    translated_path: str
    status: str
    translated_at: str
    notes: str


@dataclass(frozen=True)
class SearchResult:
    page: WikiPage
    score: float
    snippet: str


@dataclass
class WikiSnapshot:
    root: Path
    wiki_dir: Path
    raw_dir: Path
    translated_dir: Path
    content_pages: list[WikiPage]
    all_non_meta_pages: list[WikiPage]
    existing_page_names: set[str]
    raw_paths: list[str]
    translated_paths: list[str]
    manifest_rows: list[ManifestRow]
    translation_rows: list[TranslationManifestRow]
    index_links: list[str]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def to_posix(path: Path) -> str:
    return path.as_posix()


def rel_to_root(root: Path, path: Path) -> str:
    return to_posix(path.relative_to(root))


def clean_wikilink(raw: str) -> str:
    target = raw.split("|", 1)[0].split("#", 1)[0].strip()
    return target


def extract_wikilinks(text: str) -> list[str]:
    links = [clean_wikilink(match.group(1)) for match in WIKILINK_RE.finditer(text)]
    return [link for link in links if link]


def strip_wikilinks(text: str) -> str:
    return WIKILINK_RE.sub(lambda match: clean_wikilink(match.group(1)), text)


def strip_frontmatter(text: str) -> str:
    return FRONTMATTER_RE.sub("", text, count=1)


def tokenize(text: str) -> list[str]:
    normalized = strip_wikilinks(text).replace("_", " ").replace("-", " ").lower()
    return TOKEN_RE.findall(normalized)


def parse_simple_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}

    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def parse_inline_list(value: str) -> tuple[str, ...]:
    value = value.strip()
    if not value.startswith("[") or not value.endswith("]"):
        return ()
    inner = value[1:-1].strip()
    if not inner:
        return ()
    if inner.startswith(("raw/", "assets/")) and re.search(r"\.(md|pdf|txt|html?)\s*$", inner, re.IGNORECASE):
        return (inner,)
    return tuple(item.strip().strip('"').strip("'") for item in next(csv.reader([inner], skipinitialspace=True)) if item.strip())


def parse_page(root: Path, path: Path) -> WikiPage:
    text = read_text(path)
    frontmatter = parse_simple_frontmatter(text)
    rel_path = rel_to_root(root, path)
    page_type = frontmatter.get("type", infer_type_from_path(path))
    sources = parse_inline_list(frontmatter.get("sources", "[]"))
    return WikiPage(
        name=path.stem,
        path=path,
        rel_path=rel_path,
        page_type=page_type,
        links=tuple(sorted(set(extract_wikilinks(text)))),
        sources=sources,
    )


def infer_type_from_path(path: Path) -> str:
    parent = path.parent.name
    if parent == "concepts":
        return "concept"
    if parent == "entities":
        return "entity"
    if parent == "sources":
        return "source"
    if parent == "syntheses":
        return "synthesis"
    return "unknown"


def iter_markdown_files(directory: Path) -> Iterable[Path]:
    if not directory.exists():
        return []
    return sorted(directory.rglob("*.md"))


def list_raw_paths(root: Path, raw_dir: Path) -> list[str]:
    if not raw_dir.exists():
        return []
    return sorted(rel_to_root(root, path) for path in raw_dir.rglob("*") if path.is_file() and path.name != ".gitkeep")


def list_translated_paths(root: Path, translated_dir: Path) -> list[str]:
    if not translated_dir.exists():
        return []
    return sorted(
        rel_to_root(root, path) for path in translated_dir.rglob("*") if path.is_file() and path.name != ".gitkeep"
    )


def parse_manifest_table(manifest_path: Path) -> list[ManifestRow]:
    if not manifest_path.exists():
        return []

    rows: list[ManifestRow] = []
    for line in read_text(manifest_path).splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) != 6:
            continue
        if cells[0] in {"raw_path", "---"} or set(cells[0]) == {"-"}:
            continue
        raw_path, status, source_page, output_pages, last_ingested, notes = cells
        rows.append(
            ManifestRow(
                raw_path=raw_path,
                status=status,
                source_page=clean_wikilink(strip_wikilinks(source_page)),
                output_pages=tuple(extract_wikilinks(output_pages)),
                last_ingested=last_ingested,
                notes=notes,
            )
        )
    return rows


def parse_translation_manifest_table(manifest_path: Path) -> list[TranslationManifestRow]:
    if not manifest_path.exists():
        return []

    rows: list[TranslationManifestRow] = []
    for line in read_text(manifest_path).splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) != 5:
            continue
        if cells[0] in {"raw_path", "---"} or set(cells[0]) == {"-"}:
            continue
        raw_path, translated_path, status, translated_at, notes = cells
        rows.append(
            TranslationManifestRow(
                raw_path=raw_path,
                translated_path=translated_path,
                status=status,
                translated_at=translated_at,
                notes=notes,
            )
        )
    return rows


def load_snapshot(root: Path) -> WikiSnapshot:
    wiki_dir = root / "wiki"
    raw_dir = root / "raw"
    translated_dir = root / "translated"
    all_non_meta_paths = [
        path
        for path in iter_markdown_files(wiki_dir)
        if "_meta" not in path.relative_to(wiki_dir).parts
    ]
    all_non_meta_pages = [parse_page(root, path) for path in all_non_meta_paths]
    content_pages = [page for page in all_non_meta_pages if page.path.name not in EXCLUDED_WIKI_NAMES]
    existing_page_names = {page.name for page in all_non_meta_pages}
    raw_paths = list_raw_paths(root, raw_dir)
    translated_paths = list_translated_paths(root, translated_dir)
    manifest_rows = parse_manifest_table(wiki_dir / "_meta" / "manifest.md")
    translation_rows = parse_translation_manifest_table(wiki_dir / "_meta" / "translation-manifest.md")
    index_path = wiki_dir / "index.md"
    index_links = extract_wikilinks(read_text(index_path)) if index_path.exists() else []
    return WikiSnapshot(
        root=root,
        wiki_dir=wiki_dir,
        raw_dir=raw_dir,
        translated_dir=translated_dir,
        content_pages=content_pages,
        all_non_meta_pages=all_non_meta_pages,
        existing_page_names=existing_page_names,
        raw_paths=raw_paths,
        translated_paths=translated_paths,
        manifest_rows=manifest_rows,
        translation_rows=translation_rows,
        index_links=sorted(set(index_links)),
    )


def registered_missing(snapshot: WikiSnapshot) -> list[str]:
    return sorted(link for link in snapshot.index_links if link not in snapshot.existing_page_names)


def content_deadlinks(snapshot: WikiSnapshot) -> list[tuple[str, str]]:
    deadlinks: list[tuple[str, str]] = []
    for page in snapshot.content_pages:
        for link in page.links:
            if link not in snapshot.existing_page_names:
                deadlinks.append((page.rel_path, link))
    return sorted(set(deadlinks))


def orphan_pages(snapshot: WikiSnapshot) -> list[str]:
    incoming: Counter[str] = Counter()
    for page in snapshot.content_pages:
        for link in page.links:
            incoming[link] += 1
    return sorted(page.name for page in snapshot.content_pages if incoming[page.name] == 0)


def manifest_status_counts(snapshot: WikiSnapshot) -> Counter[str]:
    return Counter(row.status for row in snapshot.manifest_rows)


def translation_status_counts(snapshot: WikiSnapshot) -> Counter[str]:
    return Counter(row.status for row in snapshot.translation_rows)


def manifest_issues(snapshot: WikiSnapshot) -> list[str]:
    issues: list[str] = []
    raw_set = set(snapshot.raw_paths)
    manifest_raw = {row.raw_path for row in snapshot.manifest_rows}
    page_by_name = {page.name: page for page in snapshot.all_non_meta_pages}

    for raw_path in sorted(raw_set - manifest_raw):
        issues.append(f"raw 文件未登记 manifest：`{raw_path}`")
    for raw_path in sorted(manifest_raw - raw_set):
        issues.append(f"manifest raw_path 不存在：`{raw_path}`")

    for row in snapshot.manifest_rows:
        if row.status not in VALID_MANIFEST_STATUSES:
            issues.append(f"manifest 状态未知：`{row.raw_path}` -> `{row.status}`")
        if row.status == "ingested" and not row.source_page:
            issues.append(f"ingested 条目缺少 source_page：`{row.raw_path}`")
        if row.source_page and row.source_page not in snapshot.existing_page_names:
            issues.append(f"manifest source 页面不存在：`{row.raw_path}` -> [[{row.source_page}]]")
            continue
        if row.source_page in page_by_name:
            source_page = page_by_name[row.source_page]
            if source_page.sources and row.raw_path not in source_page.sources:
                issues.append(
                    "source frontmatter 与 manifest raw_path 不一致："
                    f"[[{row.source_page}]] sources={list(source_page.sources)} manifest=`{row.raw_path}`"
                )
    return issues


def render_manifest_table(snapshot: WikiSnapshot) -> str:
    rows_by_raw = {row.raw_path: row for row in snapshot.manifest_rows}
    ordered_raw_paths = [row.raw_path for row in snapshot.manifest_rows]
    for raw_path in snapshot.raw_paths:
        if raw_path not in rows_by_raw:
            ordered_raw_paths.append(raw_path)

    lines = [
        "| raw_path | status | source_page | output_pages | last_ingested | notes |",
        "|---|---|---|---|---|---|",
    ]
    for raw_path in ordered_raw_paths:
        row = rows_by_raw.get(raw_path)
        if row is None:
            values = [raw_path, "pending", "", "", "", "自动发现，尚未形成 source 页面"]
        else:
            source_page = f"[[{row.source_page}]]" if row.source_page else ""
            output_pages = ", ".join(f"[[{page}]]" for page in row.output_pages)
            values = [row.raw_path, row.status, source_page, output_pages, row.last_ingested, row.notes]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def type_counts(snapshot: WikiSnapshot) -> Counter[str]:
    return Counter(page.page_type for page in snapshot.content_pages)


def page_search_text(page: WikiPage) -> str:
    text = strip_frontmatter(read_text(page.path))
    return f"{page.name}\n{page.page_type}\n{text}"


def make_snippet(text: str, query_terms: set[str], max_len: int = 120) -> str:
    body = strip_wikilinks(strip_frontmatter(text))
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        lowered = stripped.replace("_", " ").replace("-", " ").lower()
        if any(term in lowered for term in query_terms):
            return stripped[:max_len]
    compact = " ".join(body.split())
    return compact[:max_len]


def search_pages(snapshot: WikiSnapshot, query: str, limit: int = 10) -> list[SearchResult]:
    query_terms = set(tokenize(query))
    if not query_terms:
        return []

    page_tokens: dict[str, list[str]] = {}
    document_frequency: Counter[str] = Counter()
    for page in snapshot.content_pages:
        tokens = tokenize(page_search_text(page))
        page_tokens[page.name] = tokens
        for token in set(tokens):
            document_frequency[token] += 1

    page_count = max(len(snapshot.content_pages), 1)
    results: list[SearchResult] = []
    for page in snapshot.content_pages:
        tokens = page_tokens[page.name]
        token_counts = Counter(tokens)
        score = 0.0
        for term in query_terms:
            tf = token_counts.get(term, 0)
            if tf == 0:
                continue
            idf = math.log((page_count + 1) / (document_frequency[term] + 1)) + 1
            score += tf * idf
            if term in tokenize(page.name):
                score += 2.0 * idf
        if score <= 0:
            continue
        raw_text = read_text(page.path)
        results.append(SearchResult(page=page, score=round(score, 4), snippet=make_snippet(raw_text, query_terms)))

    return sorted(results, key=lambda item: (-item.score, item.page.name))[:limit]


def build_graph(snapshot: WikiSnapshot) -> dict[str, object]:
    nodes = [
        {
            "id": page.name,
            "path": page.rel_path,
            "type": page.page_type,
            "exists": True,
        }
        for page in sorted(snapshot.content_pages, key=lambda item: item.name)
    ]
    missing_targets = sorted({target for _, target in content_deadlinks(snapshot)})
    nodes.extend({"id": target, "path": None, "type": "missing", "exists": False} for target in missing_targets)

    edges = []
    for page in snapshot.content_pages:
        for target in page.links:
            edges.append(
                {
                    "source": page.name,
                    "target": target,
                    "target_exists": target in snapshot.existing_page_names,
                }
            )
    return {
        "generated_at": date.today().isoformat(),
        "nodes": nodes,
        "edges": sorted(edges, key=lambda item: (item["source"], item["target"])),
    }


def xml_escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def render_graphml(graph: dict[str, object]) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">',
        '  <key id="path" for="node" attr.name="path" attr.type="string" />',
        '  <key id="type" for="node" attr.name="type" attr.type="string" />',
        '  <key id="exists" for="node" attr.name="exists" attr.type="boolean" />',
        '  <key id="target_exists" for="edge" attr.name="target_exists" attr.type="boolean" />',
        '  <graph id="G" edgedefault="directed">',
    ]
    for node in graph["nodes"]:
        lines.append(f'    <node id="{xml_escape(node["id"])}">')
        if node.get("path"):
            lines.append(f'      <data key="path">{xml_escape(node["path"])}</data>')
        lines.append(f'      <data key="type">{xml_escape(node["type"])}</data>')
        lines.append(f'      <data key="exists">{str(node["exists"]).lower()}</data>')
        lines.append("    </node>")
    for edge in graph["edges"]:
        lines.append(f'    <edge source="{xml_escape(edge["source"])}" target="{xml_escape(edge["target"])}">')
        lines.append(f'      <data key="target_exists">{str(edge["target_exists"]).lower()}</data>')
        lines.append("    </edge>")
    lines.extend(["  </graph>", "</graphml>"])
    return "\n".join(lines) + "\n"


def render_health(snapshot: WikiSnapshot) -> str:
    missing = registered_missing(snapshot)
    deadlinks = content_deadlinks(snapshot)
    deadlink_targets = sorted({target for _, target in deadlinks})
    manifest_counts = manifest_status_counts(snapshot)
    issues = manifest_issues(snapshot)

    def status_count(status: str) -> int:
        return manifest_counts.get(status, 0)

    lines = [
        "# Wiki Health",
        "",
        f"最近检查日期：{date.today().isoformat()}",
        "",
        "## 摘要",
        "",
        f"- wiki 内容页：{len(snapshot.content_pages)} 个（不含 `wiki/index.md`、`wiki/log.md` 和 `wiki/_meta/`）",
        f"- raw 文件：{len(snapshot.raw_paths)} 个",
        f"- translated 译文文件：{len(snapshot.translated_paths)} 个",
        (
            "- manifest 状态："
            f"`ingested` {status_count('ingested')} 个，"
            f"`path_mismatch` {status_count('path_mismatch')} 个，"
            f"`pending` {status_count('pending')} 个，"
            f"`conflict_paused` {status_count('conflict_paused')} 个"
        ),
        "- translation 状态："
        + ", ".join(
            f"`{status}` {translation_status_counts(snapshot).get(status, 0)} 个"
            for status in ("translated", "needs_review", "pending", "skipped")
        ),
        f"- 已注册但未创建页面：{len(missing)} 个",
        f"- 知识页死链引用：{len(deadlinks)} 处（{len(deadlink_targets)} 个唯一目标；不含 `wiki/index.md`、`wiki/log.md` 和 `wiki/_meta/`）",
        f"- 孤儿页面：{len(orphan_pages(snapshot))} 个",
        f"- Manifest 不一致项：{len(issues)} 个",
        "",
        "## 已注册但未创建页面",
        "",
    ]
    lines.extend(f"- [[{name}]]" for name in missing)
    if not missing:
        lines.append("- 无")

    lines.extend(["", "## 知识页死链目标", ""])
    lines.extend(f"- [[{name}]]" for name in deadlink_targets)
    if not deadlink_targets:
        lines.append("- 无")

    lines.extend(["", "## Manifest 注意事项", ""])
    if issues:
        lines.extend(f"- {issue}" for issue in issues)
    else:
        lines.append("- 未发现 manifest/raw/source 不一致项。")
    for row in snapshot.manifest_rows:
        if row.status == "pending":
            lines.append(f"- `{row.raw_path}` 仍为 `pending`。")
        elif row.status == "path_mismatch":
            lines.append(f"- `{row.raw_path}` 当前为 `path_mismatch`，请人工确认后修正 source frontmatter 或保留记录。")

    lines.extend(
        [
            "",
            "## Lint 口径",
            "",
            "- 死链扫描默认排除 `wiki/log.md`。",
            "- `wiki/index.md` 中预注册但未创建的页面归类为“已注册但未创建”，不与普通知识页死链混在一起。",
            "- `wiki/_meta/templates/` 不作为正式知识页参与索引、死链、孤儿页面或知识冲突统计。",
            "- 修复动作必须经过用户确认。",
            "",
            "## 下一步建议",
            "",
        ]
    )
    suggestions = next_step_suggestions(snapshot, missing, deadlink_targets, issues)
    lines.extend(f"{idx}. {item}" for idx, item in enumerate(suggestions, start=1))
    return "\n".join(lines).rstrip() + "\n"


def next_step_suggestions(
    snapshot: WikiSnapshot,
    missing: list[str],
    deadlink_targets: list[str],
    manifest_issue_list: list[str],
) -> list[str]:
    suggestions: list[str] = []
    pending = [row.raw_path for row in snapshot.manifest_rows if row.status == "pending"]
    if pending:
        suggestions.append(f"优先摄取 `{pending[0]}`。")
    if missing:
        overlap = sorted(set(missing) & set(deadlink_targets))
        if overlap:
            suggestions.append(f"优先补齐同时出现在 index 和内容死链中的页面：{', '.join(overlap[:5])}。")
        else:
            suggestions.append(f"批量补齐 {len(missing)} 个已注册但未创建页面。")
    if manifest_issue_list:
        suggestions.append("复核 manifest/raw/source 不一致项，必要时更新 `wiki/_meta/manifest.md`。")
    if deadlink_targets:
        suggestions.append("复核 synthesis 页面中的示例型双链是否应改为普通文本或真实页面。")
    if not suggestions:
        suggestions.append("当前未发现结构性问题，继续翻译、增量摄取或查询即可。")
    return suggestions


def print_status(snapshot: WikiSnapshot) -> None:
    counts = manifest_status_counts(snapshot)
    translation_counts = translation_status_counts(snapshot)
    missing = registered_missing(snapshot)
    deadlinks = content_deadlinks(snapshot)
    issues = manifest_issues(snapshot)
    recent_log = read_recent_log(snapshot.wiki_dir / "log.md")
    print(f"Wiki Status — {date.today().isoformat()}")
    print()
    print(f"- wiki 内容页：{len(snapshot.content_pages)}")
    print(f"- raw 文件：{len(snapshot.raw_paths)}")
    print(f"- translated 译文文件：{len(snapshot.translated_paths)}")
    print(
        "- translation 状态："
        f"translated {translation_counts.get('translated', 0)} / "
        f"needs_review {translation_counts.get('needs_review', 0)} / "
        f"pending {translation_counts.get('pending', 0)} / "
        f"skipped {translation_counts.get('skipped', 0)}"
    )
    print(
        "- manifest 状态："
        f"ingested {counts.get('ingested', 0)} / "
        f"pending {counts.get('pending', 0)} / "
        f"path_mismatch {counts.get('path_mismatch', 0)} / "
        f"conflict_paused {counts.get('conflict_paused', 0)}"
    )
    print(f"- 已注册但未创建页面：{len(missing)}")
    print(f"- 知识页死链引用：{len(deadlinks)}")
    print(f"- manifest 不一致项：{len(issues)}")
    print(f"- 最近一次操作：{recent_log or '未找到'}")


def read_recent_log(log_path: Path) -> str:
    if not log_path.exists():
        return ""
    headings = [line.strip().lstrip("#").strip() for line in read_text(log_path).splitlines() if line.startswith("## ")]
    return headings[-1] if headings else ""


def cmd_status(args: argparse.Namespace) -> int:
    snapshot = load_snapshot(args.root)
    print_status(snapshot)
    return 0


def cmd_lint(args: argparse.Namespace) -> int:
    snapshot = load_snapshot(args.root)
    report = render_health(snapshot)
    if args.write:
        target = snapshot.wiki_dir / "_meta" / "health.md"
        write_text(target, report)
        print(f"wrote {rel_to_root(snapshot.root, target)}")
    else:
        print(report, end="")
    return 0


def cmd_manifest(args: argparse.Namespace) -> int:
    snapshot = load_snapshot(args.root)
    issues = manifest_issues(snapshot)
    data = {
        "raw_count": len(snapshot.raw_paths),
        "manifest_count": len(snapshot.manifest_rows),
        "status_counts": dict(sorted(manifest_status_counts(snapshot).items())),
        "issues": issues,
    }
    if args.format == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_manifest_table(snapshot))
    else:
        print(f"raw 文件：{data['raw_count']}")
        print(f"manifest 条目：{data['manifest_count']}")
        print("manifest 状态：" + ", ".join(f"{key} {value}" for key, value in data["status_counts"].items()))
        if issues:
            print("问题：")
            for issue in issues:
                print(f"- {issue}")
        else:
            print("问题：无")
    return 1 if issues and args.strict else 0


def cmd_graph(args: argparse.Namespace) -> int:
    snapshot = load_snapshot(args.root)
    graph = build_graph(snapshot)
    if args.format == "graphml":
        text = render_graphml(graph)
    else:
        text = json.dumps(graph, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output = args.output
        if not output.is_absolute():
            output = args.root / output
        write_text(output, text)
        print(f"wrote {rel_to_root(snapshot.root, output)}")
    else:
        print(text, end="")
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    snapshot = load_snapshot(args.root)
    results = search_pages(snapshot, args.query, args.limit)
    if args.format == "json":
        payload = [
            {
                "page": result.page.name,
                "type": result.page.page_type,
                "path": result.page.rel_path,
                "score": result.score,
                "snippet": result.snippet,
            }
            for result in results
        ]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if not results:
        print("No results.")
        return 0

    for idx, result in enumerate(results, start=1):
        print(f"{idx}. [[{result.page.name}]] ({result.page.page_type}) score={result.score}")
        print(f"   path: {result.page.rel_path}")
        if result.snippet:
            print(f"   {result.snippet}")
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    snapshot = load_snapshot(args.root)
    stats = {
        "content_pages": len(snapshot.content_pages),
        "raw_files": len(snapshot.raw_paths),
        "translated_files": len(snapshot.translated_paths),
        "translation_statuses": dict(sorted(translation_status_counts(snapshot).items())),
        "registered_missing": len(registered_missing(snapshot)),
        "content_deadlinks": len(content_deadlinks(snapshot)),
        "orphan_pages": len(orphan_pages(snapshot)),
        "manifest_issues": len(manifest_issues(snapshot)),
        "types": dict(sorted(type_counts(snapshot).items())),
    }
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local tools for the Obsidian LLM Wiki")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Vault root, defaults to current working directory.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    status = subparsers.add_parser("status", help="Print a concise wiki status.")
    status.set_defaults(func=cmd_status)

    lint = subparsers.add_parser("lint", help="Render or update wiki/_meta/health.md.")
    lint.add_argument("--write", action="store_true", help="Write the report to wiki/_meta/health.md.")
    lint.set_defaults(func=cmd_lint)

    manifest = subparsers.add_parser("manifest", help="Check raw/manifest/source consistency.")
    manifest.add_argument("--format", choices=("text", "json", "markdown"), default="text")
    manifest.add_argument("--strict", action="store_true", help="Exit 1 when manifest issues are found.")
    manifest.set_defaults(func=cmd_manifest)

    graph = subparsers.add_parser("graph", help="Export the wiki link graph as JSON or GraphML.")
    graph.add_argument("--format", choices=("json", "graphml"), default="json")
    graph.add_argument("--output", type=Path, help="Output path, for example wiki/_meta/graph.json.")
    graph.set_defaults(func=cmd_graph)

    search = subparsers.add_parser("search", help="Search wiki knowledge pages without reading raw/ contents.")
    search.add_argument("query", help="Search query.")
    search.add_argument("--limit", type=int, default=10)
    search.add_argument("--format", choices=("text", "json"), default="text")
    search.set_defaults(func=cmd_search)

    stats = subparsers.add_parser("stats", help="Print machine-readable wiki statistics.")
    stats.set_defaults(func=cmd_stats)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.root = args.root.resolve()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
