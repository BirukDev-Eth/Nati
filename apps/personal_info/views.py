# apps/experience/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import personal_info
from .serializers import PersonalInfoSerializer
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
# List & Create Experiences / Personal Info
# -------------------------
class PersonalInfoListCreate(APIView):

    def get(self, request):
        # GET is public, no token required
        personalInfos = personal_info.objects.all()
        serializer = PersonalInfoSerializer(personalInfos, many=True)
        return Response(serializer.data)

    def post(self, request):
        # POST requires token
        user, error = get_user_from_token(request)
        if error:
            return error

        serializer = PersonalInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------------------------
# Retrieve, Update & Delete
# -------------------------
class PersonalInfoRetrieveUpdateDelete(APIView):

    def get_object(self, pk):
        try:
            return personal_info.objects.get(pk=pk)
        except personal_info.DoesNotExist:
            return None

    def get(self, request, pk):
        # GET is public, no token required
        personalInfo = self.get_object(pk)
        if not personalInfo:
            return Response({'error': 'PersonalInfo not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PersonalInfoSerializer(personalInfo)
        return Response(serializer.data)

    def put(self, request, pk):
        # PUT requires token
        user, error = get_user_from_token(request)
        if error:
            return error

        personalInfo = self.get_object(pk)
        if not personalInfo:
            return Response({'error': 'PersonalInfo not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PersonalInfoSerializer(personalInfo, data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # DELETE requires token
        user, error = get_user_from_token(request)
        if error:
            return error

        personalInfo = self.get_object(pk)
        if not personalInfo:
            return Response({'error': 'PersonalInfo not found'}, status=status.HTTP_404_NOT_FOUND)

        personalInfo.delete()
        return Response({'message': 'PersonalInfo deleted'}, status=status.HTTP_204_NO_CONTENT)
