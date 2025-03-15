from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
from django.db import models
from data_news_api.models import Article, Feature, MLModel
from ml_news_classifier.models import MLExperiment, FeatureImportance
import joblib
import os
from django.utils import timezone


class RandomForestNewsClassifier:
    def __init__(self, n_estimators=100, max_depth=None):
        self.model = RandomForestClassifier(
            n_estimators=n_estimators, max_depth=max_depth, random_state=42
        )
        self.parameters = {"n_estimators": n_estimators, "max_depth": max_depth}

    def prepare_data(self, include_features=None, exclude_features=None):
        """
        Prepara los datos para el entrenamiento del modelo.
        """
        # Obtener artículos de entrenamiento con etiquetas conocidas
        training_articles = Article.objects.filter(
            in_training_set=True,
            label__in=[Article.TRUE, Article.FALSE]
        )

        # Verificar que hay suficientes datos
        if training_articles.count() < 10:
            raise ValueError("No hay suficientes artículos en el conjunto de entrenamiento.")

        # Obtener IDs de los artículos
        article_ids = list(training_articles.values_list('id', flat=True))

        # Obtener características de la base de datos
        features = Feature.objects.filter(article_id__in=article_ids)

        # Filtrar características según los parámetros
        if include_features:
            features = features.filter(feature_name__startswith=tuple(include_features))
        if exclude_features:
            features = features.exclude(feature_name__startswith=tuple(exclude_features))

        # Crear un DataFrame con las características
        df = pd.DataFrame(list(features.values('article_id', 'feature_name', 'feature_value')))
        X_df = df.pivot(index='article_id', columns='feature_name', values='feature_value').fillna(0)

        # Obtener etiquetas
        article_labels = {a.id: 1 if a.label == Article.TRUE else 0 for a in training_articles}
        y = np.array([article_labels[aid] for aid in X_df.index])

        return X_df.values, y, list(X_df.columns)

    def train(self, experiment_name, include_features=None, exclude_features=None):
        """
        Entrena el modelo Random Forest y guarda el experimento en la base de datos.
        """
        try:
            # Preparar datos
            X_df, y, feature_names = self.prepare_data(include_features, exclude_features)
            self.feature_names = feature_names

            # Crear experimento
            experiment = MLExperiment.objects.create(
                name=experiment_name,
                description=f"Random Forest con {len(feature_names)} características",
                algorithm_name="RandomForestClassifier",
                parameters={
                    "n_estimators": self.model.n_estimators,
                    "max_depth": self.model.max_depth,
                    "include_features": include_features,
                    "exclude_features": exclude_features,
                    "feature_names": feature_names,
                },
                created_at=timezone.now()
            )

            # experiment.parameters['feature_names'] = feature_names
            # experiment.save()
            
            # Entrenar modelo
            self.model.fit(X_df, y)

            # Guardar importancias de características
            importances = self.model.feature_importances_
            feature_importances = [
                FeatureImportance(
                    experiment=experiment, feature_name=name, importance=importance
                )
                for name, importance in zip(feature_names, importances) if importance > 0
            ]
            if feature_importances:
                FeatureImportance.objects.bulk_create(feature_importances)

            # Guardar modelo en un archivo
            model_path = f"ml_models/rf_{experiment.id}.joblib"
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            joblib.dump(self.model, model_path)

            # Crear registro de modelo
            ml_model = MLModel.objects.create(
                name=f"RandomForest-{experiment.id}",
                description=f"Random Forest classifier trained with {len(feature_names)} features",
                algorithm="random_forest",
                experiment=experiment,
                created_at=timezone.now()
            )

            # Asociar el archivo al modelo
            with open(model_path, 'rb') as f:
                ml_model.model_file.save(os.path.basename(model_path), f)

            # Asociar el modelo al experimento
            experiment.ml_model = ml_model
            experiment.save()

            return experiment

        except Exception as e:
            print(f"Error durante el entrenamiento de Random Forest: {e}")
            return None
            
    def load(self, model_id):
        """
        Carga un modelo entrenado desde la base de datos
        
        Args:
            model_id: ID del modelo a cargar
        """
        try:
            model_record = MLModel.objects.get(id=model_id)
        except MLModel.DoesNotExist:
            raise ValueError(f"No se encontró un modelo con ID {model_id}")
            
        if model_record.algorithm != 'random_forest':
            raise ValueError(f"El modelo con ID {model_id} no es un Random Forest")
            
        if model_record.model_file:
            self.model = joblib.load(model_record.model_file.path)
        else:
            model_path = f"ml_models/rf_{model_record.id}.joblib"
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
            else:
                raise FileNotFoundError(f"No se encontró el archivo del modelo: {model_path}")
                
        # Cargar los nombres de características del experimento
        experiment = model_record.experiment
        if experiment and 'feature_names' in experiment.parameters:
            self.feature_names = experiment.parameters['feature_names']
        else:
            print("Advertencia: No se encontraron los nombres de características en el experimento")
        
        self.model_id = model_id

    def predict(self, article):
        """
        Predice si un artículo es verdadero o falso
        
        Args:
            article: Objeto Article a predecir
            
        Returns:
            tuple: (label, confidence)
            - label: Article.TRUE o Article.FALSE
            - confidence: Valor entre 0 y 1
        """
        # Verificar que el modelo está cargado
        if self.model is None:
            raise ValueError("El modelo no está cargado. Usa load() o train() primero.")
        
        # Obtener características del artículo
        features = Feature.objects.filter(article=article)
        
        if not features.exists():
            raise ValueError(f"El artículo {article.id} no tiene características extraídas")
        
        # Convertir a diccionario
        feature_dict = {f.feature_name: f.feature_value for f in features}
        
        # Crear vector con las mismas características que se usaron en entrenamiento
        if not hasattr(self, 'feature_names') or not self.feature_names:
            raise ValueError("No se encontraron los nombres de características del modelo")
            
        # Crear vector de características en el mismo orden que se usó durante el entrenamiento
        X = np.zeros((1, len(self.feature_names)))
        for i, feature_name in enumerate(self.feature_names):
            X[0, i] = feature_dict.get(feature_name, 0)
            
        # Predecir
        proba = self.model.predict_proba(X)[0]
        
        # El índice 1 corresponde a la clase positiva (verdadero)
        confidence = proba[1]  
        predicted_label = Article.TRUE if confidence >= 0.5 else Article.FALSE
        
        return predicted_label, confidence
