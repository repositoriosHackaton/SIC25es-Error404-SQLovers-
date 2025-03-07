from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import agent_model
from .serializers import AgentModelSerializer

# Create your views here.

class agentView(APIView):
    def get(self, request):
        agents = agent_model.objects.all()
        serializer = AgentModelSerializer(agents, many=True)
        return Response({"agents": serializer.data})

    def post(self, request):
        agent = request.data.get('agent')
        # Create an article from the above data
        serializer = AgentModelSerializer(data=agent)
        if serializer.is_valid(raise_exception=True):
            agent_saved = serializer.save()
        return Response({"success": "Agent '{}' created successfully".format(agent_saved.agent_name)})

    def put(self, request, pk):
        saved_agent = get_object_or_404(agent_model.objects.all(), pk=pk)
        data = request.data.get('agent')
        serializer = AgentModelSerializer(instance=saved_agent, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            agent_saved = serializer.save()
        return Response({"success": "Agent '{}' updated successfully".format(agent_saved.agent_name)})

    def delete(self, request, pk):
        # Get object with this pk
        agent = get_object_or_404(agent_model.objects.all(), pk=pk)
        agent.delete()
        return Response({"message": "Agent with id `{}` has been deleted.".format(pk)},status=204)