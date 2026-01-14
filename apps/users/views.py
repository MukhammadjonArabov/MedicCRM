from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets, filters, generics
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from apps.users.models import User, StaffSchedule, Patients
from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView
from django.contrib.auth.models import AnonymousUser
from apps.users.permissions import (
    IsAdmin,
    IsDoctorOrAdminOrRegisterOrNurse
)
from apps.users.serializers import (
    UserSerializer,
    LoginSerializer,
    RefreshTokenSerializer,
    UserListRetrieveSerializer,
    StaffScheduleSerializer,
    StaffScheduleCreateSerializer,
    TokenResponseSerializer,
    PatientListSerializer,
    PatientDetailSerializer,
    PatientCreateUpdateSerializer
)


# ================= AUTH =================


class BaseAPIView(GenericAPIView):
    def get_user(self):
        user = getattr(self.request, 'user', None)
        if isinstance(user, AnonymousUser):
            return None
        return user

    def get_user_role(self):
        user = self.get_user()
        return getattr(user, 'role', None)

    def is_swagger(self):
        return getattr(self, 'swagger_fake_view', False)
    

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: TokenResponseSerializer}
    )
    def post(self, request):
        if request.user and request.user.is_authenticated:
            return Response(
                {
                    "detail": "User already authenticated",
                    "user": {
                        "id": request.user.id,
                        "email": request.user.email,
                        "full_name": request.user.full_name,
                        "role": request.user.role,
                    }
                },
                status=status.HTTP_200_OK, 
            )
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response(
                {"detail": "Email or password is incorrect"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {"detail": "User is inactive"},
                status=status.HTTP_403_FORBIDDEN
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": user.role,
                }
            },
            status=status.HTTP_200_OK
        )


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


class DoctorListView(generics.ListAPIView):
    queryset = User.objects.filter(role='doctor')
    serializer_class = UserListRetrieveSerializer
    permission_classes = [permissions.IsAdminUser]


class StaffScheduleListView(BaseAPIView, generics.ListAPIView):
    serializer_class = StaffScheduleSerializer
    permission_classes = [IsDoctorOrAdminOrRegisterOrNurse]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['staff', 'staff__role', 'day']
    ordering_fields = ['day', 'start_time', 'staff__full_name']
    ordering = ['day', 'start_time']

    def get_queryset(self):
        if self.is_swagger():
            return StaffSchedule.objects.none()

        user = self.get_user()
        role = self.get_user_role()

        if not user:
            return StaffSchedule.objects.none()

        if role in ['doctor', 'nurse']:
            return StaffSchedule.objects.filter(staff=user)

        if role in ['admin', 'registrar']:
            return StaffSchedule.objects.filter(
                staff__role__in=['doctor', 'nurse']
            ).select_related('staff')

        return StaffSchedule.objects.none()


class StaffScheduleCreateView(generics.CreateAPIView):
    queryset = StaffSchedule.objects.all()
    serializer_class = StaffScheduleCreateSerializer
    permission_classes = [IsAdmin]


class StaffScheduleUpdateView(generics.UpdateAPIView):
    queryset = StaffSchedule.objects.all()
    serializer_class = StaffScheduleCreateSerializer
    permission_classes = [IsAdmin]

    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patients.objects.all()
    lookup_field = 'pk'
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['created_at', 'full_name']
    ordering = ['-created_at']
    search_fields = ['full_name', 'phone_number']

    def get_serializer_class(self):
        if getattr(self, 'swagger_fake_view', False):
            return PatientListSerializer

        if self.action in ['list', 'search']:
            return PatientListSerializer
        if self.action in ['retrieve', 'update', 'partial_update']:
            return PatientDetailSerializer
        return PatientCreateUpdateSerializer
