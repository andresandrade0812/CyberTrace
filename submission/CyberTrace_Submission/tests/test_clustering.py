import pandas as pd
import pytest

from cybertrace.clustering import cluster_features, summarize_clusters


def test_cluster_features_returns_assignment_for_each_sample() -> None:
    features = pd.DataFrame(
        {
            "connection_count": [1, 2, 50, 60],
            "avg_packet_size": [100, 120, 900, 950],
        }
    )
    metadata = pd.DataFrame({"sample_id": ["a", "b", "c", "d"], "label": ["benign"] * 4})

    result = cluster_features(features, metadata, cluster_count=2)

    assert len(result.assignments) == 4
    assert "cluster" in result.assignments.columns
    assert result.assignments["cluster"].nunique() == 2


def test_cluster_count_cannot_exceed_sample_count() -> None:
    features = pd.DataFrame({"connection_count": [1, 2]})
    metadata = pd.DataFrame({"sample_id": ["a", "b"]})

    with pytest.raises(ValueError, match="number of samples"):
        cluster_features(features, metadata, cluster_count=3)


def test_summarize_clusters_counts_samples() -> None:
    assignments = pd.DataFrame({"sample_id": ["a", "b", "c"], "cluster": [0, 0, 1]})

    summary = summarize_clusters(assignments)

    assert summary.to_dict("records") == [
        {"cluster": 0, "sample_count": 2},
        {"cluster": 1, "sample_count": 1},
    ]
