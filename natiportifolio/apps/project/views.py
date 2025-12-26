# apps/experience/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.project.serializers import ProjectSerializer
from .models import Project
from .serializers import ProjectSerializer
from apps.users.models import User

# -------------------------
# Helper: check token from headers
# -------------------------
def get_user_from_token(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None, Response({'error': 'Authorization header missing'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        prefix, token = auth_header.split(' ')
        if prefix != 'Token':
            return None, Response({'error': 'Invalid token prefix'}, status=status.HTTP_401_UNAUTHORIZED)
    except ValueError:
        return None, Response({'error': 'Invalid authorization header'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        user = User.objects.get(reset_token=token)
        return user, None
    except User.DoesNotExist:
        return None, Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

# -------------------------
# List & Create Experiences
# -------------------------
class ProjectListCreate(APIView):

    def get(self, request):
        user, error = get_user_from_token(request)
        if error:
            return error  # token invalid, return 401

        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        user, error = get_user_from_token(request)
        if error:
            return error  # token invalid, return 401

        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)  # assign user from token
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------------------------
# Retrieve, Update & Delete
# -------------------------
class ProjectRetrieveUpdateDelete(APIView):

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return None

    def get(self, request, pk):
        user, error = get_user_from_token(request)
        if error:
            return error

        project = self.get_object(pk)
        if not project:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        user, error = get_user_from_token(request)
        if error:
            return error

        project = self.get_object(pk)
        if not project:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user, error = get_user_from_token(request)
        if error:
            return error

        experience = self.get_object(pk)
        if not experience:
            return Response({'error': 'Experience not found'}, status=status.HTTP_404_NOT_FOUND)

        experience.delete()
        return Response({'message': 'Experience deleted'}, status=status.HTTP_204_NO_CONTENT)
