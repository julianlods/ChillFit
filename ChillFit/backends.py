# ChillFit/backends.py

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class UsuarioEmailBackend(BaseBackend):
    """
    Backend de autenticación personalizado que permite el login
    utilizando el email o el username junto con la contraseña.
    Ahora también insensible a mayúsculas.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Insensible a mayúsculas
            users = UserModel.objects.filter(
                Q(email__iexact=username) | Q(username__iexact=username)
            )

            if users.count() == 1:
                user = users.first()
            else:
                return None
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

