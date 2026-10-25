"""Level 8: check file boundaries independently of protocol transports."""

from pathlib import Path

import pytest

from mcp_practice import level08_files as files

pytestmark = pytest.mark.exercise


def test_resolver_and_reader_preserve_markdown_text(tmp_path):
    root = tmp_path / "notes"
    (root / "nested").mkdir(parents=True)
    target = root / "nested" / "a.md"
    target.write_text("  中文\n\n", encoding="utf-8")
    assert files.resolve_note_path(root, "./nested/a.md") == target.resolve()
    assert files.read_note(root, "nested/a.md") == "  中文\n\n"


@pytest.mark.parametrize("path", ["", " \n", "../outside.md", "/outside.md", "C:/outside.md", "nested\\a.md", "bad\x00.md", "a.txt"])
def test_invalid_relative_paths(tmp_path, path):
    with pytest.raises(ValueError):
        files.resolve_note_path(tmp_path, path)


def test_missing_file_and_directory_target(tmp_path):
    with pytest.raises(FileNotFoundError):
        files.resolve_note_path(tmp_path, "missing.md")
    (tmp_path / "folder.md").mkdir()
    with pytest.raises(IsADirectoryError):
        files.resolve_note_path(tmp_path, "folder.md")


def test_symlink_must_resolve_inside_root(tmp_path):
    root = tmp_path / "notes"
    root.mkdir()
    outside = tmp_path / "outside.md"
    outside.write_text("outside", encoding="utf-8")
    inside = root / "inside.md"
    inside.write_text("inside", encoding="utf-8")
    try:
        (root / "escape.md").symlink_to(outside)
        (root / "alias.md").symlink_to(inside)
    except OSError:
        pytest.skip("Creating symlinks is not available on this platform.")
    with pytest.raises(PermissionError):
        files.resolve_note_path(root, "escape.md")
    assert files.resolve_note_path(root, "alias.md") == inside.resolve()


def test_reader_reuses_path_boundary(monkeypatch, tmp_path):
    target = tmp_path / "safe.md"
    target.write_text("safe\n", encoding="utf-8")
    calls = []

    def resolve(root, path):
        calls.append((root, path))
        return target

    monkeypatch.setattr(files, "resolve_note_path", resolve)
    assert files.read_note(Path("given-root"), "given.md") == "safe\n"
    assert calls == [(Path("given-root"), "given.md")]
