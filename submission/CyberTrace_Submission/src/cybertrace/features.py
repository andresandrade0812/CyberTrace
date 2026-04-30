"""Utilities for preparing feature tables for analysis."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from cybertrace.config import DEFAULT_ID_COLUMN, NON_FEATURE_COLUMNS


@dataclass(frozen=True)
class FeatureTable:
    """A feature matrix and the metadata kept beside it."""

    features: pd.DataFrame
    metadata: pd.DataFrame


def load_feature_table(path: Path, id_column: str = DEFAULT_ID_COLUMN) -> FeatureTable:
    """Load a CSV and split numeric model features from descriptive metadata."""

    frame = pd.read_csv(path)
    if id_column not in frame.columns:
        msg = f"Feature file must include an '{id_column}' column."
        raise ValueError(msg)

    metadata_columns = [column for column in frame.columns if column in NON_FEATURE_COLUMNS]
    numeric_features = frame.drop(columns=metadata_columns, errors="ignore").select_dtypes(
        include="number"
    )

    if numeric_features.empty:
        msg = "Feature file must include at least one numeric feature column."
        raise ValueError(msg)

    return FeatureTable(features=numeric_features, metadata=frame[metadata_columns].copy())


def save_feature_table(frame: pd.DataFrame, path: Path) -> None:
    """Save a feature table, creating the parent directory when needed."""

    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
