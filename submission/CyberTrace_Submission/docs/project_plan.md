# Project Plan

## Working Question

How can clustering and comparative analysis help identify patterns in suspicious network traffic and malicious file characteristics without relying only on signature matching?

## Proposed Pipeline

1. Collect safe artifacts in `data/raw/`.
2. Normalize or clean artifacts into `data/interim/`.
3. Extract measurable features into `data/processed/features.csv`.
4. Run clustering with `cybertrace cluster`.
5. Interpret clusters and document cybersecurity findings in `reports/`.

## Candidate Features

- Network behavior: connection counts, unique source or destination counts, port distribution, protocol counts, packet size statistics, timing gaps, and repeated beaconing indicators.
- File characteristics: file size, extension, hashes stored as metadata, entropy-style measures, section counts, import counts, string counts, and timestamp metadata.
- Context fields: benign or malicious label, source dataset, sample family, analyst notes, and collection date.

## Milestones

- Repository scaffold and Python environment.
- Safe starter dataset selection and artifact inventory.
- Feature extraction notebook or script.
- Baseline clustering experiments with `data/processed/features.csv`.
- Cluster interpretation with tables and figures.
- Final report and presentation.

## Current Starter Dataset

The project currently includes a small synthetic feature table at `data/processed/features.csv`.
It contains benign, suspicious, and malicious-like network behavior examples. These rows are
not real malware traffic; they are safe placeholders for testing the analysis pipeline.

The project also includes `data/raw/example_network_events.csv`, a tiny safe event log that can
be converted into features with:

```bash
cybertrace extract-network-log data/raw/example_network_events.csv --output data/processed/features_from_logs.csv
```

## Real Dataset Milestone

The first real dataset is a small NSL-KDD training CSV sample stored at
`data/raw/nsl_kdd_small_training.csv`. It was downloaded from the `Small Training Set.csv`
file in the `Jehuty4949/NSL_KDD` GitHub mirror and is based on the NSL-KDD benchmark
described by the Canadian Institute for Cybersecurity. It is prepared with:

```bash
cybertrace prepare-nsl-kdd data/raw/nsl_kdd_small_training.csv --output data/processed/features_nsl_kdd.csv
```

The prepared dataset contains 1,011 records:

- 516 benign records
- 495 malicious records

Baseline clustering is run with:

```bash
cybertrace cluster data/processed/features_nsl_kdd.csv --output reports/real_clusters.csv --clusters 3
```

Current baseline cluster mix:

- Cluster 0: 493 benign, 95 malicious
- Cluster 1: 23 benign, 109 malicious
- Cluster 2: 0 benign, 291 malicious

This gives the final report a clear starting interpretation: one cluster is mostly benign, one
is mixed but malicious-heavy, and one is fully malicious in this sample.

## Safety Rules

- Use only controlled, course-appropriate artifacts.
- Do not commit live malware or sensitive captures.
- Keep raw data immutable and record where each artifact came from.
