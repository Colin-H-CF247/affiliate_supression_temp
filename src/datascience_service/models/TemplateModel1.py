from ..error_handling import ModelError
from datascience_core.modelling import MLFlowManager
import mlflow
from ..utils import load_config_yaml


class Model:
    registered_model_name = "template_model"
    registered_model_version = 4
    model = None

    def __init__(self):
        pass

    def load_model(self):
        if self.model is not None:
            return

        config = load_config_yaml()

        experiment_name = "no_using_for_saving"
        save_path = "not_using_for_saving"

        mlflow_manager = MLFlowManager(
            config["ml_studio_name"],
            config["subscription_id"],
            config["resource_group"],
            experiment_name,
            save_path,
        )

        mlflow_manager._initialise_ml_flow()

        model_uri = (
            f"models:/{self.registered_model_name}/{self.registered_model_version}"
        )
        self.model = mlflow.sklearn.load_model(model_uri=model_uri)

    def preprocess(self, df):
        if self.model is None:
            raise ModelError("Model not loaded")
        if "AveRooms" not in df.columns:
            raise ModelError("Field1 column not in input payload")
        return df

    def make_prediction(self, df):
        if self.model is None:
            raise ModelError("Model not loaded")
        return self.model.predict(df)

    def postprocess(self, df, model_confidence_score):
        if self.model is None:
            raise ModelError("Model not loaded")
        return model_confidence_score
