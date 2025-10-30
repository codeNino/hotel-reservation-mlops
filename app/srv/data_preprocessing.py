import os
import pandas as pd
import numpy as np

from app.utils.logger import AppLogger
from app.utils.error import CustomException
from app.config.paths_config import *
from app.utils.file_handler import read_yaml, load_data

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = AppLogger(__name__)()


class DataProcessor:

    def __init__(self, train_path: str, test_path: str, processed_dir: str, config_path : str):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        
        self.config = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir, exist_ok=True)


    
    def preprocess_data(self, df: pd.DataFrame):
        try:
            logger.info("Starting Data Processing")

            logger.info("Dropping irrelevaqnt columns")
            df.drop(columns=['Unnamed: 0', 'Booking_ID'] , inplace=True)
            df.drop_duplicates(inplace=True)

            categorical_columns = self.config["data_processing"]["categorical_columns"]
            numerical_columns = self.config["data_processing"]["numerical_columns"]

            logger.info("Applying Label Encoding")

            encoder = LabelEncoder()
            mappings = {}

            for col in categorical_columns:
                df[col] = encoder.fit_transform(df[col])

                mappings[col] = {label:code for label,code in zip(encoder.classes_ , encoder.transform(encoder.classes_))}

            logger.info("Label Mappings are : ")
            for col, mapping in mappings.items():
                logger.info(f"{col} : {mapping}")

            logger.info("Doing skewness handling")
            skew_threshold = self.config["data_processing"]["skewness_threshold"]
            skewness = df[numerical_columns].apply(lambda x: x.skew())

            for column in skewness[skewness > skew_threshold].index:
                df[column] = np.log1p(df[column])

            return df       

        except Exception as e:
            logger.error(f"Error during preprocessing step {e}")
            raise CustomException("Error while preprocessing data", e)
        

    def balance_data(self, df: pd.DataFrame):
        try:
            logger.info("Handling Imbalanced data")
            X = df.drop(columns='booking_status')
            y = df["booking_status"]

            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X, y)

            balanced_df = pd.DataFrame(X_resampled, columns = X.columns)
            balanced_df["booking_status"] = y_resampled

            logger.info("Data balanced successfully")
            return balanced_df
        except Exception as e:
            logger.error(f"Error during data balancing : {e}")
            raise CustomException("Failed to balance data", e)
        
    def select_features(self, df: pd.DataFrame):
        try:
            logger.info("Starting Feature Selection")
            X = df.drop(columns = "booking_status")
            y = df["booking_status"]

            model = RandomForestClassifier(random_state=42)
            model.fit(X, y)

            feature_importance = model.feature_importances_
            feature_importance_df = pd. DataFrame({
                         'feature': X.columns,
                'importance': feature_importance
            })

            number_of_features_to_select = self.config["data_processing"]["no_features_select"]

            top_features_importance_df = feature_importance_df.sort_values(by="importance" , ascending=False)

            top_features = top_features_importance_df["feature"].head(number_of_features_to_select).values

            logger.info(f"Top Features Selected : {top_features.tolist() }")

            top_df = df[top_features.tolist() + ["booking_status"]]

            logger.info("Feature Selection Completed")

            return top_df

        except Exception as e:
            logger.error(f"Error during feature selection : {e}")
            raise CustomException("Failed to select features", e)
        

    def export_data(self, df: pd.DataFrame, file_path: str):
        try:
            logger.info("Saving data to processed folder")
            df.to_csv(file_path, index=False)
        except Exception as e:
            logger.error(f"Error during data export : {e}")
            raise CustomException("Failed to export data", e)
        


    def process(self):
        try:
            logger.info("Loading data fro RAW dir")

            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df = self.balance_data(train_df)

            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns]

            self.export_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.export_data(test_df, PROCESSED_TEST_DATA_PATH)

            logger.info("Data Processing completed")

        except Exception as e:
            logger.error(f"Error during data processing : {e}")
            raise CustomException("Failed to process data", e)




if __name__ == "__main__":

    processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH,
            PROCESSED_DIR, CONFIG_PATH)

    processor.process()