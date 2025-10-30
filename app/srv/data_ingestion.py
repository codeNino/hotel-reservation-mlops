import os
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from app.utils.logger import AppLogger
from app.utils.error import CustomException
from app.config.secrets import SecretManager
from app.config.paths_config import *
from app.utils.file_handler import read_yaml


logger = AppLogger(__name__)()

class DataIngestion:

    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]

        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info(f"Data Ingestion started with {self.bucket_name} and file is {self.file_name}")


    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)

            blob.download_to_filename(RAW_FILE_PATH)

            logger.info(f"Raw file is successfully downloaded to {RAW_FILE_PATH}")

        except Exception as e:
            logger.error("Error while downloading the csv file")
            raise CustomException("Failed to download csv file", e)
        
    def split_data(self):
        try:
            logger.info("Starting the splitting process")

            data = pd.read_csv(RAW_FILE_PATH)

            train_data, test_data = train_test_split(data, train_size=self.train_test_ratio, random_state=42)

            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)

            logger.info(f"Train Data saved to {TRAIN_FILE_PATH}")
            logger.info(f"Test Data saved to {TEST_FILE_PATH}")
        
        except Exception as e:
            logger.error("Error while splitting data")
            raise CustomException("Failed to split data into training and test sets", e)
        

    def run(self):
        try:
            logger.info("Starting data ingestion process")

            self.download_csv_from_gcp()
            self.split_data()

            logger.info("Data ingestion completed successfully")

        except CustomException as ce:
            logger.error(f"CustomException :: {str(ce)}")

        finally:
            logger.info("Data ingestion completed")


if __name__ == "__main__":
    config = read_yaml(CONFIG_PATH)

    data_ingestion = DataIngestion(config)

    data_ingestion.run()





