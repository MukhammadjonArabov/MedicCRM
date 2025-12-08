from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from apps.users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from apps.users.serializers import (
    UserSerializer, LoginSerializer, RefreshTokenSerializer, TokenSerializer, UserCreateSerializer
)

###  -------  Login  -------
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(tags=["Auth"], request_body=LoginSerializer, responses={200: TokenSerializer})
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({'error': 'Incorrect password'}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_active:
            return Response({'error': 'User account is inactive'}, status=status.HTTP_404_NOT_FOUND)

        refresh = RefreshToken.for_user(user)
        token_data = {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
        return Response(TokenSerializer(token_data).data)

###  -------  Logout  -------
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=["Auth"], request_body=RefreshTokenSerializer)
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data['refresh']

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Successfully logged out'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'detail': 'Failed to logout'}, status=status.HTTP_400_BAD_REQUEST)

###  -------  Refresh Token  -------
class RefreshView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(tags=["Auth"], request_body=RefreshTokenSerializer, responses={200: TokenSerializer})
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data['refresh']

        try:
            token = RefreshToken(refresh_token)
            access_data = {'access': str(token.access_token)}
            return Response(TokenSerializer(access_data).data)
        except Exception:
            return Response({'detail': 'Failed to refresh token'}, status=status.HTTP_400_BAD_REQUEST)

###  -------  User Info  -------
class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=["Users"])
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

### -------  User Register  -------
class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(tags=["Users"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

