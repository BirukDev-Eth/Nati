from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Education
from .serializers import EducationSerializer
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
# List & Create Education
# -------------------------
class EducationListCreate(APIView):

    def get(self, request):
        user, error = get_user_from_token(request)
        if error:
            return error

        educations = Education.objects.filter(user=user)
        serializer = EducationSerializer(educations, many=True)
        return Response(serializer.data)

    def post(self, request):
        user, error = get_user_from_token(request)
        if error:
            return error

        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------------------------
# Retrieve, Update & Delete Education
# -------------------------
class EducationRetrieveUpdateDelete(APIView):

    def get_object(self, pk):
        try:
            return Education.objects.get(pk=pk)
        except Education.DoesNotExist:
            return None

    def get(self, request, pk):
        user, error = get_user_from_token(request)
        if error:
            return error

        education = self.get_object(pk)
        if not education or education.user != user:
            return Response({'error': 'Education not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EducationSerializer(education)
        return Response(serializer.data)

    def put(self, request, pk):
        user, error = get_user_from_token(request)
        if error:
            return error

        education = self.get_object(pk)
        if not education or education.user != user:
            return Response({'error': 'Education not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EducationSerializer(education, data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user, error = get_user_from_token(request)
        if error:
            return error

        education = self.get_object(pk)
        if not education or education.user != user:
            return Response({'error': 'Education not found'}, status=status.HTTP_404_NOT_FOUND)

        education.delete()
        return Response({'message': 'Education deleted'}, status=status.HTTP_204_NO_CONTENT)
