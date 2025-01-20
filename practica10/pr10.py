"""
TODO: rellenar

Asignatura: GIW
Práctica 10
Grupo: 5
Autores:
 - Luis Enrique Barrero Peña
 - Daniel Fernández Ortiz
 - Airam Martín Peraza
 - José Waldo Villacres Zumaeta

Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
de manera directa o indirecta. Declaramos además que no hemos realizado de manera
deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
resultados de los demás.
"""
import base64
import json
import string
import random
from datetime import datetime, timezone
from flask import Flask, redirect, request, session, render_template
import requests

# Resto de importaciones


app = Flask(__name__)


# Credenciales
CLIENT_ID = 'client_id'
CLIENT_SECRET = 'client_secret'

REDIRECT_URI = 'http://localhost:5000/token'

# Fichero de descubrimiento para obtener el 'authorization endpoint' y el
# 'token endpoint'
DISCOVERY_DOC = 'https://accounts.google.com/.well-known/openid-configuration'
JSON_DISCOVERY_DOC = requests.get(DISCOVERY_DOC, timeout=5).json()

def generate_csrf_token():
    """Función que genera el token CSRF"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def decode_jwt(jwt):
    """
    Decodifica un JWT sin validar la firma (ya que confíamos en Google).
    """
    _, payload, _ = jwt.split('.')

    padded_payload = payload + "=" * ((4 - len(payload) % 4) % 4)
    decoded_payload = base64.urlsafe_b64decode(padded_payload).decode('utf-8')

    payload_data = json.loads(decoded_payload)

    exp = payload_data.get("exp")
    if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(tz=timezone.utc):
        raise ValueError("El token ha expirado")

    iss = payload_data.get("iss")
    if iss != JSON_DISCOVERY_DOC["issuer"]:
        raise ValueError("El token no fue emitido por Google")

    aud = payload_data.get("aud")
    if aud != CLIENT_ID:
        raise ValueError("El token no pertenece a esta aplicación")

    return payload_data

def validate_id_token_with_google(id_token):
    """
    Valida el id_token usando el extremo tokeninfo de Google.
    """
    tokeninfo_url = f"{JSON_DISCOVERY_DOC['token_endpoint']}info?id_token={id_token}"
    response = requests.get(tokeninfo_url, timeout=2)
    if response.status_code != 200:
        raise ValueError("El id_token no es válido")
    return response.json()

@app.route("/", methods=['GET'])
def redirect_login_google():
    """Redirige a login_google para no escribir la ruta en el navegador"""
    return redirect("/login_google")

@app.route('/login_google', methods=['GET'])
def login_google():
    """
    Redirige al usuario a Google para iniciar el proceso de autenticación.
    Primero generamos un token al que llamamos state y lo almacenamos en la sesión
    """
    state = generate_csrf_token()
    session['state'] = state

    auth_url = ( f"{JSON_DISCOVERY_DOC['authorization_endpoint']}?"
                f"client_id={CLIENT_ID}&"
                f"redirect_uri={REDIRECT_URI}&"
                f"response_type=code&"
                f"scope=openid email&"
                f"state={state}")

    return redirect(auth_url)


@app.route('/token', methods=['GET'])
def token():
    """
    Recibe la petición del usuario redirigida desde Google
    """

    code = request.args.get('code')
    state = request.args.get('state')

    if not code:
        return "Error: No se ha recibido el código de autorización.", 400

    if state != session.get('state'):
        return "Error: el token CSRF no coincide", 403

    token_url = JSON_DISCOVERY_DOC['token_endpoint']

    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response = requests.post(token_url, data=data, timeout=2)
    token_response = response.json()

    if "id_token" not in token_response:
        return f"""
        Error al obtener el token: {token_response.get('error_description', 'Desconocido')}
        """, 400

    id_token = token_response["id_token"]
    try:
        user_info = decode_jwt(id_token)
    except ValueError as e:
        return f"Error al validar el token: {str(e)}", 400

    email = user_info.get("email", "Usuario desconocido")

    return render_template('bienvenida.html', email=email)


if __name__ == '__main__':
    # Activa depurador y recarga automáticamente
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['TEST'] = True

    # Imprescindible para usar sesiones
    app.config['SECRET_KEY'] = 'giw_clave_secreta'

    app.config['STATIC_FOLDER'] = 'static'
    app.config['TEMPLATES_FOLDER'] = 'templates'

    app.run()
