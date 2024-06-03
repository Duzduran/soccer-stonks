from kedro.pipeline import Pipeline, node
from .nodes import load_data, drop_duplicates, drop_unnecessary_columns, encode_and_transform, drop_correlated_columns, preprocess_data

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(load_data, "players_data", "raw_data"),
            node(drop_duplicates, "raw_data", "deduplicated_data"),
            node(drop_unnecessary_columns, "deduplicated_data", "data_with_dropped_columns"),
            node(encode_and_transform, "data_with_dropped_columns", "transformed_data"),
            node(preprocess_data, "transformed_data", "transformed_processed_data"),


            node(drop_correlated_columns, "transformed_processed_data", "preprocessed_players_data"),
        ]
    )
