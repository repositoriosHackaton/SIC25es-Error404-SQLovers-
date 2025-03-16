from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ml_models.models import MODELS, VECTORIZER
from ml_models.processor import preprocess_text
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import PredictNewsSerializer
from predictions.models import Prediction, TrainingStats
import time


class PredictNewsView(APIView):
    @swagger_auto_schema(
        operation_description="Predice si una noticia es falsa o real usando el modelo por defecto (logistic).",
        request_body=PredictNewsSerializer,
        tags=['Predictions (default model)'],  # Agrega la etiqueta "Predictions" a la documentación
    )
    def post(self, request):
        serializer = PredictNewsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        text = serializer.validated_data["text"]
        model = MODELS.get("logistic")

        clean_text = preprocess_text(text)
        text_vectorized = VECTORIZER.transform([clean_text])
        prediction = model.predict(text_vectorized)[0]
        prediction_label = "Fake" if prediction == 1 else "Real"

        
        Prediction.objects.create(
            text=text,
            prediction=prediction_label,
            model_used="logistic"
        )
        print("✅ Predicción guardada en la base de datos.")

        return Response(
            {"prediction": "Fake" if prediction == 1 else "Real"},
            status=status.HTTP_200_OK,
        )

class PredictWithModelView(APIView):
    @swagger_auto_schema(
        operation_description="Predice si una noticia es falsa o real usando un modelo específico.",
        manual_parameters=[
            openapi.Parameter(
                "model_type",
                openapi.IN_PATH,
                description=f"Tipo de modelo a usar. Opciones válidas: {', '.join(MODELS.keys())}",
                type=openapi.TYPE_STRING,
                enum=list(MODELS.keys()),
            )
        ],
        tags=['Predictions (specific model)'],  
        request_body=PredictNewsSerializer,
    )
    def post(self, request, model_type):
        serializer = PredictNewsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        text = serializer.validated_data["text"]
        model = MODELS.get(model_type)
        if not model:
            return Response(
                {"error": f"Invalid model type. Valid options are: {', '.join(MODELS.keys())}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        clean_text = preprocess_text(text)
        text_vectorized = VECTORIZER.transform([clean_text])
        prediction = model.predict(text_vectorized)[0]
        prediction_label = "Fake" if prediction == 1 else "Real"

        # Guardar la predicción en la base de datos
        Prediction.objects.create(
            text=text,
            prediction=prediction_label,
            model_used=model_type
        )
        print("✅ Predicción guardada en la base de datos.")

        return Response(
            {"prediction": "Fake" if prediction == 1 else "Real"},
            status=status.HTTP_200_OK,
        )

class InsightsView(APIView):
    @swagger_auto_schema(
        operation_description="Devuelve estadísticas generales de las predicciones y los modelos entrenados.",
        tags=["Stats"],  # Agrega la etiqueta "stats" a la documentación
    )
    def get(self, request):
        # Cantidad total de predicciones
        total_predictions = Prediction.objects.count()

        real_count = Prediction.objects.filter(prediction="Real").count()
        fake_count = Prediction.objects.filter(prediction="Fake").count()

        last_predictions = Prediction.objects.order_by("-created_at")[:5].values("text", "prediction", "model_used", "created_at")

        model_stats = TrainingStats.objects.all().values("model_name", "accuracy", "trained_at")

        return Response({
            "total_predictions": total_predictions,
            "real_count": real_count,
            "fake_count": fake_count,
            "last_predictions": list(last_predictions),
            "model_stats": list(model_stats),
        }, status=status.HTTP_200_OK)

class ModelStatsView(APIView):
    @swagger_auto_schema(
        operation_description="Devuelve estadísticas específicas de un modelo.",
        manual_parameters=[
            openapi.Parameter(
                "model_name",
                openapi.IN_PATH,
                description=f"Nombre del modelo. Opciones válidas: {', '.join(MODELS.keys())}",
                type=openapi.TYPE_STRING,
                enum=list(MODELS.keys()),  # Enumera las opciones válidas
            )
        ],
        tags=["Model Stats by name"],  # Agrega la etiqueta "stats" a la documentación
    )
    def get(self, request, model_name):
        # Buscar estadísticas del modelo en la base de datos
        stats = TrainingStats.objects.filter(model_name=model_name).first()
        if not stats:
            return Response(
                {"error": "Model not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Devolver las estadísticas del modelo
        return Response(
            {
                "model_name": stats.model_name,
                "accuracy": stats.accuracy,
                "trained_at": stats.trained_at,
            },
            status=status.HTTP_200_OK,
        )

class PredictWithAllModelsView(APIView):
    @swagger_auto_schema(
        operation_description="Evalúa una noticia con todos los modelos disponibles y devuelve un promedio ponderado.",
        request_body=PredictNewsSerializer,
        tags=["Predictions (all models)"],
    )
    def post(self, request):
        serializer = PredictNewsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        text = serializer.validated_data["text"]
        clean_text = preprocess_text(text)
        text_vectorized = VECTORIZER.transform([clean_text])

        predictions = {}
        weighted_sum = 0
        total_weight = 0

        # Evaluar con todos los modelos
        for model_name, model in MODELS.items():
            if model is None:
                continue  # Saltar modelos no cargados

            # Obtener precisión del modelo desde la base de datos
            stats = TrainingStats.objects.filter(model_name=model_name).first()
            accuracy = stats.accuracy if stats else 0

            # Medir el tiempo de predicción
            start_time = time.time()
            prediction = model.predict(text_vectorized)[0]
            end_time = time.time()
            prediction_time = round(end_time - start_time, 4)  # Tiempo en segundos

            prediction_label = "Fake" if prediction == 1 else "Real"

            # Guardar predicción en la base de datos
            Prediction.objects.create(
                text=text,
                prediction=prediction_label,
                model_used=model_name
            )
            print(f"✅ Predicción guardada para el modelo {model_name}.")

            # Guardar detalles de la predicción
            predictions[model_name] = {
                "prediction": prediction_label,
                "accuracy": accuracy,
                "prediction_time": prediction_time,  # Tiempo de predicción
            }

            # Calcular promedio ponderado
            weighted_sum += accuracy * prediction  # prediction será 1 para "Fake" y 0 para "Real"
            total_weight += accuracy

        # Calcular predicción final basada en el promedio ponderado
        final_score = weighted_sum / total_weight if total_weight > 0 else 0
        final_prediction = "Fake" if final_score >= 0.5 else "Real"

        # Calcular confianza como la proporción de votos ponderados
        confidence = final_score if final_prediction == "Fake" else 1 - final_score

        return Response(
            {
                "predictions": predictions,
                "final_prediction": final_prediction,
                "confidence": round(confidence, 4),
            },
            status=status.HTTP_200_OK,
        )