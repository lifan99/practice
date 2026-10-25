"""Ensure every core module imports with only the Python standard library."""

import subprocess
import sys
from pathlib import Path


def test_core_imports_without_site_packages():
    root = Path(__file__).resolve().parents[1]
    script = """
import importlib
import pkgutil
import sys
sys.path.insert(0, sys.argv[1])
import rag_practice.core as core
for info in pkgutil.iter_modules(core.__path__):
    importlib.import_module(core.__name__ + '.' + info.name)
from rag_practice.core.types import Document, Chunk, SearchHit
assert SearchHit(Chunk('a', 'x', 'a.md', 0, 1), 1).chunk.text == 'x'
assert Document('x', 'a.md').source == 'a.md'
assert not any(name.startswith(('langchain', 'langgraph', 'numpy')) for name in sys.modules)
"""
    result = subprocess.run([sys.executable, "-I", "-S", "-c", script, str(root)], capture_output=True, text=True, timeout=10)
    assert result.returncode == 0, result.stderr
