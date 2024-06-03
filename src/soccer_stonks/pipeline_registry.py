from typing import Dict
from kedro.pipeline import Pipeline
from soccer_stonks.pipelines.data_processing import pipeline as data_processing_pipeline
from soccer_stonks.pipelines.data_science import pipeline as data_science_pipeline
from soccer_stonks.pipelines.reporting import pipeline as reporting_pipeline

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    data_processing = data_processing_pipeline.create_pipeline()
    data_science = data_science_pipeline.create_pipeline()
    reporting = reporting_pipeline.create_pipeline()

    pipelines = {
        "data_processing": data_processing,
        "data_science": data_science,
        "reporting": reporting,
    }

    pipelines["__default__"] = data_processing + data_science + reporting
    return pipelines
