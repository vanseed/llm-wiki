from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import wiki_tools


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


class WikiToolsTest(unittest.TestCase):
    def make_vault(self) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        root = Path(temp_dir.name)

        write(root / "raw" / "01-articles" / "secret.md", "rawonlyterm should not be searchable")
        write(
            root / "wiki" / "index.md",
            "# Wiki Index\n\n- [[Prompt_Engineering]] — Prompt topic\n- [[Other_Page]] — Related topic\n",
        )
        write(root / "wiki" / "log.md", "## [2026-06-23] sync | test vault\n")
        write(
            root / "wiki" / "_meta" / "manifest.md",
            "# Source Manifest\n\n"
            "| raw_path | status | source_page | output_pages | last_ingested | notes |\n"
            "|---|---|---|---|---|---|\n"
            "| raw/01-articles/secret.md | pending |  |  |  | test |\n",
        )
        write(
            root / "wiki" / "concepts" / "Prompt_Engineering.md",
            "---\n"
            "title: Prompt Engineering\n"
            "type: concept\n"
            "sources: []\n"
            "---\n\n"
            "# Prompt Engineering\n\n"
            "Prompt engineering improves prompts. Prompt design matters.\n\n"
            "## 关联连接\n"
            "- [[Other_Page]] — related\n",
        )
        write(
            root / "wiki" / "concepts" / "Other_Page.md",
            "---\n"
            "title: Other Page\n"
            "type: concept\n"
            "sources: []\n"
            "---\n\n"
            "# Other Page\n\n"
            "Prompt notes.\n\n"
            "## 关联连接\n"
            "- [[Prompt_Engineering]] — related\n",
        )
        return root

    def test_parse_inline_list_keeps_unquoted_raw_path_with_commas(self) -> None:
        parsed = wiki_tools.parse_inline_list(
            "[raw/01-articles/Prompt Engineering in 2025_ Complete Guide for ChatGPT, Claude, and Gemini.md]"
        )

        self.assertEqual(
            parsed,
            ("raw/01-articles/Prompt Engineering in 2025_ Complete Guide for ChatGPT, Claude, and Gemini.md",),
        )

    def test_list_raw_paths_ignores_gitkeep_placeholders(self) -> None:
        root = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(root))
        write(root / "raw" / "01-articles" / ".gitkeep", "")
        write(root / "raw" / "04-notes" / ".gitkeep", "")

        self.assertEqual(wiki_tools.list_raw_paths(root, root / "raw"), [])

    def test_list_translated_paths_ignores_gitkeep_placeholders(self) -> None:
        root = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(root))
        write(root / "translated" / "01-articles" / ".gitkeep", "")
        write(root / "translated" / "01-articles" / "example.zh.md", "# 示例")

        self.assertEqual(
            wiki_tools.list_translated_paths(root, root / "translated"),
            ["translated/01-articles/example.zh.md"],
        )

    def test_search_pages_ranks_wiki_matches_and_ignores_raw_content(self) -> None:
        snapshot = wiki_tools.load_snapshot(self.make_vault())

        results = wiki_tools.search_pages(snapshot, "prompt engineering")

        self.assertGreaterEqual(len(results), 2)
        self.assertEqual(results[0].page.name, "Prompt_Engineering")
        self.assertGreater(results[0].score, results[1].score)
        self.assertEqual(wiki_tools.search_pages(snapshot, "rawonlyterm"), [])

    def test_search_pages_ignores_translated_content(self) -> None:
        root = self.make_vault()
        write(root / "translated" / "01-articles" / "example.zh.md", "translatedonlyterm")
        snapshot = wiki_tools.load_snapshot(root)

        self.assertEqual(wiki_tools.search_pages(snapshot, "translatedonlyterm"), [])

    def test_parse_translation_manifest_table(self) -> None:
        root = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(root))
        manifest = root / "wiki" / "_meta" / "translation-manifest.md"
        write(
            manifest,
            "# Translation Manifest\n\n"
            "| raw_path | translated_path | status | translated_at | notes |\n"
            "|---|---|---|---|---|\n"
            "| raw/01-articles/example.md | translated/01-articles/example.zh.md | translated | 2026-06-24 | ok |\n",
        )

        rows = wiki_tools.parse_translation_manifest_table(manifest)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].raw_path, "raw/01-articles/example.md")
        self.assertEqual(rows[0].translated_path, "translated/01-articles/example.zh.md")
        self.assertEqual(rows[0].status, "translated")

    def test_cli_stats_includes_translation_statuses(self) -> None:
        root = self.make_vault()
        write(root / "translated" / "01-articles" / "example.zh.md", "# 示例")
        write(
            root / "wiki" / "_meta" / "translation-manifest.md",
            "# Translation Manifest\n\n"
            "| raw_path | translated_path | status | translated_at | notes |\n"
            "|---|---|---|---|---|\n"
            "| raw/01-articles/secret.md | translated/01-articles/example.zh.md | translated | 2026-06-24 | ok |\n",
        )

        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = wiki_tools.main(["--root", str(root), "stats"])

        payload = json.loads(stdout.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["translated_files"], 1)
        self.assertEqual(payload["translation_statuses"], {"translated": 1})

    def test_render_graphml_contains_nodes_and_edges(self) -> None:
        snapshot = wiki_tools.load_snapshot(self.make_vault())

        graphml = wiki_tools.render_graphml(wiki_tools.build_graph(snapshot))

        self.assertIn('<graphml xmlns="http://graphml.graphdrawing.org/xmlns"', graphml)
        self.assertIn('<node id="Prompt_Engineering">', graphml)
        self.assertIn('<edge source="Prompt_Engineering" target="Other_Page">', graphml)

    def test_cli_graph_writes_graphml(self) -> None:
        root = self.make_vault()
        output = root / "wiki" / "_meta" / "graph.graphml"

        with redirect_stdout(io.StringIO()):
            exit_code = wiki_tools.main(
                ["--root", str(root), "graph", "--format", "graphml", "--output", "wiki/_meta/graph.graphml"]
            )

        self.assertEqual(exit_code, 0)
        self.assertIn("<graphml", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
