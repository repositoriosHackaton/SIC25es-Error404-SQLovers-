from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import agent_model
from .serializers import AgentModelSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

# Create your views here.

class AgentsView(APIView):
    
    @swagger_auto_schema(
        operation_description="GET method to get all agents from db", 
        tags=['Agents'], 
        method='GET'
        )
    @api_view(['GET'])
    def get_all(request):
        agents = agent_model.objects.all()
        serializer = AgentModelSerializer(agents, many=True)
        return Response({"agents": serializer.data})



    @swagger_auto_schema(
        operation_description="POST method to get a single agent from db", 
        tags=['Agents'], 
        method='POST'
        )
    @api_view(['POST'])
    def create_agent(request):
        agent = request.data.get('agent')
        serializer = AgentModelSerializer(data=agent)
        if serializer.is_valid(raise_exception=True):
            agent_saved = serializer.save()
        return Response({"success": "Agent '{}' created successfully".format(agent_saved.agent_name)})



    @swagger_auto_schema(
        operation_description="PUT method to get a single agent from db", 
        tags=['Agents'], 
        method='PUT',
        )
    @api_view(['PUT'])
    def update_agent(request, pk):
        saved_agent = get_object_or_404(agent_model.objects.all(), pk=pk)
        data = request.data.get('agent')
        serializer = AgentModelSerializer(instance=saved_agent, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            agent_saved = serializer.save()
        return Response({"success": "Agent '{}' updated successfully".format(agent_saved.agent_name)})



    @swagger_auto_schema(
        operation_description="DELETE method to get a single agent from db", 
        tags=['Agents'], 
        method='DELETE'
        )
    @api_view(['DELETE'])
    def delete_agent(request, pk):
        agent = get_object_or_404(agent_model.objects.all(), pk=pk)
        agent.delete()
        return Response({"message": "Agent with id `{}` has been deleted.".format(pk)},status=204)