from django.core.management.base import BaseCommand
import os
import pickle
from datasets.loader import load_dataset
from ml_models.processor import preprocess_text
from predictions.models import TrainingStats
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

class Command(BaseCommand):
    help = "Entrena los modelos de Machine Learning y los guarda en .pkl, además de registrar métricas en la BD."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("🔄 Iniciando proceso de entrenamiento..."))

        try:
            # 📌 Cargar el dataset
            self.stdout.write("🔄 Cargando datasets...")
            df = load_dataset()

            # 📌 Preprocesamiento del texto
            self.stdout.write("🔄 Preprocesando textos...")
            df["clean_text"] = df["text"].apply(preprocess_text)

            # 📌 División en conjunto de entrenamiento y prueba
            X = df["clean_text"]
            y = df["label"]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # 📌 Vectorización del texto
            self.stdout.write("🔄 Vectorizando texto...")
            vectorizer = CountVectorizer()
            X_train_dtm = vectorizer.fit_transform(X_train)
            X_test_dtm = vectorizer.transform(X_test)

            # 📌 Definimos los modelos a entrenar
            self.stdout.write("🔄 Entrenando modelos...")

            models = {
                "logistic": LogisticRegression(),
                "random_forest": RandomForestClassifier(random_state=42),
                "xgboost": XGBClassifier(),
                "naive_bayes": MultinomialNB(),
                "neural_network": MLPClassifier(hidden_layer_sizes=(100,), max_iter=500, random_state=42),
            }

            trained_models = {}
            model_stats = []

            for name, model in models.items():
                self.stdout.write(f"🚀 Entrenando {name}...")
                model.fit(X_train_dtm, y_train)

                # 📌 Evaluación del modelo
                y_pred = model.predict(X_test_dtm)
                accuracy = accuracy_score(y_test, y_pred)

                # 📌 Guardamos el modelo en memoria
                trained_models[name] = model

                # 📌 Guardamos la estadística del modelo
                model_stats.append(TrainingStats(model_name=name, accuracy=accuracy))

                self.stdout.write(self.style.SUCCESS(f"✅ {name} entrenado con precisión: {accuracy:.4f}"))

            # 📌 Guardar modelos y vectorizador en archivos .pkl
            save_path = os.path.join("ml_models")
            os.makedirs(save_path, exist_ok=True)

            self.stdout.write("💾 Guardando modelos entrenados...")
            pickle.dump(vectorizer, open(os.path.join(save_path, "vectorizer.pkl"), "wb"))

            for name, model in trained_models.items():
                pickle.dump(model, open(os.path.join(save_path, f"model_{name}.pkl"), "wb"))

            # 📌 Guardar estadísticas en la base de datos
            TrainingStats.objects.bulk_create(model_stats)

            self.stdout.write(self.style.SUCCESS("✅ Modelos entrenados y estadísticas guardadas con éxito."))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Error durante el entrenamiento: {str(e)}"))
