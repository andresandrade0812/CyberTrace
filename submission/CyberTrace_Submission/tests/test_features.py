from pathlib import Path

import pandas as pd

from cybertrace.features import load_feature_table


def test_load_feature_table_splits_metadata_from_numeric_features(tmp_path: Path) -> None:
    path = tmp_path / "features.csv"
    pd.DataFrame(
        {
            "sample_id": ["a", "b"],
            "label": ["benign", "suspicious"],
            "connection_count": [2, 15],
            "protocol_tcp_ratio": [0.8, 0.4],
            "notes": ["normal", "odd"],
        }
    ).to_csv(path, index=False)

    table = load_feature_table(path)

    assert list(table.metadata.columns) == ["sample_id", "label", "notes"]
    assert list(table.features.columns) == ["connection_count", "protocol_tcp_ratio"]
