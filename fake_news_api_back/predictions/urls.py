from django.urls import path
from .views import PredictNewsView, PredictWithModelView, InsightsView, ModelStatsView, PredictWithAllModelsView, analyze_article_by_url
from .views import PredictFromImageView  

urlpatterns = [
    path("predict/v1/api/ai/default", PredictNewsView.as_view(), name="predict"),
    path("predict/v1/api/ai/custom-type/<str:model_type>/", PredictWithModelView.as_view(), name="predict_with_model"),
    path("stats/v1/api/ai/generals", InsightsView.as_view(), name="stats"),
    path("stats/v1/api/ai/custom-model/<str:model_name>/", ModelStatsView.as_view(), name="model_stats"),  # Nueva ruta
    path("predict/advanced/v1/ai/full-featured", PredictWithAllModelsView.as_view(), name="predict_with_all_models"),  # Nueva ruta
    path("predict/v1/api/ai/image", PredictFromImageView.as_view(), name="predict_from_image"),
    path('analyze-url/', analyze_article_by_url, name='analyze_article_by_url'),
]