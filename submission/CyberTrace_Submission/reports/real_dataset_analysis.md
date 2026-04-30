# Real Dataset Analysis

## Dataset

CyberTrace uses a small public NSL-KDD training CSV sample for the first real-data milestone. The prepared table keeps sample identifiers, binary labels, original attack types, source file metadata, and numeric/encoded features suitable for clustering.

- Raw records: 1011
- Benign records: 516
- Malicious records: 495
- Feature columns used for clustering: 106
- Source: `Small Training Set.csv` from the `Jehuty4949/NSL_KDD` GitHub mirror
- Benchmark reference: Canadian Institute for Cybersecurity NSL-KDD dataset page

## Cluster Label Mix

| cluster | benign | malicious |
| --- | --- | --- |
| 0 | 493 | 95 |
| 1 | 23 | 109 |
| 2 | 0 | 291 |

## Attack Types By Cluster

| cluster | back | buffer_overflow | guess_passwd | ipsweep | loadmodule | neptune | nmap | normal | pod | portsweep | rootkit | satan | smurf | teardrop | warezclient |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 6 | 6 | 0 | 27 | 1 | 0 | 5 | 493 | 1 | 0 | 4 | 5 | 17 | 11 | 12 |
| 1 | 0 | 0 | 1 | 4 | 0 | 58 | 0 | 23 | 0 | 35 | 0 | 11 | 0 | 0 | 0 |
| 2 | 0 | 0 | 0 | 0 | 0 | 287 | 2 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |

## Interpretation Notes

- Clusters with mostly benign records can be discussed as normal-like network behavior.
- Clusters with high malicious concentration should be inspected by attack type and by features such as error rates, count-based traffic features, and byte counts.
- Because this is clustering, labels are used only after the fact to interpret groups; they are not used to fit the clusters.
- NSL-KDD is useful and safe for a course project, but it is an older benchmark, so the final report should mention that results may not fully represent modern traffic.
