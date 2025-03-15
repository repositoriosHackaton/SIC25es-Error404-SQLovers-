from data_news_api.models import Article, MLModel
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib
import pandas as pd
import numpy as np
import os
from django.db.models import Count, Q

def evaluate_model(model_id, X_test=None, y_true=None):
    """
    Evalúa un modelo entrenado con los artículos del conjunto de prueba.

    Args:
        model_id: ID del modelo a evaluar.
        X_test: Matriz de características de prueba (opcional).
        y_true: Etiquetas reales del conjunto de prueba (opcional).

    Returns:
        Dict con métricas de evaluación.
    """
    try:
        # Cargar el modelo
        model = MLModel.objects.get(id=model_id)
        model_path = model.model_file.path if model.model_file else f"ml_models/model_{model.id}.joblib"
        
        if not os.path.exists(model_path):
            print(f"No se encontró el archivo del modelo: {model_path}")
            return None
            
        clf = joblib.load(model_path)

        # Si no se proporcionan X_test o y_true, cargarlos desde la base de datos
        if X_test is None or y_true is None:
            # Obtener artículos de prueba
            test_articles = Article.objects.filter(
                in_test_set=True,
                features__isnull=False,
                label__in=[Article.TRUE, Article.FALSE]
            ).annotate(feature_count=Count('features')).filter(feature_count__gt=0).distinct()

            # Verificar que hay suficientes datos
            if test_articles.count() < 10:
                print(f"Muy pocos artículos de prueba con características: {test_articles.count()}")
                return None

            # Preparar datos para predicción
            article_ids = list(test_articles.values_list('id', flat=True))

            # Obtener características
            from data_news_api.models import Feature
            features = Feature.objects.filter(article__id__in=article_ids)

            # Verificar que hay características
            if not features.exists():
                print("No se encontraron características para los artículos de prueba")
                return None

            # Crear DataFrame
            df = pd.DataFrame(list(features.values('article_id', 'feature_name', 'feature_value')))
            X_test_df = df.pivot(index='article_id', columns='feature_name', values='feature_value').fillna(0)

            # Obtener etiquetas reales
            test_article_labels = {
                a.id: (1 if a.label == Article.TRUE else 0) 
                for a in test_articles
            }

            # Filtrar artículos que están en el DataFrame
            article_ids_with_features = list(X_test_df.index)
            y_true = np.array([test_article_labels[aid] for aid in article_ids_with_features if aid in test_article_labels])

            # Asegurar que tenemos todas las características que el modelo espera
            model_features = getattr(clf, 'feature_names_in_', None)

            if model_features is not None:
                # Añadir columnas faltantes con ceros
                for feature in model_features:
                    if feature not in X_test_df.columns:
                        X_test_df[feature] = 0

                # Ordenar columnas según el modelo
                X_test = X_test_df[model_features].values
            else:
                # Si no sabemos qué características espera el modelo, usamos todas
                X_test = X_test_df.values

        # Hacer predicciones
        try:
            y_pred = clf.predict(X_test)
        except Exception as e:
            print(f"Error al predecir: {str(e)}")
            return None

        # Calcular métricas
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        cm = confusion_matrix(y_true, y_pred)

        # Actualizar métricas en el modelo
        model.accuracy = accuracy
        model.precision = precision
        model.recall = recall
        model.f1_score = f1
        model.save()

        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'confusion_matrix': cm.tolist(),
            'num_test_samples': len(y_true)
        }

    except Exception as e:
        print(f"Error evaluando modelo: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return None