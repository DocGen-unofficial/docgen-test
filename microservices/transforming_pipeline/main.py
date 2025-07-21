from transforming_pipeline import normalization, standardization, anonymization, etc

pipeline_steps = {
    "normalization": normalization.run,
    "standardization": standardization.run,
    "anonymization": anonymization.run,
    # altre fasi della pipeline, dove ogni fase e` una classe ad esempio
}

def run_pipeline(data, selected_steps):
    for step in selected_steps:
        if step in pipeline_steps:
            data = pipeline_steps[step](data)
    return data