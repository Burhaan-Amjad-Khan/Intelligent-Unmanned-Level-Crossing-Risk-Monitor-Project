def alert_description(assessment, source_label):
    return f"{assessment.state}: {assessment.reason} Input source: {source_label}."
