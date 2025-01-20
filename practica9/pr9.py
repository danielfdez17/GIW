"""
TODO: rellenar

Asignatura: GIW
Práctica 9
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


import io
import base64
from flask import Flask, request, render_template
from mongoengine import connect, Document, StringField, EmailField
# Resto de importaciones
from flask_bcrypt import Bcrypt
import pyotp
import pyotp.utils
import qrcode
from flask_qrcode import QRcode


app = Flask(__name__)
QRcode(app)
connect('giw_auth')

bcrypt = Bcrypt(app)

# Clase para almacenar usuarios usando mongoengine
# ** No es necesario modificarla **
class User(Document):
    """Clase para almacenar usuarios usando mongoengine"""
    user_id = StringField(primary_key=True)
    full_name = StringField(min_length=2, max_length=50, required=True)
    country = StringField(min_length=2, max_length=50, required=True)
    email = EmailField(required=True)
    passwd = StringField(required=True)
    totp_secret = StringField(required=False)


##############
# APARTADO 1 #
##############

#
# Explicación detallada del mecanismo escogido para el almacenamiento de
# contraseñas, explicando razonadamente por qué es seguro
#


# El mecanismo utilizado para almacenar contraseñas en esta práctica ha sido Bcrypt.
# Hemos decidido usarlo por la facilidad de uso para proteger de forma segura las
# contraseñas almacenadas. Este mecanismo genera sal de forma aleatoria en cada contraseña,
# incluso si son contraseñas iguales. Además, mitiga ataques de fuerza bruta gracias
# a la iteratividad configurable de bcrypt. Es muy común y recomendada para proteger contraseñas.
# Para almacenar las contraseñas llamamos a la función generate_password_hash()
# que genera el hash de la contraseña, y posteriormente se almacena el resultado en la BBDD.
# También hacemos uso de la función check_password_hash() para comprobar que las contraseñas
# introducidas coinciden con las almacenadas en la BBDD.


@app.route('/signup', methods=['POST'])
def signup():
    """
    Función que implementa un registro básico con usuario y contraseña
    """

    nickname = request.form.get('nickname')
    full_name = request.form.get('full_name')
    country = request.form.get('country')
    email = request.form.get('email')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if password != password2:
        return render_template('mensajes.html', message="Las contraseñas no coinciden")


    if User.objects(user_id=nickname):
        return render_template('mensajes.html', message="El usuario ya existe")

    password_hash = bcrypt.generate_password_hash(password)

    usuario = User(user_id=nickname,
                   full_name=full_name,
                   country=country,
                   email=email,
                   passwd=password_hash)

    usuario.save()

    return render_template('mensajes.html', message=f"Bienvenido usuario {full_name}")


@app.route('/change_password', methods=['POST'])
def change_password():
    """
    Función que permite al usuario cambiar la contraseña
    """

    nickname = request.form.get('nickname')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')

    usuario = User.objects(user_id=nickname).first()
    if not usuario:
        return render_template('mensajes.html', message="Usuario o contraseña incorrectos")

    if not bcrypt.check_password_hash(usuario.passwd, old_password):
        return render_template('mensajes.html', message="Usuario o contraseña incorrectos")

    password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')

    usuario.update(passwd=password_hash)

    return render_template('mensajes.html',
                           message=f"La contraseña del usuario {nickname} ha sido modificada")

@app.route('/login', methods=['POST'])
def login():
    """
    Función que implementa un login básico con usuario y contraseña
    """

    nickname = request.form.get('nickname')
    password = request.form.get('password')

    # Si el identificador de usuario no existe o si la password no coincide
    usuario = User.objects(user_id=nickname).first()
    if not usuario or not bcrypt.check_password_hash(usuario.passwd, password):
        return render_template('mensajes.html', message="Usuario o contraseña incorrectos")
    return render_template('mensajes.html', message=f"Bienvenido {usuario.full_name}")

##############
# APARTADO 2 #
##############

#
# Explicación detallada de cómo se genera la semilla aleatoria, cómo se construye
# la URL de registro en Google Authenticator y cómo se genera el código QR
#

@app.route('/signup_totp', methods=['POST'])
def signup_totp():
    """
    Primero realizamos las validaciones necesarias:
    1. Verificamos si las contraseñas no coinciden (contraseña y confirmación).
    2. Comprobamos si el nickname del usuario ya existe en la base de datos.
    En cualquiera de estos casos, mostramos un mensaje de error al usuario.
    A continuación:
    
    1. Generamos un código aleatorio en formato Base32 que servirá como secreto para TOTP.
    2. Construimos la URL compatible con Google Authenticator,
       que incluye los datos necesarios para configurar la cuenta del usuario.
    3. Generamos un código QR con la URL y lo incrustamos en la página que se mostrará al usuario,
       para que pueda escanearlo y configurar su autenticador.
    """
    nickname = request.form.get('nickname')
    full_name = request.form.get('full_name')
    country = request.form.get('country')
    email = request.form.get('email')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if password != password2:
        return render_template('signup_totp.html', message="Las contraseñas no coinciden")

    if User.objects(user_id=nickname).first():
        return render_template('signup_totp.html', message="El usuario ya existe")
    random_token = pyotp.random_base32()

    usuario = User(
        user_id=nickname,
        full_name=full_name,
        country=country,
        email=email,
        passwd=bcrypt.generate_password_hash(password),
        totp_secret=random_token  # Almacenar el secreto generado
    )
    usuario.save()
    totp_url = pyotp.utils.build_uri(
        secret=random_token,
        name=email,
        issuer="GiwAuth"
    )
    #Generamos el codigo QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(totp_url)
    qr.make(fit=True)
    # Convertir el QR a Base64
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return render_template('qr_scan.html',
                            qr_code=qr_base64,
                            message="Escanea este código QR en la App de Google Autenticator.")


@app.route('/login_totp', methods=['POST'])
def login_totp():
    """
    Este método verifica las credenciales del usuario y autentica mediante TOTP.
    1. Comprueba si el nickname proporcionado existe en la base de datos.
    2. Valida que la contraseña ingresada coincida con la almacenada.
    3. Verifica que el código TOTP ingresado sea válido para el usuario.
    Si cualquiera de estas verificaciones falla, se muestra un mensaje de error en la página.
    Si la autenticación es exitosa, redirige al usuario a una página de bienvenida.
    """
    nickname = request.form.get('nickname')
    password = request.form.get('password')
    totp_code = request.form.get('totp')
    # Verificar si el usuario existe en la base de datos
    usuario = User.objects(user_id=nickname).first()
    if not usuario:
        return render_template('login_totp.html', message="Usuario o contraseña incorrectos")

    # Verificar la contraseña
    if not bcrypt.check_password_hash(usuario.passwd, password):
        return render_template('login_totp.html', message="Usuario o contraseña incorrectos")

    # Verificar el código TOTP
    totp = pyotp.TOTP(usuario.totp_secret)
    if not totp.verify(totp_code):
        return render_template('login_totp.html', message="Usuario o contraseña incorrectos")

    return render_template('login_totp_welcome.html', welcome=usuario.full_name)


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
