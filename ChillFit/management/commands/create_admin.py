from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Crea el usuario admin j'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(username='j').exists():
            User.objects.create_superuser('j', 'julian.lods@gmail.com', 'j')
            self.stdout.write(self.style.SUCCESS('✔️ Superusuario j creado.'))
        else:
            self.stdout.write('ℹ️ El usuario j ya existe.')
