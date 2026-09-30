"""Ensure published documentation is reader-facing rather than internal notes."""

import importlib.util
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("release_builder", ROOT / "tools/build_release.py")
builder = importlib.util.module_from_spec(spec)
sys.path.insert(0, str(ROOT / "tools"))
try:
    spec.loader.exec_module(builder)
finally:
    sys.path.pop(0)


def test_publication_rejects_internal_markdown():
    builder.check_public_docs(sorted(builder.PUBLIC_DOCS))
    for name in ("AGENTS.md", "PUBLICATION_AUDIT.md", "docs/feedback.md", "TODO.md"):
        with pytest.raises(ValueError, match="Unexpected Markdown"):
            builder.check_public_docs(["README.md", name])


def test_public_docs_contain_no_conversation_or_todo_notes():
    assert {path.name for path in ROOT.glob("*.md")} == builder.PUBLIC_DOCS
    pattern = re.compile(r"\b(?:TODO|FIXME)\b|please\s+(?:move|change|update)|next\s+agent", re.IGNORECASE)
    for name in builder.PUBLIC_DOCS:
        assert not pattern.search((ROOT / name).read_text(encoding="utf-8")), name
