from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics, viewsets
from apps.users.models import User
from rest_framework import generics, filters
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from apps.users.permissions import IsAdmin
from django_filters.rest_framework import DjangoFilterBackend
from apps.users.serializers import (
    UserSerializer, LoginSerializer, RefreshTokenSerializer, TokenSerializer, UserListRetrieveSerializer
)

class LoginView(APIView):
    """
    Login
    """
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

class LogoutView(APIView):
    """
    Logout
    """
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


class RefreshView(APIView):
    """
    Refresh Token
    """
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

class UserView(APIView):
    """
    User Info
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=["Users"])
    def get(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response(
                {'error': 'User does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserListRetrieveSerializer(request.user)
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    """
     User CRUD API
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_active']
    search_fields = ['full_name', 'email', 'phone_number', 'descriptor']
    ordering_fields = ['full_name', 'email', 'role']
    ordering = ['full_name']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UserListRetrieveSerializer
        return UserSerializer

    @swagger_auto_schema(tags=["Users"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Users"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Users"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Users"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Users"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Users"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)