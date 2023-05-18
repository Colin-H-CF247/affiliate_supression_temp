import yaml
import pandas as pd
import os
from importlib import import_module
from .error_handling import InputError

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")


def get_named_model(model_name: str, loaded_models: dict = None) -> object:
    model_name = handle_model_name(model_name)

    if loaded_models is not None:
        model = loaded_models.get(model_name)
    else:
        model = None

    if model is None:
        try:
            module = import_module(
                "src.datascience_service.models." + model_name,
            )
        except ModuleNotFoundError:
            raise InputError("Model " + model_name + "does not exist")
        model = module.Model()
        if loaded_models is not None:
            loaded_models[model_name] = model

    return model


def handle_model_name(model_name):
    if model_name == "live":
        model_name = get_live_model()
    return model_name


def score_dataframe(df: pd.DataFrame, model_to_load: str, loaded_models: dict = {}):
    model = get_named_model(model_to_load, loaded_models=loaded_models)
    model.load_model()
    processed_payload = model.preprocess(df)
    model_confidence_score = model.make_prediction(processed_payload)
    output_prediction = model.postprocess(model_confidence_score, processed_payload)
    return model_confidence_score, output_prediction


def load_config_yaml():
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)
    return config


def get_live_model():
    config = load_config_yaml()
    return config["live_model"]


def get_service_name():
    config = load_config_yaml()
    return config["service_name"]
