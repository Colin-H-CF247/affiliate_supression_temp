from datascience_service.models.TemplateModel1 import Model
from sklearn import datasets
from datascience_core.data_retrieval import ProjectDatasetManager
import pandas as pd


def sklearn_to_df(sklearn_dataset):
    df = pd.DataFrame(sklearn_dataset.data, columns=sklearn_dataset.feature_names)
    return df


class TestModel:
    def test_predict(self):
        sklean_dataset = datasets.fetch_california_housing()
        boston_df = sklearn_to_df(sklean_dataset)
        model = Model()
        model.load_model()
        result = model.make_prediction(boston_df)
        assert result.shape[0] == boston_df.shape[0]

    def test_preprocess(self):
        pass

    def test_postprocess(self):
        pass

    def test_load_model(self):
        model = Model()
        model.load_model()
        assert model.model is not None
