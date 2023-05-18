# Should call the the model in the same way as score.py
import pandas as pd
from utils import score_dataframe


def init():
    pass


def run(files):
    """
    Entry point for the batch endpoint

    Args:
        files (list): list of files to be scored

    Returns:
        results (pd.DataFrame): results of the scoring
    """
    results = pd.DataFrame()
    for data_file in files:
        data = pd.read_csv(data_file)
        if "models_to_score" not in data.columns:
            raise Exception(
                f"models_to_score column is not present in the data file {data_file}. It must contain a comma seperated string of model versions to score"  # noqa: E501
            )
        model_names = data["models_to_score"].values[0].split(",")
        data.drop(columns=["models_to_score"], inplace=True)
        mini_batch_results = data[["ApplicationId"]]
        for model_name in model_names:
            confidences, mapped_confidences = score_dataframe(data, model_name)
            mini_batch_results[f"{model_name}.raw_score"] = confidences
            mini_batch_results[f"{model_name}.mapped_score"] = mapped_confidences
        results = pd.concat([results, mini_batch_results])
    return results
