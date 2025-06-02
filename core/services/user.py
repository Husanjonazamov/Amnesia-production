from datetime import datetime

from django.contrib.auth import get_user_model, hashers
from django.utils.translation import gettext as _
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt import tokens


class UserService:
    def get_token(self, user):
        refresh = tokens.RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def create_user(self, user_id, first_name, last_name, password):
        get_user_model().objects.update_or_create(
            user_id=user_id,
            defaults={
                "user_id": user_id,
                "first_name": first_name,
                "last_name": last_name,
                "password": hashers.make_password(password),
            },
        )
        

    def validate_user(self, user) -> dict:
        """
        Create user if user not found
        """
        if user.validated_at is None:
            user.validated_at = datetime.now()
        user.save()
        token = self.get_token(user)
        return token

    def is_validated(self, user) -> bool:
        """
        User is validated check
        """
        if user.validated_at is not None:
            return True
        return False

    def change_password(self, user_id, password):
        """
        Change password
        """
        user = get_user_model().objects.filter(user_id=user_id).first()
        if user:
            user.set_password(password)
            user.save()
