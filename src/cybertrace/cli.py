"""Command line interface for CyberTrace."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from cybertrace.clustering import cluster_features, summarize_clusters
from cybertrace.config import DEFAULT_CLUSTER_COUNT, DEFAULT_ID_COLUMN
from cybertrace.extractors import extract_network_log_features
from cybertrace.features import load_feature_table

app = typer.Typer(help="CyberTrace cybersecurity clustering toolkit.")
console = Console()


@app.command()
def cluster(
    input_csv: Annotated[Path, typer.Argument(help="Processed feature CSV to cluster.")],
    output: Annotated[
        Path, typer.Option("--output", "-o", help="Where to write assignments.")
    ] = Path("reports/clusters.csv"),
    clusters: Annotated[
        int, typer.Option("--clusters", "-k", help="Number of clusters to create.")
    ] = DEFAULT_CLUSTER_COUNT,
    id_column: Annotated[
        str, typer.Option("--id-column", help="Unique sample identifier column.")
    ] = DEFAULT_ID_COLUMN,
) -> None:
    """Cluster a processed feature table and write sample assignments."""

    table = load_feature_table(input_csv, id_column=id_column)
    result = cluster_features(table.features, table.metadata, cluster_count=clusters)

    output.parent.mkdir(parents=True, exist_ok=True)
    result.assignments.to_csv(output, index=False)

    summary = summarize_clusters(result.assignments)
    display = Table(title="Cluster Summary")
    display.add_column("Cluster")
    display.add_column("Samples", justify="right")

    for row in summary.itertuples(index=False):
        display.add_row(str(row.cluster), str(row.sample_count))

    console.print(display)
    console.print(f"Wrote cluster assignments to [bold]{output}[/bold]")


@app.command()
def extract_network_log(
    input_csv: Annotated[Path, typer.Argument(help="Safe network event CSV to summarize.")],
    output: Annotated[
        Path, typer.Option("--output", "-o", help="Where to write extracted features.")
    ] = Path("data/processed/features_from_logs.csv"),
) -> None:
    """Extract per-sample features from a simple network event log."""

    features = extract_network_log_features(input_csv, output)
    console.print(f"Extracted {len(features)} samples to [bold]{output}[/bold]")


if __name__ == "__main__":
    app()
