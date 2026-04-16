"""Feature extraction helpers for safe network event logs."""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd

from cybertrace.features import save_feature_table

REQUIRED_NETWORK_LOG_COLUMNS = {
    "sample_id",
    "timestamp",
    "dst_ip",
    "dst_port",
    "protocol",
    "packet_size",
    "bytes_out",
    "dns_query",
    "http_request",
    "connection_success",
}


def extract_network_log_features(input_csv: Path, output_csv: Path) -> pd.DataFrame:
    """Extract per-sample behavioral features from a safe network event CSV."""

    events = pd.read_csv(input_csv, parse_dates=["timestamp"])
    missing_columns = REQUIRED_NETWORK_LOG_COLUMNS.difference(events.columns)
    if missing_columns:
        formatted = ", ".join(sorted(missing_columns))
        msg = f"Network log is missing required columns: {formatted}"
        raise ValueError(msg)

    rows = []
    for sample_id, group in events.groupby("sample_id", sort=True):
        packet_sizes = group["packet_size"]
        protocols = group["protocol"].str.upper()
        duration = (group["timestamp"].max() - group["timestamp"].min()).total_seconds()
        connection_count = len(group)
        successful_connections = group["connection_success"].sum()
        failed_connections = connection_count - successful_connections

        rows.append(
            {
                "sample_id": sample_id,
                "label": "unknown",
                "source": input_csv.name,
                "connection_count": connection_count,
                "unique_destinations": group["dst_ip"].nunique(),
                "unique_ports": group["dst_port"].nunique(),
                "avg_packet_size": round(packet_sizes.mean(), 3),
                "packet_size_std": round(_safe_std(packet_sizes), 3),
                "tcp_ratio": round((protocols == "TCP").mean(), 3),
                "udp_ratio": round((protocols == "UDP").mean(), 3),
                "dns_query_count": int(group["dns_query"].sum()),
                "http_request_count": int(group["http_request"].sum()),
                "failed_connection_ratio": round(failed_connections / connection_count, 3),
                "beacon_score": round(_beacon_score(group["timestamp"]), 3),
                "bytes_out_ratio": round(group["bytes_out"].sum() / packet_sizes.sum(), 3),
                "duration_seconds": int(duration),
            }
        )

    features = pd.DataFrame(rows)
    save_feature_table(features, output_csv)
    return features


def _safe_std(series: pd.Series) -> float:
    if len(series) <= 1:
        return 0.0
    return float(series.std())


def _beacon_score(timestamps: pd.Series) -> float:
    """Estimate repeated timing regularity on a 0-1 scale."""

    sorted_timestamps = timestamps.sort_values()
    intervals = sorted_timestamps.diff().dt.total_seconds().dropna()
    if len(intervals) < 2:
        return 0.0

    mean_interval = intervals.mean()
    if mean_interval <= 0 or math.isnan(mean_interval):
        return 0.0

    coefficient_of_variation = intervals.std() / mean_interval
    return max(0.0, min(1.0, 1.0 - coefficient_of_variation))
