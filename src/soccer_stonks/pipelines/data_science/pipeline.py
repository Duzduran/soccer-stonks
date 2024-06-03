from kedro.pipeline import Pipeline, node
from .nodes import split_data, train_random_forest, evaluate_model

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(split_data, ["preprocessed_players_data", "params:test_size"], ["X_train", "X_test", "y_train", "y_test"]),
            node(train_random_forest, ["X_train", "y_train"], "model"),
            node(evaluate_model, ["model", "X_test", "y_test"], "mae"),
        ]
    )
