import os
from pathlib import Path

def get_project_root() -> Path:
    """Find the project root by looking for pyproject.toml or .git"""
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "pyproject.toml").exists() or (parent / ".git").exists():
            return parent
    # fallback: assume 3 levels up from this file
    return current.parents[3]

APP_BASE_DIR = get_project_root()


##################### DATA INGESTION ###################


RAW_DIR =  APP_BASE_DIR / "artifacts/raw"
RAW_FILE_PATH = os.path.join(RAW_DIR, "raw.csv")
TRAIN_FILE_PATH = os.path.join(RAW_DIR, "train.csv")
TEST_FILE_PATH = os.path.join(RAW_DIR, "test.csv")

CONFIG_PATH = APP_BASE_DIR / "app/config/config.yaml"




################## DATA PROCESSING #################


PROCESSED_DIR = APP_BASE_DIR / "artifacts/processed"
PROCESSED_TRAIN_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_train.csv")
PROCESSED_TEST_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_test.csv")




############# MODEL TRAINING ###########################
MODEL_OUTPUT_PATH = APP_BASE_DIR / "artifacts/models/lgbm_model.pkl"
MODEL_DIR = APP_BASE_DIR / "artifacts/models/"