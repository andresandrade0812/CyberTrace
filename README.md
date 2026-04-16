# CyberTrace

CyberTrace is a Python-based CS544 project for clustering and analyzing suspicious network traffic and malicious file characteristics. The project focuses on cybersecurity investigation first: extracting observable indicators from safe artifacts, grouping similar samples, and explaining what separates benign, suspicious, and malicious behavior.

## Project Goals

- Collect safe artifacts such as packet captures, network logs, metadata, and preexisting sample descriptions.
- Extract measurable features including protocol usage, communication frequency, packet size patterns, file metadata, and entropy-style indicators.
- Cluster samples to discover shared behavioral patterns.
- Produce clear reports that explain what each cluster suggests from a cybersecurity perspective.

## Repository Layout

```text
CyberTrace/
├── data/
│   ├── raw/          # Original safe artifacts. Do not edit these directly.
│   ├── interim/      # Cleaned or normalized intermediate files.
│   └── processed/    # Feature tables ready for clustering.
├── docs/             # Project planning notes and methodology.
├── notebooks/        # Exploratory analysis notebooks.
├── reports/
│   └── figures/      # Charts and generated visualizations.
├── src/cybertrace/   # Python package source code.
└── tests/            # Unit tests for reusable code.
```

## Quick Start

Create a virtual environment and install the project in editable mode:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Run the command line interface:

```bash
cybertrace --help
```

Run clustering against a processed feature CSV:

```bash
cybertrace cluster data/processed/features.csv --output reports/clusters.csv
```

The input CSV should include a `sample_id` column plus numeric feature columns. Optional label columns such as `label`, `family`, or `source` are preserved in the output but are not used for clustering.

Extract features from the included safe example network event log:

```bash
cybertrace extract-network-log data/raw/example_network_events.csv --output data/processed/features_from_logs.csv
```

Then cluster those extracted features:

```bash
cybertrace cluster data/processed/features_from_logs.csv --output reports/example_log_clusters.csv
```

The starter `data/processed/features.csv` file is synthetic and safe. It exists so the analysis workflow can be tested before real course-approved artifacts are selected.

Prepare the included NSL-KDD benchmark sample:

```bash
cybertrace prepare-nsl-kdd data/raw/nsl_kdd_small_training.csv --output data/processed/features_nsl_kdd.csv
```

Run clustering on the prepared NSL-KDD feature table:

```bash
cybertrace cluster data/processed/features_nsl_kdd.csv --output reports/real_clusters.csv --clusters 3
```

The real-data summary is written to `reports/real_dataset_analysis.md`, and the generated cluster projection is saved at `reports/figures/nsl_kdd_clusters.png`.

## Dataset Source

The first real-data milestone uses a small public NSL-KDD CSV sample downloaded from the `Small Training Set.csv` file in the [Jehuty4949/NSL_KDD GitHub mirror](https://github.com/Jehuty4949/NSL_KDD). The benchmark is described by the Canadian Institute for Cybersecurity on the [ISCX NSL-KDD dataset page](https://www.unb.ca/cic/datasets/nsl.html). NSL-KDD is an older but safe intrusion-detection benchmark derived from KDD-style network connection records. It is useful for this course project because it provides labeled benign and attack traffic records without requiring live malware handling.

## Safety Note

This repository is designed for analysis of safe, controlled artifacts. Do not store live malware, credentials, private network captures, or sensitive production data in the repo.
