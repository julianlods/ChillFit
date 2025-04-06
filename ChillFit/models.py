from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.contrib.auth import get_user_model
from django.utils import timezone
from cloudinary.models import CloudinaryField
import uuid
import re  


class UsuarioManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    edad = models.PositiveIntegerField(blank=False, null=False, default=18)
    avatar = CloudinaryField('avatar', blank=True, null=True)

    sexo = models.CharField(
        max_length=10,
        choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')],
        blank=True,
        null=True
    )
    plan_de_trabajo = models.ForeignKey(
        'PlanDeTrabajo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='perfiles'
    )

    def __str__(self):
        return f"Perfil de {self.usuario.username}"


class PlanDeTrabajo(models.Model):
    nombre = models.CharField(max_length=255)
    precio_mensual = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Ejercicio(models.Model):
    descripcion = models.CharField(max_length=200)
    video = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.descripcion

    def clean(self):
        if self.video and 'shorts/' in self.video:
            match = re.search(r'shorts/([a-zA-Z0-9_-]{11})', self.video)
            if match:
                video_id = match.group(1)
                self.video = f"https://www.youtube.com/watch?v={video_id}"

    @property
    def video_id(self):
        if self.video and "youtube" in self.video:
            return self.video.split("v=")[-1].split("&")[0]
        elif "youtu.be/" in self.video:
            return self.video.split("youtu.be/")[-1].split("?")[0]
        return None


class MetodoDeTrabajo(models.Model):
    descripcion = models.CharField(max_length=250)

    def __str__(self):
        return self.descripcion


class Bloque(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    metodo_de_trabajo = models.ForeignKey(MetodoDeTrabajo, on_delete=models.CASCADE)
    ejercicios_ordenados = models.ManyToManyField(Ejercicio, through='BloqueEjercicio', related_name='bloques_ordenados', blank=True)


    def __str__(self):
        if self.descripcion:
            return f"{self.nombre} - {self.descripcion[:30]}"
        return self.nombre


class BloqueEjercicio(models.Model):
    bloque = models.ForeignKey('Bloque', on_delete=models.CASCADE)
    ejercicio = models.ForeignKey('Ejercicio', on_delete=models.CASCADE)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('bloque', 'ejercicio')
        ordering = ['orden']

    def __str__(self):
        return f"{self.bloque.nombre} - {self.ejercicio.descripcion} (orden {self.orden})"


class Rutina(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)  # Campo agregado
    bloques = models.ManyToManyField(Bloque, blank=True)
    incluir_tabata = models.BooleanField(default=True, help_text="¿Mostrar temporizador Tabata en esta rutina?")

    def __str__(self):
        return self.nombre


class UsuarioRutina(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='rutinas_asignadas')
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE, related_name='usuarios_asignados')
    realizada = models.BooleanField(default=False)
    fecha_realizacion = models.DateField(blank=True, null=True)
    orden = models.PositiveIntegerField(default=0)  # Nuevo campo

    class Meta:
        unique_together = ('usuario', 'rutina')
        ordering = ['orden', 'id']  # Se ordenan por este campo por defecto

    def __str__(self):
        estado = "Realizada" if self.realizada else "Pendiente"
        return f"{self.usuario.username} - {self.rutina.nombre} ({estado})"

Usuario = get_user_model()

class Pago(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('informado', 'Informado'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]

    METODO_CHOICES = [
        ('mercadopago', 'MercadoPago'),
        ('transferencia', 'Transferencia'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="pagos")
    plan_de_trabajo = models.ForeignKey(PlanDeTrabajo, on_delete=models.SET_NULL, null=True, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=255, help_text="Ejemplo: 'Clase 1' o 'Mensualidad Enero'")
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    comprobante_transferencia = CloudinaryField(
        'comprobante',
        blank=True,
        null=True,
        help_text="Solo para pagos informados por transferencia"
    )

    id_pago_usuario = models.PositiveIntegerField(editable=False)
    id_pago_mercadopago = models.CharField(max_length=50, blank=True, null=True, help_text="ID de MercadoPago")
    metodo_pago = models.CharField(max_length=20, choices=METODO_CHOICES, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id_pago_usuario:
            ultimo_pago = Pago.objects.filter(usuario=self.usuario).order_by('-id_pago_usuario').first()
            self.id_pago_usuario = (ultimo_pago.id_pago_usuario + 1) if ultimo_pago else 1
        super().save(*args, **kwargs)

    def __str__(self):
        metodo = self.get_metodo_pago_display() if self.metodo_pago else "Sin método"
        return f"Pago {self.id_pago_usuario} - {self.usuario.username} - ${self.monto} - {self.get_estado_display()} ({metodo})"

