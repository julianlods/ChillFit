from ChillFit.models import Usuario
from django.db.models import Count

def limpiar_usuarios_duplicados():
    duplicados = Usuario.objects.values('email').annotate(email_count=Count('email')).filter(email_count__gt=1)
    for dup in duplicados:
        print(f"Usuarios duplicados con email: {dup['email']}")
        usuarios = Usuario.objects.filter(email=dup['email'])
        for usuario in usuarios[1:]:  # Mantén solo uno, elimina los demás
            usuario.delete()

limpiar_usuarios_duplicados()
