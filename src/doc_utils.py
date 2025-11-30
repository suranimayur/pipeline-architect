# doc_utils.py
"""
Utilities to load reference architecture documents so the LLM
can use them as extra context when generating designs.
"""

from typing import List
import os


def load_reference_text(folder: str = "reference_docs") -> str:
    """
    Read all .txt and .md files from the given folder and return
    a single big string with their contents.

    Each file is prefixed with a header so the LLM knows which file it came from.
    """
    if not os.path.exists(folder):
        return ""

    chunks: List[str] = []
    for name in os.listdir(folder):
        path = os.path.join(folder, name)
        if not os.path.isfile(path):
            continue

        lower = name.lower()
        if lower.endswith(".txt") or lower.endswith(".md"):
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read().strip()
                    if content:
                        chunks.append(f"# From file: {name}\n{content}")
            except Exception as e:
                # If something goes wrong with a file, skip it
                print(f"Could not read {path}: {e}")

    return "\n\n".join(chunks)
