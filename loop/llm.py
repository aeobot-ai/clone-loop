"""LLM calls go through headless Claude Code, like blogs-gen's planner."""

from __future__ import annotations

import subprocess

TIMEOUT_S = 900


def ask(prompt: str) -> str:
    p = subprocess.run(["claude", "-p"], input=prompt, capture_output=True, text=True, timeout=TIMEOUT_S)
    if p.returncode != 0 or not p.stdout.strip():
        raise RuntimeError(f"claude -p exited {p.returncode}: {p.stderr[-300:]}")
    return p.stdout.strip()
