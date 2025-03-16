import pickle
import os
from django.conf import settings

MODELS_PATH = os.path.join(settings.BASE_DIR, "ml_models/")

def safe_load_model(file_path):
    try:
        with open(file_path, "rb") as f:
            return pickle.load(f)
    except (EOFError, FileNotFoundError, pickle.UnpicklingError) as e:
        print(f"Error loading model from {file_path}: {e}")
        return None

MODELS = {
    "logistic": safe_load_model(os.path.join(MODELS_PATH, "model_logistic.pkl")),
    "random_forest": safe_load_model(os.path.join(MODELS_PATH, "model_random_forest.pkl")),
    "xgboost": safe_load_model(os.path.join(MODELS_PATH, "model_xgboost.pkl")),
    "naive_bayes": safe_load_model(os.path.join(MODELS_PATH, "model_naive_bayes.pkl")),
    "neural_network": safe_load_model(os.path.join(MODELS_PATH, "model_neural_network.pkl")),
}

# Cargar vectorizador de texto
VECTORIZER = safe_load_model(os.path.join(MODELS_PATH, "vectorizer.pkl"))