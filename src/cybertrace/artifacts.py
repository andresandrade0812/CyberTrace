"""Artifact inventory helpers.

This module intentionally avoids executing or inspecting live malware. It is for cataloging
safe files, logs, captures, and metadata before feature extraction.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ArtifactRecord:
    """Basic metadata for an artifact stored in the project data directory."""

    sample_id: str
    path: Path
    artifact_type: str
    label: str | None = None
    notes: str | None = None


def list_artifacts(directory: Path) -> list[ArtifactRecord]:
    """Create simple artifact records for files in a directory."""

    records: list[ArtifactRecord] = []
    for path in sorted(item for item in directory.rglob("*") if item.is_file()):
        if path.name == ".gitkeep":
            continue
        records.append(
            ArtifactRecord(
                sample_id=path.stem,
                path=path,
                artifact_type=path.suffix.lstrip(".") or "unknown",
            )
        )
    return records
