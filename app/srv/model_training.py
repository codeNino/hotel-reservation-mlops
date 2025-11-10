import os
import json
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
from sklearn.base import BaseEstimator
import lightgbm as lgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from scipy.stats import randint

import mlflow
import mlflow.sklearn

from app.utils.logger import AppLogger
from app.utils.error import CustomException
from app.config.paths_config import *
from app.config.model_params import *
from app.utils.file_handler import read_yaml, load_data


logger = AppLogger(__name__)()


class ModelTraining:


    def __init__(self, train_path: str, test_path: str, model_output_path: str):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        self.params_dist = LIGHTGBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    
    def load_and_split_data(self):
        try:
            logger.info(f"Loading data from {self.train_path}")
            train_df = load_data(self.train_path)

            logger.info(f"Loading data from {self.test_path}")
            test_df = load_data(self.test_path)

            X_train = train_df.drop(columns= ["booking_status"])
            y_train = train_df["booking_status"]


            X_test = test_df.drop(columns= ["booking_status"])
            y_test = test_df["booking_status"]

            logger.info("Data Splitted successsfully")

            return X_train, y_train, X_test, y_test

        except Exception as e:
            logger.error(f"Error while loading data : {e}")
            raise CustomException("Failed to load and split data", e)
        

    def train_lgbm(self, X_train, y_train):
        try:
            logger.info("Initializing model")
            model = lgb.LGBMClassifier(random_state=self.random_search_params["random_state"])
            logger.info("Starting hyperparameter tuning")
            random_search = RandomizedSearchCV(
                estimator=model,
                param_distributions=self.params_dist,
                n_iter=self.random_search_params["n_iter"],
                cv= self.random_search_params["cv"],
                n_jobs= self.random_search_params["n_jobs"],
                verbose= self.random_search_params["verbose"],
                random_state= self.random_search_params["random_state"],
                scoring= self.random_search_params["scoring"]
            )

            logger.info("Starting Hyperparameter tuning ")

            random_search.fit(X_train, y_train)

            logger.info("Hyperparameter tuning completed ")

            best_params = random_search.best_params_

            best_model = random_search.best_estimator_

            logger.info(f"Best paramters : {best_params}")

            return best_model


        except Exception as e:
            logger.error(f"Error while training lgbm model : {e}")
            raise CustomException("Failed to train lgbm model", e)
        

    def export_feature_list(self, X_test: pd.DataFrame):
        feature_schema = {
    col: str(dtype)
    for col, dtype in X_test.dtypes.items()
}

# Save both list and schema
        data = {
    "features": list(X_test.columns),
    "schema": feature_schema
}

        with open(f"{APP_BASE_DIR}/features.json", "w") as f:
            json.dump(data, f, indent=4)
    
    def evaluate_model(self, model: BaseEstimator, X_test: pd.DataFrame, y_test: pd.Series):
        try:
            logger.info("Evaluating model")
            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test,y_pred)
            precision = precision_score(y_test,y_pred)
            recall = recall_score(y_test,y_pred)
            f1 = f1_score(y_test,y_pred)

            logger.info(f"Accuracy Score :: {accuracy}")
            logger.info(f"Precision Score :: {precision}")
            logger.info(f"Recall Score :: {recall}")
            logger.info(f"F1 Score :: {f1}")

            self.export_feature_list(X_test)

            return {
                "accuracy" : accuracy,
                "precision" : precision,
                "recall" : recall,
                "f1" : f1
            }


        except Exception as e:
            logger.error(f"Error while evaluating model : {e}")
            raise CustomException("Failed to evaluate model", e)


    def export_model(self, model: BaseEstimator):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)

            logger.info("Saving the model...")

            joblib.dump(model, self.model_output_path)

            logger.info(f"Model saved to {self.model_output_path}")

        except Exception as e:
            logger.error(f"Error while saving the model : {e}")
            raise CustomException("Failed to save model", e)
        


    def run(self):
        try:
            with mlflow.start_run():
                logger.info("Starting model training pipeline")

                logger.info("Starting MLFLOW Experimenttion")

                logger.info("Logging Training and Testing dataset to MLFLOW")
                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path="datasets")

                X_train, y_train, X_test, y_test = self.load_and_split_data()

                model = self.train_lgbm(X_train, y_train)

                metrics = self.evaluate_model(model, X_test, y_test)

                self.export_model(model)

                logger.info("Logging the model to MLFLOW")
                mlflow.log_artifact(self.model_output_path)

                logger.info("Logging Params and Metrics to MLFLOW")
                mlflow.log_params(model.get_params())
                mlflow.log_metrics(metrics)

                logger.info("Model training completed")
        except Exception as e:
            logger.error(f"Error while running the model training pipeline : {e}")
            raise CustomException("Failed to run the model training pipeline", e)
        

if __name__ == "__main__":

    trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)

    trainer.run()




