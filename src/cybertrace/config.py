"""Shared project paths and defaults."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

DEFAULT_ID_COLUMN = "sample_id"
DEFAULT_CLUSTER_COUNT = 3
NON_FEATURE_COLUMNS = {
    "sample_id",
    "label",
    "attack_type",
    "difficulty",
    "family",
    "source",
    "filename",
    "path",
    "notes",
}
