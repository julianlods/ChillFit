# ChillFit/backends.py

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class UsuarioEmailBackend(BaseBackend):
    """
    Backend de autenticación personalizado que permite el login
    utilizando el email o el username junto con la contraseña.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Buscar al usuario por email o username
            if '@' in username:
                users = UserModel.objects.filter(email=username)
            else:
                users = UserModel.objects.filter(username=username)

            if users.count() == 1:
                user = users.first()
            else:
                return None  # Maneja el caso de múltiples usuarios o ninguno encontrado
        except UserModel.DoesNotExist:
            return None

        # Verificar la contraseña
        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
