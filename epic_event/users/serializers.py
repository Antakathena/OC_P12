from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta:
        model = CustomUser
        fields = ('id', 'team', 'email', 'first_name', 'last_name', 'username',
                  'date_joined', 'password',)

        extra_kwargs = {'password': {'write_only': True}}


class RegisterUserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()
    team = serializers.ChoiceField(choices=CustomUser.TEAM_CHOICES)

    class Meta:
        model = CustomUser
        fields = ('id', 'team', 'email', 'first_name', 'last_name', 'username',
                  'date_joined', 'password',)

        extra_kwargs = {
            'password': {'write_only': True},
            'team':  {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'username': {'required': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            is_active=True,
        )
        return user
        # return User.objects.create_user(**validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
