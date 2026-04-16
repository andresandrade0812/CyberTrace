# Data Directory

Store project data by processing stage:

- `raw/`: original safe artifacts, packet captures, logs, or metadata exports.
- `interim/`: cleaned or normalized intermediate files.
- `processed/`: feature tables used by clustering and reporting.

Do not commit sensitive data, private captures, credentials, or live malware. The `.gitkeep` files preserve the directory structure while keeping data files out of version control by default.
