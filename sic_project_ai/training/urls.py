from django.urls import path
from .views import AgentsView

class AgentsUrlsPatterns:
    urlPatterns = [
        path('services/agents/list/', AgentsView.get_all, name='get_all_agents'),
        path('services/agents/create/', AgentsView.create_agent, name='create_agent'),
        path('services/agents/update/<int:id>/', AgentsView.update_agent, name='update_agent'),
        path('services/agents/delete/<int:id>/', AgentsView.delete_agent, name='delete_agent'),
    ]