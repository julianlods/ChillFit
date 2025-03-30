from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, PerfilUsuario, UsuarioRutina, Rutina, BloqueEjercicio


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        error_messages={
            'invalid': 'Introduzca una dirección válida de email'
        }
    )

    class Meta:
        model = Usuario
        fields = ('email', 'username', 'password1', 'password2')


class PerfilUsuarioForm(forms.ModelForm):
    """
    Formulario para capturar datos adicionales del perfil de usuario.
    """
    class Meta:
        model = PerfilUsuario
        fields = ('telefono', 'edad')


class UsuarioRutinaForm(forms.ModelForm):
    """
    Formulario personalizado para UsuarioRutina.
    Permite mostrar el nombre y descripción de la rutina.
    """
    class Meta:
        model = UsuarioRutina
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rutina'].queryset = Rutina.objects.all()
        self.fields['rutina'].label_from_instance = lambda obj: (
            f"{obj.nombre} - {obj.descripcion[:30]}..." if obj.descripcion else obj.nombre
        )


class BloqueEjercicioForm(forms.ModelForm):
    class Meta:
        model = BloqueEjercicio
        fields = '__all__'
        widgets = {
            'ejercicio': forms.Select(attrs={'class': 'vTextField', 'style': 'width: 300px'}),
        }
