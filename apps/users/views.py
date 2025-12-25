from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets, filters, generics
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from apps.users.permissions import IsAdmin, IsDoctorOrAdminOrRegister
from apps.users.models import User, StaffSchedule
from apps.users.serializers import (
    UserSerializer,
    LoginSerializer,
    RefreshTokenSerializer,
    TokenSerializer,
    UserListRetrieveSerializer, StaffScheduleSerializer,
)


# ================= AUTH =================

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer, responses={200: TokenSerializer})
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not user.check_password(password):
            return Response(
                {"detail": "Invalid password"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.is_active:
            return Response(
                {"detail": "User is inactive"},
                status=status.HTTP_403_FORBIDDEN
            )

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=RefreshTokenSerializer)
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            token = RefreshToken(serializer.validated_data['refresh'])
            token.blacklist()
            return Response({"detail": "Logged out successfully"})
        except Exception:
            return Response(
                {"detail": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )


class RefreshView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=RefreshTokenSerializer)
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            token = RefreshToken(serializer.validated_data['refresh'])
            return Response({
                "access": str(token.access_token)
            })
        except Exception:
            return Response(
                {"detail": "Invalid refresh token"},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        serializer = UserListRetrieveSerializer(request.user)
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdmin]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['role', 'is_active']
    search_fields = ['full_name', 'email', 'phone_number', 'descriptor']
    ordering_fields = ['full_name', 'email', 'role']
    ordering = ['full_name']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UserListRetrieveSerializer
        return UserSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class DoctorListView(generics.ListAPIView):
    queryset = User.objects.filter(role='doctor')
    serializer_class = UserListRetrieveSerializer
    permission_classes = [permissions.IsAdminUser]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class StaffScheduleListView(generics.ListAPIView):
    serializer_class = StaffScheduleSerializer
    permission_classes = [IsDoctorOrAdminOrRegister]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['staff', 'staff__role', 'day']
    ordering_fields = ['day', 'start_time', 'staff__full_name']
    ordering = ['day', 'start_time']

    def get_queryset(self):
        user = self.request.user

        if user.role in ['doctor', 'nurse']:
            return StaffSchedule.objects.filter(staff=user)

        elif user.role in ['admin', 'registrar',]:
            return StaffSchedule.objects.filter(
                staff__role__in=['doctor', 'nurse']
            ).select_related('staff')

        return StaffSchedule.objects.none()

