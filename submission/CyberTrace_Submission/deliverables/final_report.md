# CyberTrace Final Report

**Course Project:** CS544

**Group Members:** Victor Andrade and Ben Miller

## Abstract

CyberTrace explores how clustering can support cybersecurity analysis when suspicious
traffic or artifacts do not match a known signature exactly. The project emphasizes
investigative workflow rather than only classifier accuracy. In the final implementation,
Python is used to prepare a safe public intrusion-detection benchmark, convert it into a
numeric feature table, cluster the samples, and generate interpretable outputs for review.
The real dataset milestone uses a small NSL-KDD training sample with 1,011 records and
produces three clusters that separate mostly benign traffic from two malicious-heavy groups.
These results suggest that clustering can help analysts prioritize review, compare related
behaviors, and distinguish clearly malicious traffic from normal-like activity.

## 1. Problem Statement

The problem addressed by CyberTrace is how to compare suspicious network-related artifacts
without depending only on exact signature matching. Traditional rule-based and signature-based
defenses remain valuable, but they can miss new, modified, or behaviorally subtle threats.
Analysts still need a way to examine observable characteristics and organize suspicious activity
into groups that support investigation.

More specifically, this project asks whether safe network traffic records can be transformed into
a useful feature representation and then clustered into groups that reveal meaningful differences
between benign and malicious behavior. The goal is not to claim perfect detection, but to build
a reproducible analysis workflow that helps answer why certain samples look suspicious and how
they relate to one another.

A useful final project in this space should therefore do three things well. First, it should
represent the problem in a way that is close to actual analyst reasoning. Second, it should be
implemented in a reproducible way rather than as a fragile one-time experiment. Third, it should
produce findings that can be discussed in plain cybersecurity language, not only in model-centric
terms. CyberTrace was designed around those three needs.

## 2. Motivation

This problem is important because modern cybersecurity work involves more than checking whether
something matches a known bad indicator. Analysts often face large sets of events, connections,
or artifacts that need quick prioritization. If clustering can place similar behaviors together,
then it can reduce analyst effort, reveal repeated suspicious patterns, and provide a clearer
starting point for incident response or deeper forensic review.

The motivation is also practical for a course project. A safe benchmark dataset can still capture
many of the behavioral questions that matter in cybersecurity: error rates, destination patterns,
service usage, and connection counts. By focusing on those interpretable signals, the project
stays aligned with real analyst thinking instead of turning into a purely abstract machine
learning exercise.

This motivation also connects directly to incident response. In a live environment, defenders
often need to sort through events that are not immediately conclusive. A clustering-based view
does not replace expert judgment, but it can create structure around that judgment by showing
which samples appear isolated, which appear repeated, and which share behavior with clearly
malicious records. That makes the exploration process more systematic.

## 3. Dataset and Safety

The final project uses a small public NSL-KDD training CSV sample stored in
`data/raw/nsl_kdd_small_training.csv`. NSL-KDD is a safe, labeled intrusion-detection
benchmark derived from KDD-style connection records. It is appropriate for this course
project because it avoids handling live malware or sensitive production traffic while still
providing realistic benign and attack labels for interpretation.

- Total records: 1011
- Benign records: 516
- Malicious records: 495
- Source mirror: Jehuty4949/NSL_KDD GitHub repository
- Benchmark reference: Canadian Institute for Cybersecurity NSL-KDD page

Using NSL-KDD lets the project focus on exploratory cybersecurity analysis without introducing
the risk of storing live malware, sensitive enterprise packet captures, or private credentials
inside the repository. That safety constraint matters because the project should be reproducible,
shareable, and suitable for course submission.

The dataset is also useful because it includes a mixture of normal traffic and several attack
categories such as neptune, portsweep, ipsweep, and satan. Even though NSL-KDD is older, it still
provides a reasonable environment for discussing the core question of this project: whether groups
of records can be organized into meaningful behavioral clusters that reflect benign or malicious
activity.

## 4. Contributions

The main contributions of this work are:

1. A Python repository structure designed around cybersecurity investigation workflows.
2. A command-line data preparation step for converting raw NSL-KDD rows into a CyberTrace
   feature table with metadata and numeric model inputs.
3. A clustering pipeline that standardizes features, applies KMeans, and writes cluster
   assignments for further analysis.
4. Notebooks, figures, tests, and packaging scripts that make the project reproducible.
5. A final interpretation of how the discovered clusters relate to benign and malicious behavior.

An important contribution is that the project does not stop at code execution. It also packages
the work into a report, presentation, and submission archive so the analysis can be reviewed by
someone who did not watch the implementation happen. That makes the work more complete and more
appropriate for a final academic submission.

## 5. Methodology

The project workflow has four main stages:

1. Store raw safe datasets in `data/raw/`.
2. Prepare the dataset into a CyberTrace feature table with the `prepare-nsl-kdd` command.
3. Standardize numeric features and cluster them with KMeans.
4. Interpret cluster membership by comparing labels and attack types after clustering.

The NSL-KDD preparer converts raw rows into a table containing metadata columns
(`sample_id`, `label`, `attack_type`, `source`, and `difficulty`) plus numeric features and
one-hot encoded categorical protocol, service, and flag fields. Clustering is then applied
only to the numeric feature matrix, not to the labels.

This approach matters because it preserves the separation between unsupervised learning and
interpretation. The labels are not used to fit the clustering model; instead, they are used
afterward to understand what kinds of behaviors ended up together. That is much closer to how
clustering would be used in an exploratory cybersecurity workflow.

KMeans was chosen as the baseline method because it is easy to explain, easy to reproduce, and
useful for a first clustering pass over standardized numeric features. The cluster count of three
was selected as a straightforward baseline that could separate normal-like, mixed, and strongly
malicious behavior. This is not presented as the only correct choice, but as an interpretable
starting point for the exploration.

The methodology also includes validation at the software level. The repository contains automated
tests for clustering, feature loading, extraction, and dataset preparation. That matters because
a cybersecurity analysis workflow should not depend only on manually repeated notebook steps. By
testing the code paths that produce the prepared data and final outputs, the project improves its
reliability and repeatability.

From an investigative standpoint, the feature preparation step is especially important. Raw traffic
records are rarely useful unless they can be summarized into stable technical signals. In this
project, those signals include byte-oriented values, counts, error-related rates, service usage,
and protocol or flag indicators. Each of these features captures one piece of behavioral evidence,
and clustering works by evaluating how those pieces line up across many records at once.

This feature-centric view is one reason the project remains explainable. Even if the clustering
itself is unsupervised, the inputs still have a concrete meaning that analysts can discuss. That
means the final write-up can talk about repeated attack behavior, normal-like connections, service
patterns, and suspicious concentration, rather than presenting the clusters as unexplained black
box outputs.

## 6. Implementation

CyberTrace is implemented as a Python package under `src/cybertrace/`. The main commands are:

- `cybertrace prepare-nsl-kdd data/raw/nsl_kdd_small_training.csv --output data/processed/features_nsl_kdd.csv`
- `cybertrace cluster data/processed/features_nsl_kdd.csv --output reports/real_clusters.csv --clusters 3`

The codebase also includes starter synthetic data, a simple network-log extractor, notebooks,
tests, and figures. The repository was validated with Ruff and Pytest before packaging.

The implementation also includes a reproducible submission builder that generates the final
report, presentation slides, and zip archive. This makes the final project easier to inspect,
rerun, and update if small report changes are needed before submission.

From a software-engineering perspective, the project is organized into clear responsibilities.
Dataset preparation logic lives in a dataset module, clustering logic lives in its own module,
shared configuration is centralized, and the command-line interface ties those pieces together.
This structure makes the code easier to extend to new datasets or additional analysis commands.

The use of notebooks is intentionally limited to exploration and communication. The core logic
needed to reproduce the project results lives in the package and CLI commands, which means the
project can still be rerun from the terminal without depending on interactive notebook state.

That design choice has practical benefits for a final project. It means someone reviewing the
submission can run the code paths directly, inspect the generated artifacts, and understand the
main flow without reconstructing hidden notebook state. It also makes the project more maintainable
because new datasets or additional reporting layers can be added incrementally as separate modules.

## 7. Findings and Results

The real dataset clustering produced three groups:

- Cluster 0: 588 samples (493 benign, 95 malicious, 83.8% benign)
- Cluster 1: 132 samples (23 benign, 109 malicious, 82.6% malicious)
- Cluster 2: 291 samples (0 benign, 291 malicious, 100.0% malicious)

The cluster label mix is:

- Cluster 0: 493 benign and 95 malicious
- Cluster 1: 23 benign and 109 malicious
- Cluster 2: 0 benign and 291 malicious

The most common attack types in the sample are:

- normal: 516
- neptune: 345
- portsweep: 36
- ipsweep: 31
- satan: 17
- smurf: 17
- warezclient: 12
- teardrop: 11

### Cluster Interpretation

Cluster 0 is primarily benign and functions as the most normal-like group in the analysis.
It still contains a smaller malicious subset, which reflects the fact that unsupervised
clustering groups by shared behavior rather than by ground-truth labels alone.

Cluster 1 is malicious-heavy and includes a mixture of neptune, portsweep, satan, and a
smaller number of benign records. This suggests a mixed suspicious-behavior cluster where
attack traffic shares count-based or rate-based characteristics with some normal connections.

Cluster 2 is entirely malicious in this sample and is dominated by neptune records. This
is the clearest malicious cluster in the baseline run and shows that clustering can isolate
a strongly attack-oriented region of the feature space.

These results reveal an important pattern. The baseline run did not create one single malicious
cluster containing every attack record. Instead, it produced at least two malicious-heavy groups:
one mixed cluster and one extremely concentrated malicious cluster. That suggests the malicious
traffic in the sample is not behaviorally uniform. Some attacks share characteristics with each
other closely enough to form a concentrated cluster, while others overlap more with a wider range
of traffic patterns.

That distinction matters for cybersecurity interpretation. A strongly concentrated malicious
cluster may correspond to repeated or stereotyped attack behavior, which is often easier to flag
and isolate. A mixed malicious-heavy cluster is different: it reflects a region of the feature
space where suspicious traffic may blend with more ordinary behavior, making investigation more
challenging and more dependent on contextual review.

The attack-type distribution helps reinforce this point. The sample contains a substantial number
of neptune records, and those records dominate the most malicious cluster. By contrast, portsweep,
ipsweep, satan, and smaller attack categories appear in more mixed groupings. That suggests some
attack behaviors are much more behaviorally concentrated than others, which is exactly the kind of
pattern a clustering-based exploratory workflow should be able to reveal.

The benign records also tell an important story. Most benign traffic is concentrated in Cluster 0,
which gives the analysis a clear normal-like reference point. However, a smaller number of benign
records appear in a malicious-heavy cluster. That overlap is a reminder that not every suspicious
looking pattern is malicious and that not every benign record is behaviorally simple. In practice,
that is why analysts need both grouping methods and contextual judgment.

An important takeaway is that clustering did not create a perfect benign-versus-malicious split,
and that is actually useful to discuss. Unsupervised methods group by similarity, so mixed
clusters highlight where suspicious and benign records share overlapping characteristics. That
kind of ambiguity is realistic in cybersecurity analysis and is often where investigators spend
the most time.

## 8. Implications

The results support the project goal: clustering can help analysts organize traffic into useful
groups and interpret those groups in cybersecurity terms. The workflow does not replace
signature-based or supervised detection, but it creates a structured investigative view of the
data. In practice, this can help analysts prioritize clusters for deeper review, identify
families of suspicious behavior, and compare what separates benign from malicious traffic
patterns.

Another implication is educational: a relatively compact Python project can still model the full
arc of a cybersecurity data analysis task. The repo now includes preparation, experimentation,
interpretation, reporting, and packaging, which makes it a strong demonstration project beyond
just a one-off notebook.

There is also an implication for how students and practitioners think about unsupervised methods.
Clustering is sometimes treated as a vague exploratory add-on, but in this project it becomes a
practical organizational tool. The value is not only in the cluster assignments themselves, but
in the discipline of preparing interpretable features, comparing group composition, and asking
what characteristics make one cluster look more suspicious than another.

The project also suggests a broader lesson about cybersecurity analytics: interpretation is often
the bridge between data science and operational usefulness. A model output by itself is not enough.
What makes the output valuable is the ability to explain why a cluster appears suspicious, what
technical signals are likely contributing to that grouping, and how an analyst might act on the
finding. CyberTrace intentionally emphasizes that interpretive step.

Because of that emphasis, the project contributes not only a result but also a workflow pattern.
The pattern is: prepare safe data, cluster behaviorally similar records, compare discovered groups
to known labels after the fact, and then translate those groups into plain-language cybersecurity
insights. That pattern is portable and can be reused on other safe datasets or more advanced future
versions of the project.

## 9. Group Members and Contributions

The project was completed by Victor Andrade and Ben Miller.

### Victor Andrade

- Implemented the Python repository structure and CLI commands.
- Added dataset preparation, clustering, tests, notebooks, and deliverable packaging.
- Integrated the real dataset outputs and final submission materials.

### Ben Miller

- Helped shape the cybersecurity framing of the project.
- Contributed to the problem definition, motivation, and interpretation goals.
- Supported the final explanation of findings, implications, and future directions.

These contribution descriptions are meant to make the division of work visible in the final
submission rather than leaving the project to appear as a single undifferentiated artifact. If
the group wants to revise the exact wording, this section can be edited easily before submission.

## 10. Limitations

- NSL-KDD is an older benchmark and may not fully represent modern enterprise traffic.
- The current clustering uses KMeans with a fixed cluster count of three for the baseline run.
- This project focuses on network-connection style benchmark features rather than live packet
  parsing or current malware families.
- Interpretation is aided by labels after clustering, so future work should add stronger
  feature-importance analysis and expanded datasets.

Another limitation is that the current report emphasizes one baseline clustering result rather
than a larger sweep across many parameter settings. That is acceptable for a course project, but
a deeper study would compare alternative values of k, different random seeds, and potentially
different distance-based or density-based clustering methods.

## 11. Future Work

- Evaluate additional safe public datasets such as CIC-style flow data.
- Compare KMeans with hierarchical clustering or DBSCAN.
- Add packet-capture or Zeek/Suricata preparation commands for richer lab artifacts.
- Expand reporting with more visualizations and cluster-specific feature summaries.

Future work should also focus on more modern datasets and a stronger comparison of clustering
quality. For example, silhouette scores, per-feature summary tables, and comparisons across
multiple values of k would help show how stable the discovered groups are. Another strong next
step would be mapping the cluster outputs to concrete analyst actions, such as escalation,
triage, or additional artifact collection.

Future work could also connect the project more directly to operational workflows. For example,
cluster outputs might be used to generate short analyst notes, candidate incident categories, or
recommendations for which samples deserve manual review first. That would move the project from
a strong exploratory analysis into a stronger analyst-support prototype.

## 12. Reproducibility and Practical Value

One of the strengths of the final project is that the entire workflow can be rerun from the
repository itself. The raw dataset, preparation step, clustering command, notebooks, figures,
tests, report source, slide deck, and submission builder are all included together. That means
the project is not just a set of final screenshots or manually written conclusions; it is a
working pipeline that can be inspected and executed again.

This reproducibility has practical value for cybersecurity work. Analysts and teams often need to
review not only results, but also how those results were produced. A clear chain from raw input
to prepared features to cluster assignments to interpretation makes it easier to trust the output,
spot weaknesses, and extend the workflow to new datasets. Even in a classroom context, that kind
of transparency is worth emphasizing because it reflects good security engineering practice.

The project is also useful as a template. Although the current implementation centers on a safe
benchmark, the same structure could be reused for lab packet captures, Zeek logs, Suricata alerts,
or other safe feature-rich artifacts. In that sense, the final submission is not only a finished
assignment but also a foundation for future cybersecurity analysis projects.

## 13. Conclusion

CyberTrace demonstrates that a Python-based clustering pipeline can support cybersecurity
analysis by preparing safe datasets, grouping samples by behavior, and producing interpretable
outputs. The final implementation achieves the project objective by delivering code, data,
results, tests, a report, and presentation materials in a reproducible repository.
