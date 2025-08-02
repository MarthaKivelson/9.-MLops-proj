from typing import Tuple
import sys

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from src.exception import MyException
from src.logger import logging
from src.utils.main_utils import load_object, load_numpy_array_data, save_object
from src.entity.config_entity import ModelTrainingConfig
from src.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact
from src.entity.estimator import MyModel

class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact, model_trainer_config: ModelTrainingConfig):
        """
        :param data_transformation_artifact: Output reference of data transformation artifact stage
        :param model_trainer_config: Configuration for model training
        """
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

    def get_model_obj_and_report(self, train:np.array, test:np.array)-> Tuple[object,object]:
        """
        Method Name :   get_model_object_and_report
        Description :   This function trains a RandomForestClassifier with specified parameters
        
        Output      :   Returns metric artifact object and trained model object
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            logging.info("Training RandomForestClassifier with specified parameters")

            #test train split
            xtrain, ytrain, xtest, ytest = train[:,:-1], train[:,-1], test[:,:-1], test[:,-1]
            logging.info("train test split done")

            model = RandomForestClassifier(
                n_estimators=self.model_trainer_config._n_estimators,
                criterion=self.model_trainer_config._criterion,
                min_samples_split=self.model_trainer_config._min_sample_split,
                min_samples_leaf=self.model_trainer_config._min_sample_leaf,
                max_depth=self.model_trainer_config._max_depth,
                random_state=self.model_trainer_config._randon_state
            )

            logging.info("Model training started")
            model.fit(xtrain, ytrain)
            logging.info("Model training done")

            #prediction
            y_pred = model.predict(xtest)
            accuracy = accuracy_score(ytest, y_pred)
            f1 = f1_score(ytest, y_pred)
            precision = precision_score(ytest, y_pred)
            recall = recall_score(ytest, y_pred)
            
            #creating metric artifact
            metrics_artifact = ClassificationMetricArtifact(f1_score=f1, precision_score=precision, recall_score=recall)
            return model, metrics_artifact
        
        except Exception as e:
            raise MyException(e, sys) from e
        
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        logging.info("In initiate_model_trainer method of ModelTrainer class ")
        """
        Method Name :   initiate_model_trainer
        Description :   This function initiates the model training steps
        
        Output      :   Returns model trainer artifact
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            print("------------------------------------------------------------------------------------------------")
            print("Starting Model Trainer Component")
            # Load transformed train and test data
            train_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)
            logging.info("Train test data loaded")

            # train model & get metrics
            trained_model, metrics_artifact = self.get_model_obj_and_report(train=train_arr, test=test_arr)
            logging.info("Model object and artifact loaded")

            #load preprocessor obj
            preprocessor_obj = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            logging.info("Preprocessor obj loaded")

            if accuracy_score(train_arr[:,-1],trained_model.predict(train_arr[:,:-1])) < self.model_trainer_config.expected_accuracy:
                logging.info("No model found with score above the base score")
                raise Exception("No model found with score above the base score")
            
            #save model
            logging.info("Saving the model as performance is better")
            my_model = MyModel(preprocessing_obj=preprocessor_obj, trained_model_obj=trained_model)
            save_object(self.model_trainer_config.trained_model_file_path, my_model)
            logging.info("Saved the final model obj with preprocessing & trained model")

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                metric_artifact=metrics_artifact
            )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise MyException(e, sys) from e