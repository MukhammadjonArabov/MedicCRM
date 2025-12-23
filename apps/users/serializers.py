from rest_framework import serializers
from apps.users.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField(required=False)


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
