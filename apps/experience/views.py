# apps/experience/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Experience
from .serializers import ExperienceSerializer
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
class ExperienceListCreate(APIView):

    def get(self, request):
        # GET is public
        experiences = Experience.objects.all()
        serializer = ExperienceSerializer(experiences, many=True)
        return Response(serializer.data)

    def post(self, request):
        # POST requires token
        user, error = get_user_from_token(request)
        if error:
            return error

        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------------------------
# Retrieve, Update & Delete
# -------------------------
class ExperienceRetrieveUpdateDelete(APIView):

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            return None

    def get(self, request, pk):
        # GET is public
        experience = self.get_object(pk)
        if not experience:
            return Response({'error': 'Experience not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExperienceSerializer(experience)
        return Response(serializer.data)

    def put(self, request, pk):
        # PUT requires token
        user, error = get_user_from_token(request)
        if error:
            return error

        experience = self.get_object(pk)
        if not experience:
            return Response({'error': 'Experience not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExperienceSerializer(experience, data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # DELETE requires token
        user, error = get_user_from_token(request)
        if error:
            return error

        experience = self.get_object(pk)
        if not experience:
            return Response({'error': 'Experience not found'}, status=status.HTTP_404_NOT_FOUND)

        experience.delete()
        return Response({'message': 'Experience deleted'}, status=status.HTTP_204_NO_CONTENT)
