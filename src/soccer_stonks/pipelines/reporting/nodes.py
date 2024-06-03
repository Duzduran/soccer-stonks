def generate_report(mae: float) -> str:
    report = f"Model Mean Absolute Error: {mae}"
    return report

def save_report(report: str, filepath: str):
    with open(filepath, 'w') as f:
        f.write(report)
