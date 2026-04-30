"""Clustering helpers for cybersecurity feature analysis."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


@dataclass(frozen=True)
class ClusterResult:
    """Cluster assignments and fitted model pipeline."""

    assignments: pd.DataFrame
    model: Pipeline


def cluster_features(
    features: pd.DataFrame,
    metadata: pd.DataFrame,
    cluster_count: int,
    random_state: int = 42,
) -> ClusterResult:
    """Cluster numeric features and return assignments joined to metadata."""

    if cluster_count < 2:
        msg = "cluster_count must be at least 2."
        raise ValueError(msg)

    if len(features) < cluster_count:
        msg = "cluster_count cannot exceed the number of samples."
        raise ValueError(msg)

    model = Pipeline(
        steps=[
            ("scale", StandardScaler()),
            (
                "cluster",
                KMeans(n_clusters=cluster_count, random_state=random_state, n_init="auto"),
            ),
        ]
    )
    clusters = model.fit_predict(features)
    assignments = metadata.copy()
    assignments["cluster"] = clusters

    return ClusterResult(assignments=assignments, model=model)


def summarize_clusters(assignments: pd.DataFrame) -> pd.DataFrame:
    """Return a simple count summary for each cluster."""

    return (
        assignments.groupby("cluster", dropna=False)
        .size()
        .reset_index(name="sample_count")
        .sort_values("cluster")
    )
