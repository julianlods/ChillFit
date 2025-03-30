import re
import json
import mercadopago

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.conf import settings

from .models import UsuarioRutina, Rutina, PerfilUsuario, PlanDeTrabajo, Pago, BloqueEjercicio
from .forms import CustomUserCreationForm, PerfilUsuarioForm


@login_required
def home(request):
    """
    Vista principal de la aplicación tras iniciar sesión.
    Muestra un mensaje de bienvenida o acceso rápido a las rutinas.
    """
    return render(request, 'ChillFit/home.html', {
        'usuario': request.user
    })


User = get_user_model()

def login_view(request):
    """
    Vista para el inicio de sesión.
    Permite autenticar con username o email junto con la contraseña.
    """
    if request.method == 'POST':
        identifier = request.POST.get('username')  # Puede ser username o email
        password = request.POST.get('password')

        # Buscar por email o username
        try:
            user_obj = User.objects.get(email=identifier)
        except User.DoesNotExist:
            try:
                user_obj = User.objects.get(username=identifier)
            except User.DoesNotExist:
                user_obj = None

        if user_obj:
            user = authenticate(request, username=user_obj.username, password=password)
        else:
            user = None

        if user is not None:
            login(request, user)
            return redirect('ver_rutinas')
        else:
            messages.error(request, 'Usuario, email o contraseña incorrectos.')

    return render(request, 'ChillFit/login.html')


def register_view(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = PerfilUsuarioForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.usuario = user
            profile.save()

            # Dejamos solo la variable para SweetAlert
            user_form = CustomUserCreationForm()
            profile_form = PerfilUsuarioForm()

            return render(request, 'ChillFit/register.html', {
                'user_form': user_form,
                'profile_form': profile_form,
                'registro_exitoso': True  
            })

    else:
        user_form = CustomUserCreationForm()
        profile_form = PerfilUsuarioForm()

    return render(request, 'ChillFit/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def ver_rutinas(request):
    """
    Vista protegida para ver rutinas.
    Muestra las rutinas asignadas al usuario autenticado con su estado.
    """
    usuario = request.user
    usuario_rutinas = UsuarioRutina.objects.filter(usuario=usuario).order_by('orden', 'id')


    # Preparar las rutinas con su estado
    rutinas = [
        {
            'id': ur.rutina.id,
            'nombre': ur.rutina.nombre,
            'bloques': ur.rutina.bloques,
            'realizada': ur.realizada
        }
        for ur in usuario_rutinas
    ]

    return render(request, 'ChillFit/rutinas/ver_rutinas.html', {
        'rutinas': rutinas
    })


def extraer_id_youtube(url):
    """Extrae el ID de un video de YouTube desde su URL."""
    if not url:
        return None

    patron = r"(?:v=|youtu\.be/|embed/|shorts/)([a-zA-Z0-9_-]{11})"
    coincidencia = re.search(patron, url)
    return coincidencia.group(1) if coincidencia else None


def extraer_id_youtube(url):
    """Extrae el ID de un video de YouTube desde su URL."""
    if not url:
        return None

    patron = r"(?:v=|youtu\.be/|embed/|shorts/|watch\?v=)([a-zA-Z0-9_-]{11})"
    coincidencia = re.search(patron, url)
    return coincidencia.group(1) if coincidencia else None


@login_required
def ver_rutina_detalle(request, rutina_id):
    usuario = request.user
    usuario_rutina = get_object_or_404(UsuarioRutina, rutina_id=rutina_id, usuario=usuario)

    if request.method == 'POST':
        usuario_rutina.realizada = 'desmarcar' not in request.POST
        usuario_rutina.fecha_realizacion = request.POST.get('fecha', now().date()) if usuario_rutina.realizada else None
        usuario_rutina.save()
        return redirect('ver_rutina_detalle', rutina_id=rutina_id)

    rutina = usuario_rutina.rutina
    bloques_lista = []

    for bloque in rutina.bloques.all():
        ejercicios_lista = []
        bloque_ejercicios = BloqueEjercicio.objects.filter(bloque=bloque).order_by('orden')

        for be in bloque_ejercicios:
            ejercicio = be.ejercicio
            video_id = extraer_id_youtube(ejercicio.video) if ejercicio.video else None
            ejercicios_lista.append({
                'descripcion': ejercicio.descripcion,
                'video': ejercicio.video,
                'video_id': video_id
            })

        bloques_lista.append(bloque)

    return render(request, 'ChillFit/rutinas/ver_rutina_detalle.html', {
        'rutina': {
            'id': rutina.id,
            'bloques': bloques_lista
        },
        'usuario_rutina': usuario_rutina,
        'fecha_hoy': now().date()
    })


@login_required
def marcar_rutina_realizada(request, rutina_id):
    """
    Marca una rutina como realizada para el usuario actual.
    """
    usuario = request.user
    usuario_rutina = get_object_or_404(UsuarioRutina, rutina_id=rutina_id, usuario=usuario)

    if request.method == 'POST':
        usuario_rutina.realizada = True
        usuario_rutina.fecha_realizacion = now()
        usuario_rutina.save()

    return redirect('ver_rutina_detalle', rutina_id=rutina_id)


def contacto(request):
    return render(request, 'ChillFit/contacto.html')


def enviar_consulta(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')

        # Envía un correo (configura correctamente el servidor de correo en settings.py)
        cuerpo_mensaje = f"Nombre: {nombre}\nCorreo: {email}\n\nMensaje:\n{mensaje}"
        send_mail(
            subject=f"Consulta: {asunto}",
            message=cuerpo_mensaje,
            from_email=email,
            recipient_list=['julian.lods@gmail.com'],  # Cambia por el correo de la profesora
        )

        messages.success(request, '¡Tu consulta fue enviada correctamente! Te responderemos pronto.')
        return redirect('contacto')


@login_required
def perfil(request):
    usuario = request.user

    # Obtener o crear el perfil del usuario
    perfil = get_object_or_404(PerfilUsuario, usuario=usuario)

    if request.method == 'POST':
        perfil.telefono = request.POST.get('telefono', perfil.telefono)
        perfil.edad = request.POST.get('edad', perfil.edad)
        perfil.sexo = request.POST.get('sexo', perfil.sexo)
        if 'avatar' in request.FILES:
            perfil.avatar = request.FILES['avatar']

        # Asignar el Plan de Trabajo seleccionado
        plan_id = request.POST.get('plan')
        if plan_id:
            perfil.plan_de_trabajo = PlanDeTrabajo.objects.get(id=plan_id)

        perfil.save()

        # CAMBIO DE CONTRASEÑA (si se completan los campos)
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 or password2:
            if password1 == password2 and password1.strip():
                usuario.set_password(password1)
                usuario.save()
                messages.success(request, 'Contraseña actualizada correctamente. Por favor, iniciá sesión de nuevo.')
                return redirect('login')  # Se desloguea tras cambiar la contraseña
            else:
                messages.error(request, 'Las contraseñas no coinciden o son inválidas.')
                return redirect('perfil')

        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('perfil')

    planes = PlanDeTrabajo.objects.all()  # Obtener todos los planes

    return render(request, 'ChillFit/perfil.html', {
        'perfil': perfil,
        'planes': planes
    })


@login_required
def generar_pago(request):
    usuario = request.user

    pagos_pendientes = Pago.objects.filter(usuario=usuario, estado="pendiente")
    pagos_aprobados = Pago.objects.filter(usuario=usuario, estado="aprobado")
    pagos_informados = Pago.objects.filter(usuario=usuario, estado="informado")

    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

    pagos_con_links = []
    for pago in pagos_pendientes:
        # SOLO generar el preference_id si no hay comprobante ni ID ya generado
        if not pago.id_pago_mercadopago and not pago.comprobante_transferencia:
            preference_data = {
                "items": [
                    {
                        "title": pago.descripcion,
                        "quantity": 1,
                        "currency_id": "ARS",
                        "unit_price": float(pago.monto),
                    }
                ],
                "back_urls": {
                    "success": request.build_absolute_uri('/pago_exitoso/'),
                    "failure": request.build_absolute_uri('/pago_fallido/'),
                    "pending": request.build_absolute_uri('/pago_pendiente/')
                },
                "auto_return": "approved",
                "external_reference": str(pago.id)
            }

            preference_response = sdk.preference().create(preference_data)
            preference_id = preference_response["response"].get("id", "")

            pago.id_pago_mercadopago = preference_id
            pago.metodo_pago = 'mercadopago'  
            pago.save()

        pagos_con_links.append({
            "id": pago.id,
            "id_pago_usuario": pago.id_pago_usuario,
            "descripcion": pago.descripcion,
            "monto": pago.monto,
            "estado": pago.estado,
            "plan_de_trabajo": pago.plan_de_trabajo.nombre if pago.plan_de_trabajo else "Sin Plan",
            "preference_id": pago.id_pago_mercadopago
        })

    return render(request, 'ChillFit/generar_pago.html', {
        "pagos_pendientes": pagos_con_links,
        "pagos_aprobados": pagos_aprobados,
        "pagos_informados": pagos_informados,
        "mp_public_key": settings.MERCADOPAGO_PUBLIC_KEY
    })


@login_required
def pago_exitoso(request):
    return render(request, 'ChillFit/pago_exitoso.html')

@login_required
def pago_fallido(request):
    return render(request, 'ChillFit/pago_fallido.html')


def get_plan_pago(request, user_id):
    """ Devuelve el plan de pago y monto del usuario seleccionado """
    try:
        perfil = PerfilUsuario.objects.get(usuario_id=user_id)
        if perfil.plan_de_trabajo:
            return JsonResponse({
                "plan_id": perfil.plan_de_trabajo.id,
                "plan_nombre": perfil.plan_de_trabajo.nombre,
                "monto": str(perfil.plan_de_trabajo.precio_mensual)
            })
    except PerfilUsuario.DoesNotExist:
        pass

    return JsonResponse({"plan_id": None, "plan_nombre": "Sin Plan", "monto": "0.00"})


@login_required
@require_http_methods(["GET", "POST"])
def informar_transferencia(request):
    if request.method == "POST":
        pago_id = request.POST.get("pago_id")

        # Validación básica
        if not pago_id or not pago_id.isdigit():
            messages.error(request, "No se pudo identificar el pago.")
            return redirect("generar_pago")

        pago_id = int(pago_id)

        try:
            pago = Pago.objects.get(id=pago_id, usuario=request.user, estado="pendiente")
        except Pago.DoesNotExist:
            messages.error(request, "El pago no existe o ya fue informado.")
            return redirect("generar_pago")

        descripcion = request.POST.get("descripcion")
        comprobante = request.FILES.get("comprobante")

        if not comprobante:
            messages.error(request, "Debés adjuntar un comprobante.")
            return redirect("informar_transferencia")  # podrías agregar ?pago_id={{ pago.id }}

        # Actualiza el pago existente
        pago.descripcion = descripcion or pago.descripcion
        pago.comprobante_transferencia = comprobante
        pago.estado = "informado"
        pago.metodo_pago = "transferencia"  # ✅ marcamos como transferencia
        pago.id_pago_mercadopago = None     # ✅ limpiamos si se generó por error
        pago.save()

        messages.success(request, "Tu comprobante fue enviado correctamente.")
        return redirect("generar_pago")

    else:
        pago_id = request.GET.get("pago_id")

        # Validar en GET también
        if not pago_id or not pago_id.isdigit():
            messages.error(request, "No se pudo identificar el pago.")
            return redirect("generar_pago")

        return render(request, "ChillFit/informar_transferencia.html", {"pago_id": pago_id})


@csrf_exempt
def webhook_mercadopago(request):
    print("==== [WEBHOOK] Nueva solicitud recibida ====")
    print("🌐 Full path:", request.get_full_path())

    try:
        # Intenta leer como JSON (correcto)
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        # Fallback: intenta tomar los datos por GET (ej: /?type=payment&data.id=xxx)
        data = {
            "type": request.GET.get("type"),
            "data": {
                "id": request.GET.get("data.id")
            }
        }

    print("📦 Data procesada:", data)

    if data.get("type") == "payment" and data.get("data", {}).get("id"):
        payment_id = data["data"]["id"]
        print("🔎 ID de pago recibido:", payment_id)

        try:
            sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
            payment_info = sdk.payment().get(payment_id)
            print("📄 Info de pago:", payment_info)

            status = payment_info["response"].get("status", "")
            external_ref = payment_info["response"].get("external_reference")

            print("📌 Estado del pago:", status)
            print("🔗 External Reference:", external_ref)

            if status == "approved" and external_ref:
                from .models import Pago
                try:
                    pago = Pago.objects.get(id=external_ref)
                    pago.estado = "aprobado"
                    pago.fecha_pago = timezone.now()
                    pago.id_pago_mercadopago = str(payment_id)
                    pago.metodo_pago = "mercadopago"
                    pago.save()
                    print("✅ Pago actualizado con éxito:", pago.id)
                except Pago.DoesNotExist:
                    print(f"❌ No se encontró el pago con id={external_ref}")
        except Exception as e:
            print("🚨 Error al consultar MP:", e)
    else:
        print("❌ Tipo o datos inválidos en el webhook")

    return HttpResponse(status=200)
