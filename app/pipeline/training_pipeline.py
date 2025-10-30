from app.config.paths_config import *
from app.utils.file_handler import read_yaml
from app.srv.data_ingestion import DataIngestion
from app.srv.data_preprocessing import DataProcessor
from app.srv.model_training import ModelTraining


if __name__ == "__main__":

    ## Data Ingestion
    config = read_yaml(CONFIG_PATH)

    data_ingestion = DataIngestion(config)

    data_ingestion.run()

    ## Data Processing

    processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH,
            PROCESSED_DIR, CONFIG_PATH)

    processor.process()


    ## Model Training

    trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)

    trainer.run()

