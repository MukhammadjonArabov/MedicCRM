from rest_framework import serializers
from apps.users.models import User, StaffSchedule


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})


class TokenResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    user = serializers.SerializerMethodField(read_only=True)

    def get_user(self, obj):
        return {
            "id": 0,
            "email": "string",
            "full_name": "string",
            "role": "string"
        }


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = [
            'id', 'email', 'password', 'full_name', 'role',
            'phone_number', 'descriptor', 'image_user',
            'is_active', 'is_staff', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_staff', 'created_at', 'updated_at']

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)

        if user.role == 'admin':
            user.is_staff = True

        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        if 'role' in validated_data:
            instance.is_staff = instance.role == 'admin'

        instance.save()
        return instance


class UserListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'role', 'phone_number', 'descriptor', 'image_user']


class StaffScheduleSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.full_name', read_only=True)
    staff_role = serializers.CharField(source='staff.get_role_display', read_only=True)
    staff_id = serializers.IntegerField(source='staff.id', read_only=True)
    day_display = serializers.CharField(source='get_day_display', read_only=True)

    class Meta:
        model = StaffSchedule
        fields = [
            'id', 'staff_id', 'staff_name', 'staff_role',
            'day', 'day_display', 'start_time', 'end_time'
        ]
        read_only_fields = ['staff_name', 'staff_role', 'day_display']

class StaffScheduleCreateSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.full_name', read_only=True)
    day_display = serializers.CharField(source='get_day_display', read_only=True)

    class Meta:
        model = StaffSchedule
        fields = [
            'id', 'staff', 'staff_name',
            'day', 'day_display', 'start_time', 'end_time'
        ]
        read_only_fields = ['staff_name', 'day_display']

    def validate(self, data):
        if data['start_time'] > data['end_time']:
            raise serializers.ValidationError(
                'Start time > End time'
            )
        return data