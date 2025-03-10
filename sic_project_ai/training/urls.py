from django.urls import path
from .views import AgentsView, AiModelsView

class AgentsUrlsPatterns:
    urlPatterns = [
        path('actions-agent/list', AgentsView.get_all, name='get_all_agents'),
        path('actions-agent/create', AgentsView.create_agent, name='create_agent'),
        path('actions-agent/update/<int:pk>/', AgentsView.update_agent, name='update_agent'),
        path('actions-agent/delete/<int:pk>/', AgentsView.delete_agent, name='delete_agent'),
    ]

class ModelsUrlPatterns:
    urlpatterns = [
        path('actions-models/list', AiModelsView.get_all, name='get_all_models'),
        path('actions-models/create', AiModelsView.create_ai_model, name='create_model'),
        path('actions-models/update/<int:pk>/', AiModelsView.update_ai_model, name='update_model'),
        path('actions-models/delete/<int:pk>/', AiModelsView.delete_ai_model, name='delete_model'),
    ]
    