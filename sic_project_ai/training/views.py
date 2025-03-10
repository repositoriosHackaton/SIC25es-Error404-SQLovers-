from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import agent_model, AiModel
from .serializers import AgentModelSerializer, AiModelsSerializer
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

class AiModelsView(APIView):
    @swagger_auto_schema(
        operation_description="GET method to get all AI models from db", 
        tags=['AI Models'], 
        method='GET'
        )
    @api_view(['GET'])
    def get_all(request):
        ai_models = AiModel.objects.all()
        serializer = AiModelsSerializer(ai_models, many=True)
        return Response({"ai_models": serializer.data})

    @swagger_auto_schema(
        operation_description="POST method to get a single AI model from db", 
        tags=['AI Models'], 
        method='POST'
        )
    @api_view(['POST'])
    def create_ai_model(request):
        ai_model = request.data.get('ai_model')
        serializer = AiModelsSerializer(data=ai_model)
        if serializer.is_valid(raise_exception=True):
            ai_model_saved = serializer.save()
        return Response({"success": "AI model '{}' created successfully".format(ai_model_saved.ai_model_name)})

    @swagger_auto_schema(
        operation_description="PUT method to get a single AI model from db", 
        tags=['AI Models'], 
        method='PUT',
        )
    @api_view(['PUT'])
    def update_ai_model(request, pk):
        saved_ai_model = get_object_or_404(AiModel.objects.all(), pk=pk)
        data = request.data.get('ai_model')
        serializer = AiModelsSerializer(instance=saved_ai_model, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            ai_model_saved = serializer.save()
        return Response({"success": "AI model '{}' updated successfully".format(ai_model_saved.ai_model_name)})

    @swagger_auto_schema(
        operation_description="DELETE method to get a single AI model from db", 
        tags=['AI Models'], 
        method='DELETE'
        )
    @api_view(['DELETE'])
    def delete_ai_model(request, pk):
        ai_model = get_object_or_404(AiModel.objects.all(), pk=pk)
        ai_model.delete()
        return Response({"message": "AI model with id `{}` has been deleted.".format(pk)},status=204)    