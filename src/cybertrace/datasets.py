"""Dataset preparation commands for public cybersecurity benchmarks."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from cybertrace.features import save_feature_table

NSL_KDD_COLUMNS = [
    "duration",
    "protocol_type",
    "service",
    "flag",
    "src_bytes",
    "dst_bytes",
    "land",
    "wrong_fragment",
    "urgent",
    "hot",
    "num_failed_logins",
    "logged_in",
    "num_compromised",
    "root_shell",
    "su_attempted",
    "num_root",
    "num_file_creations",
    "num_shells",
    "num_access_files",
    "num_outbound_cmds",
    "is_host_login",
    "is_guest_login",
    "count",
    "srv_count",
    "serror_rate",
    "srv_serror_rate",
    "rerror_rate",
    "srv_rerror_rate",
    "same_srv_rate",
    "diff_srv_rate",
    "srv_diff_host_rate",
    "dst_host_count",
    "dst_host_srv_count",
    "dst_host_same_srv_rate",
    "dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate",
    "dst_host_serror_rate",
    "dst_host_srv_serror_rate",
    "dst_host_rerror_rate",
    "dst_host_srv_rerror_rate",
    "attack_type",
    "difficulty",
]

NSL_KDD_CATEGORICAL_COLUMNS = ["protocol_type", "service", "flag"]
NSL_KDD_METADATA_COLUMNS = ["sample_id", "label", "attack_type", "source", "difficulty"]


def prepare_nsl_kdd_dataset(
    input_csv: Path,
    output_csv: Path,
    *,
    max_rows: int | None = None,
) -> pd.DataFrame:
    """Convert an NSL-KDD CSV into the CyberTrace feature-table format."""

    frame = pd.read_csv(input_csv, header=None, names=NSL_KDD_COLUMNS)
    if max_rows is not None:
        frame = frame.head(max_rows)

    prepared = pd.DataFrame(
        {
            "sample_id": [f"nsl_kdd_{index:05d}" for index in range(1, len(frame) + 1)],
            "label": frame["attack_type"].map(_to_binary_label),
            "attack_type": frame["attack_type"],
            "source": input_csv.name,
            "difficulty": frame["difficulty"],
        }
    )

    numeric_features = frame.drop(
        columns=[*NSL_KDD_CATEGORICAL_COLUMNS, "attack_type", "difficulty"]
    ).apply(pd.to_numeric)
    categorical_features = pd.get_dummies(
        frame[NSL_KDD_CATEGORICAL_COLUMNS],
        columns=NSL_KDD_CATEGORICAL_COLUMNS,
        dtype=int,
    )

    result = pd.concat([prepared, numeric_features, categorical_features], axis=1)
    save_feature_table(result, output_csv)
    return result


def _to_binary_label(attack_type: str) -> str:
    return "benign" if attack_type == "normal" else "malicious"
