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
- Safe dataset selection and artifact inventory.
- Feature extraction notebook or script.
- Baseline clustering experiments.
- Cluster interpretation with tables and figures.
- Final report and presentation.

## Safety Rules

- Use only controlled, course-appropriate artifacts.
- Do not commit live malware or sensitive captures.
- Keep raw data immutable and record where each artifact came from.
