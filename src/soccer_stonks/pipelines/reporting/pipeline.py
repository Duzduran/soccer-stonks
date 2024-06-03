from kedro.pipeline import Pipeline, node
from .nodes import generate_report, save_report

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(generate_report, "mae", "report"),
            node(save_report, ["report", "params:report_filepath"], None),
        ]
    )
