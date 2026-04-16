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

## Safety Note

This repository is designed for analysis of safe, controlled artifacts. Do not store live malware, credentials, private network captures, or sensitive production data in the repo.
