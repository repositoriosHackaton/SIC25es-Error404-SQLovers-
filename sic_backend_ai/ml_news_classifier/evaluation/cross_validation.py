from sklearn.model_selection import KFold
from data_news_api.models import Article, Feature
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def cross_validate(classifier, folds=5):
    """
    Realiza validación cruzada para un clasificador
    
    Args:
        classifier: Instancia de un clasificador (debe tener los métodos prepare_data y train)
        folds: Número de pliegues para validación cruzada
    
    Returns:
        Dict con métricas de evaluación
    """
    # Preparar datos
    X, y, feature_names = classifier.prepare_data()
    
    # Inicializar KFold
    kf = KFold(n_splits=folds, shuffle=True, random_state=42)
    
    # Variables para almacenar métricas
    accuracies = []
    precisions = []
    recalls = []
    f1_scores = []
    
    # Realizar validación cruzada
    for train_index, test_index in kf.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y[train_index], y[test_index]
        
        # Entrenar modelo
        classifier.model.fit(X_train, y_train)
        
        # Predecir
        y_pred = classifier.model.predict(X_test)
        
        # Calcular métricas
        accuracies.append(accuracy_score(y_test, y_pred))
        precisions.append(precision_score(y_test, y_pred, zero_division=0))
        recalls.append(recall_score(y_test, y_pred, zero_division=0))
        f1_scores.append(f1_score(y_test, y_pred, zero_division=0))
    
    # Resultados
    results = {
        'folds': folds,
        'accuracy_mean': np.mean(accuracies),
        'accuracy_std': np.std(accuracies),
        'precision_mean': np.mean(precisions),
        'precision_std': np.std(precisions),
        'recall_mean': np.mean(recalls),
        'recall_std': np.std(recalls),
        'f1_mean': np.mean(f1_scores),
        'f1_std': np.std(f1_scores),
        'accuracy_per_fold': accuracies,
        'precision_per_fold': precisions,
        'recall_per_fold': recalls,
        'f1_per_fold': f1_scores,
    }
    
    return results