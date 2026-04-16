from pathlib import Path

import pandas as pd

from cybertrace.extractors import extract_network_log_features


def test_extract_network_log_features_writes_expected_columns(tmp_path: Path) -> None:
    input_csv = tmp_path / "events.csv"
    output_csv = tmp_path / "features.csv"
    pd.DataFrame(
        {
            "sample_id": ["demo", "demo", "demo"],
            "timestamp": [
                "2026-04-16T10:00:00",
                "2026-04-16T10:00:10",
                "2026-04-16T10:00:20",
            ],
            "src_ip": ["10.0.0.5"] * 3,
            "dst_ip": ["1.1.1.1", "1.1.1.1", "8.8.8.8"],
            "dst_port": [53, 53, 443],
            "protocol": ["UDP", "UDP", "TCP"],
            "packet_size": [100, 120, 500],
            "bytes_out": [50, 55, 250],
            "dns_query": [1, 1, 0],
            "http_request": [0, 0, 1],
            "connection_success": [1, 1, 0],
        }
    ).to_csv(input_csv, index=False)

    features = extract_network_log_features(input_csv, output_csv)

    assert output_csv.exists()
    assert features.loc[0, "sample_id"] == "demo"
    assert features.loc[0, "connection_count"] == 3
    assert features.loc[0, "unique_destinations"] == 2
    assert features.loc[0, "dns_query_count"] == 2
