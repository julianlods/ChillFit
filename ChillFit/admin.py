from django.contrib import admin
from django import forms
from django.utils import timezone
from .models import Usuario, PerfilUsuario, PlanDeTrabajo, Ejercicio, Bloque, Rutina, MetodoDeTrabajo, UsuarioRutina, Pago, BloqueEjercicio
from .forms import UsuarioRutinaForm, BloqueEjercicioForm
from django.utils.html import format_html


# Configuración para el modelo Usuario
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    list_filter = ('is_active', 'is_staff')
    ordering = ('email',)

admin.site.register(Usuario, UsuarioAdmin)

# Configuración para el modelo PerfilUsuario
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefono', 'edad', 'sexo', 'plan_de_trabajo')
    search_fields = ('usuario__email', 'usuario__username')
    list_filter = ('sexo', 'plan_de_trabajo')

admin.site.register(PerfilUsuario, PerfilUsuarioAdmin)

# Configuración para el modelo PlanDeTrabajo
class PlanDeTrabajoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_mensual', 'descripcion')
    search_fields = ('nombre',)
    list_filter = ('precio_mensual',)
    ordering = ('nombre',)

admin.site.register(PlanDeTrabajo, PlanDeTrabajoAdmin)

# Configuración para el modelo Ejercicio
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'video')
    search_fields = ('descripcion',)

admin.site.register(Ejercicio, EjercicioAdmin)


class BloqueEjercicioInline(admin.TabularInline):
    model = BloqueEjercicio
    form = BloqueEjercicioForm
    extra = 0
    ordering = ['orden']
    autocomplete_fields = ['ejercicio']


# Configuración para el modelo Bloque
class BloqueAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'metodo_de_trabajo')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('metodo_de_trabajo',)
    ordering = ('nombre',)
    inlines = [BloqueEjercicioInline]  # ← ¡ACÁ LA MAGIA!

admin.site.register(Bloque, BloqueAdmin)

# Configuración para el modelo Rutina
class RutinaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')
    list_filter = ()
    ordering = ('nombre',)
    filter_horizontal = ('bloques',)

admin.site.register(Rutina, RutinaAdmin)

# Configuración para el modelo MetodoDeTrabajo
class MetodoDeTrabajoAdmin(admin.ModelAdmin):
    list_display = ('descripcion',)
    search_fields = ('descripcion',)

admin.site.register(MetodoDeTrabajo, MetodoDeTrabajoAdmin)

# Configuración para el modelo UsuarioRutina
class UsuarioRutinaAdmin(admin.ModelAdmin):
    form = UsuarioRutinaForm
    list_display = ('usuario', 'rutina', 'realizada', 'fecha_realizacion', 'orden')
    list_editable = ('orden',)
    ordering = ('usuario', 'orden')

admin.site.register(UsuarioRutina, UsuarioRutinaAdmin)

# Configuración para el modelo Pago
class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.usuario.perfil.plan_de_trabajo:
                self.fields['plan_de_trabajo'].initial = self.instance.usuario.perfil.plan_de_trabajo
                self.fields['monto'].initial = self.instance.usuario.perfil.plan_de_trabajo.precio_mensual
        self.fields['plan_de_trabajo'].widget.attrs['readonly'] = True
        self.fields['monto'].widget.attrs['readonly'] = True


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        exclude = ['plan_de_trabajo'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PagoAdmin(admin.ModelAdmin):
    form = PagoForm
    readonly_fields = ('mostrar_comprobante',)
    list_display = ('id_pago_usuario', 'usuario', 'monto', 'descripcion', 'estado', 'metodo_pago', 'id_pago_mercadopago', 'fecha_pago','mostrar_comprobante')
    list_filter = ('estado', 'plan_de_trabajo', 'metodo_pago')
    search_fields = ('usuario__email', 'usuario__username', 'id_pago_usuario', 'id_pago_mercadopago')
    ordering = ('-fecha_generacion',)
    actions = ['marcar_como_aprobado', 'marcar_como_rechazado']

    def save_model(self, request, obj, form, change):
        # Ya no se vincula automáticamente el plan ni el monto
        super().save_model(request, obj, form, change)

    def marcar_como_aprobado(self, request, queryset):
        queryset.update(estado="aprobado", fecha_pago=timezone.now())
        self.message_user(request, "Los pagos seleccionados han sido marcados como Aprobados.")

    def marcar_como_rechazado(self, request, queryset):
        queryset.update(estado="rechazado")
        self.message_user(request, "Los pagos seleccionados han sido marcados como Rechazados.")
    
    def mostrar_comprobante(self, obj):
        if obj.comprobante_transferencia:
            return format_html(
                '<a href="{}" target="_blank">Ver Comprobante</a>',
                obj.comprobante_transferencia.url
            )
        return "Sin comprobante"

    mostrar_comprobante.short_description = "Comprobante"

    marcar_como_aprobado.short_description = "Marcar pagos como Aprobados"
    marcar_como_rechazado.short_description = "Marcar pagos como Rechazados"

admin.site.register(Pago, PagoAdmin)
