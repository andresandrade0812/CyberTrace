from pathlib import Path

import pandas as pd

from cybertrace.datasets import NSL_KDD_COLUMNS, prepare_nsl_kdd_dataset


def test_prepare_nsl_kdd_dataset_maps_labels_and_encodes_categories(tmp_path: Path) -> None:
    input_csv = tmp_path / "nsl.csv"
    output_csv = tmp_path / "features.csv"
    benign = _nsl_row(protocol="tcp", service="http", flag="SF", attack_type="normal")
    attack = _nsl_row(protocol="udp", service="private", flag="S0", attack_type="neptune")
    pd.DataFrame([benign, attack]).to_csv(input_csv, header=False, index=False)

    prepared = prepare_nsl_kdd_dataset(input_csv, output_csv)

    assert output_csv.exists()
    assert list(prepared["label"]) == ["benign", "malicious"]
    assert "protocol_type_tcp" in prepared.columns
    assert "service_private" in prepared.columns
    assert "flag_S0" in prepared.columns


def _nsl_row(protocol: str, service: str, flag: str, attack_type: str) -> list[object]:
    row = dict.fromkeys(NSL_KDD_COLUMNS, 0)
    row["protocol_type"] = protocol
    row["service"] = service
    row["flag"] = flag
    row["attack_type"] = attack_type
    row["difficulty"] = 20
    return [row[column] for column in NSL_KDD_COLUMNS]
