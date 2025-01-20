"""
Fichero con las funciones que manejan las peticiones HTTP
"""
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.http import HttpResponseBadRequest
from django.core.exceptions import ValidationError
from .models import Pregunta, Respuesta
from .forms import LoginForm, PreguntaForm, RespuestaForm

# Create your views here.
@require_GET
def index(request):
    """ Página principal, muestra las prguntas ordenadas por fecha """
    preguntas = Pregunta.objects.order_by('-fecha')
    return render(request,
                  "listar_preguntas.html",
                  {'preguntas': preguntas, 'pregunta_form': PreguntaForm})

@require_http_methods(["GET", "POST"])
def loginfunction(request):
    """ Muestra el formulario (GET) o recibe los datos y realiza la autenticacion (POST) """
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {'login_form': form})

    form = LoginForm(request.POST)
    if not form.is_valid(): #Valida el fomulario
        return HttpResponseBadRequest(f"Error en los datos del formulario: {form.errors}")

    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(reverse('preguntas:index'))

    return render(request, 'login.html', {'error': 'Usuario o contraseña no válidos'})


@require_GET
def logoutfunction(request):
    """ Elimina al usuario de la sesión actual """
    logout(request)
    return redirect(reverse('preguntas:index'))

@login_required(login_url='preguntas:login')
@require_POST
def nueva_pregunta(request):
    """ 
        Añade la pregunta (POST)
    """

    form = PreguntaForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(f"Error en los datos del formulario: {form.errors}")
    form_titulo = form.cleaned_data['titulo']
    form_texto = form.cleaned_data['text']

    # Crea un objeto ORM a partir de los datos limpios del formulario y lo salva en la BD
    pregunta = Pregunta(titulo=form_titulo, texto=form_texto, autor=request.user)
    try:
        pregunta.full_clean()
        pregunta.save()
    except ValidationError:
        return HttpResponseBadRequest("Pregunta mal formada")

    return redirect(reverse('preguntas:index'))

@login_required(login_url='preguntas:login')
@require_http_methods(["POST", "GET"])
def nueva_respuesta(request, id):
    """
    Permite que un usuario autenticado añada una respuesta a una pregunta existente
    NOTA: si utilizamos cualquier otro nombre para el argumento id, la aplicación falla
    """
    pregunta = get_object_or_404(Pregunta, id=id)
    if request.method == "GET":
        # Mostrar un formulario vacío si se accede por GET
        respuestas = pregunta.respuesta_set.all().order_by('-fecha')
        form = RespuestaForm()
        return render(request, 'detalle_pregunta.html', {'pregunta': pregunta,
                                                         'respuestas':respuestas, 
                                                         'respuesta_form': form})

    form = RespuestaForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(f"Error en los datos del formulario: {form.errors}")

    texto = form.cleaned_data['texto']

    respuesta = Respuesta(texto=texto, autor=request.user, pregunta=pregunta)
    try:
        respuesta.full_clean()
        respuesta.save()
    except ValidationError:
        return HttpResponseBadRequest('Respuesta mal formada')

    return redirect(reverse('preguntas:detalle_pregunta', args=(id,)))
