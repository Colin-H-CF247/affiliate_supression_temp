from azureml.contrib.services.aml_response import AMLResponse
import pandas as pd
import traceback
import numpy as np
import json
from src.datascience_service.error_handling import InputError, ServiceError
from src.datascience_service.utils import score_dataframe, get_service_name


def init():
    global loaded_models
    loaded_models = {}


def run(payload):
    try:
        payload_df = (
            pd.read_json(payload, dtype=object)
            .set_index("index")
            .fillna(np.nan)
            .rename(index={"AppIdentifier": "ApplicationId"})
        ).T
        if "Model" not in payload_df.columns:
            raise InputError("Model column not in input payload")

        model_to_load = payload_df["Model"].values[0]

        payload_df.drop(columns=["Model"], inplace=True)

        model_confidence, output_prediction = score_dataframe(
            payload_df, model_to_load, loaded_models=loaded_models
        )
        # TODO: Handle statuses
        response = {
            "service": get_service_name(),
            "applicationId": str("Insert Application ID"),
            "score": float(model_confidence),
            "prediction": str(output_prediction),
            "scoreModel": model_to_load,
            "status": "PASS",
            "WARNINGS": "WARNINGS",
            "ERROR": traceback.format_exc(),
        }

        HTTPStatusCode = 200

    except ServiceError as err:
        HTTPStatusCode = 400

        response = {
            "service": get_service_name(),
            "applicationId": str(-1),
            "score": 0.0,
            "prediction": "Error",
            "scoreModel": model_to_load,
            "status": "FAIL",
            "WARNINGS": {},
            "ERROR": err.message,
            "traceback": traceback.format_exc(),
        }

    except Exception as modErr:
        print(modErr)
        response = {
            "service": get_service_name(),
            "applicationId": str(-1),
            "score": 0.0,
            "prediction": "Error",
            "scoreModel": "Error",
            "status": "FAIL",
            "WARNINGS": {},
            "ERROR": traceback.format_exc(),
        }
        HTTPStatusCode = 500
    finally:
        return AMLResponse(json.dumps([response]), HTTPStatusCode)
