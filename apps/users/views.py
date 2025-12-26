from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserCreateSerializer, PasswordResetRequestSerializer, PasswordResetSerializer

# -------------------------
# Register User
# -------------------------
class RegisterView(APIView):
    permission_classes = [AllowAny]  # <-- public access

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created', 'email': user.email}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------------------------
# Request Password Reset
# -------------------------
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]  # <-- public access

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.fetch_by_email(email)
            if not user:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            token = user.generate_token()
            # Optionally, send token via email here
            return Response({'message': 'Token generated', 'token': token})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------------------------
# Reset Password
# -------------------------
class PasswordResetView(APIView):
    permission_classes = [AllowAny]  # <-- public access

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            user = User.fetch_by_email(email)
            if not user:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            if user.reset_password(token, new_password):
                return Response({'message': 'Password reset successful'})
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------------------------
# Login User
# -------------------------
class LoginView(APIView):
    permission_classes = [AllowAny]  # <-- public access

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.fetch_by_email(email)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate token (currently using reset_token logic)
        token = user.generate_token() if hasattr(user, 'generate_token') else None

        return Response({
            'message': 'Login successful',
            'email': user.email,
            'token': token
        })
