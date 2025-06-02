from rest_framework import serializers

from core.apps.accounts.models.user import User
from rest_framework.validators import ValidationError

class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'user_id'
        ]


class ListUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta): ...


class RetrieveUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta): ...



class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  
        fields = ["id", "first_name", "last_name", "user_id"]


    def validate_user_id(self, value):
        if User.objects.filter(user_id=value).exists():
            raise ValidationError("User with this user_id already exists.")
        return value

    def create(self, validated_data):
        user_id = self.context["request"].user.user_id
        
        existing_user = User.objects.filter(user_id=user_id).first()
        if existing_user:
            return existing_user
        
        validated_data["user_id"] = user_id
        return super().create(validated_data)

