import os
import pandas as pd
from .logger import AppLogger
from .error import CustomException
import yaml


logger = AppLogger(__name__)()

def read_yaml(file_path: str):
    try:
        if  not os.path.exists(file_path):
            raise FileNotFoundError(f"File not in given path ")
        with open(file_path, "r") as yaml_file:
            config = yaml.safe_load(yaml_file)
            logger.info("Successfully read the YAML file")
            return config
    except Exception as e:
        logger.error("Error while reading YAML file")
        raise CustomException("Failed to read YAML file", e)
    



def load_data(path: str):
    try:
        logger.info("Loading Data")
        return pd.read_csv(path)
    except Exception as e:
        logger.error(f"Error loading data {e}")
        raise CustomException("Failed to load data", e)