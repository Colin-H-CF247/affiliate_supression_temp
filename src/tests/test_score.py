import os
import json
import requests
from .test_data import test_path
import os
import time
import pandas as pd
import numpy as np
import sys
import subprocess
import time

MODELS_TO_TEST = ["TemplateModel1"]


class Test200Codes:
    """
    start the inference server running from local_azure_env:
    azmlinfsrv --entry_script code\deploy\score.py --model_dir models
    """

    def test_payload_status_pass(self):
        for model in MODELS_TO_TEST:
            with open(os.path.join(test_path, "example_payload.json")) as f:
                payload_test = json.dumps(json.load(f))
            payload_test = payload_test.replace("model_name", model)
            resp = requests.post("http://127.0.0.1:5001/score", payload_test)
            msg = resp.text
            assert bool(resp)
            assert json.loads(msg)[0]["status"] == "PASS"


class Test400Codes:
    """
    start the inference server running from local_azure_env:
    azmlinfsrv --entry_script code\deploy\score.py --model_dir models
    """

    def test_model_not_exists_error(self):
        for model in MODELS_TO_TEST:
            with open(os.path.join(test_path, "example_payload.json")) as f:
                payload_test = json.dumps(json.load(f))
            payload_test = payload_test.replace("model_name", "fake_model_name")
            resp = requests.post("http://127.0.0.1:5001/score", payload_test)
            assert not bool(resp)
            assert resp.status_code == 400

    def test_payload_status_error(self):
        for model in MODELS_TO_TEST:
            with open(os.path.join(test_path, "example_payload.json")) as f:
                payload_test = json.dumps(json.load(f))
            payload_test = payload_test.replace("model_name", model)
            payload_test = payload_test.replace("AveRooms", "Incorrect_field_name")
            resp = requests.post("http://127.0.0.1:5001/score", payload_test)
            msg = resp.text

            assert not bool(resp)
            assert json.loads(msg)[0]["ERROR"] == "Field1 column not in input payload"
