import sys

import pandas as pd
from pandas import DataFrame
from sklearn.pipeline import Pipeline

from src.exception import MyException
from src.logger import logging

class TargetValueMapping:
    def __init__(self):
        self.yes: int = 0
        self.no: int = 1
    def _asdict(self):
        return self.__dict__
    def reverse_mapping(self):
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))
    

class MyModel:
    def __init__(self, preprocessing_obj: Pipeline, trained_model_obj: object):
        """
        :param preprocessing_object: Input Object of preprocesser
        :param trained_model_object: Input Object of trained model 
        """
        self.preprocessing_obj = preprocessing_obj
        self.trained_model_obj = trained_model_obj

    def predict(self, dataframe: pd.DataFrame)-> DataFrame:
        """
        Function accepts preprocessed inputs (with all custom transformations already applied),
        applies scaling using preprocessing_object, and performs prediction on transformed features.
        """
        try:
            logging.info("Starting prediction process")

            #apply scaling 
            transformed_features = self.preprocessing_obj.fit_transform(dataframe)

            #prediction using model
            logging.info("Using the trained model")
            predictions = self.trained_model_obj.predict(transformed_features)

            return predictions
        except Exception as e:
            raise MyException(e, sys) from e

    def __repr__(self):
        return f"{type(self.trained_model_obj).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_obj).__name__}()"            