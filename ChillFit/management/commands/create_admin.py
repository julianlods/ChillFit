from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Crea el usuario admin a'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(username='a').exists():
            User.objects.create_superuser('a', 'a@correo.com', 'a')
            self.stdout.write(self.style.SUCCESS('✔️ Superusuario "a" creado.'))
        else:
            self.stdout.write('ℹ️ El usuario "a" ya existe.')
