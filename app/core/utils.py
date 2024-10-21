import joblib

def load_model(model_path):
    """Load the pre-trained machine learning model."""
    return joblib.load(model_path)
