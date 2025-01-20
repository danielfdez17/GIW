# -*- coding: utf-8 -*-
"""
@author: Enrique Martín Martín
@email: emartinm@ucm.es

Vulnerabilidad Cross-Site Request Forgery (POST)

Pasos para reproducirla
1.- En pestaña 1: autenticarse en http://localhost:5000/login con 
    usuario "pepe" y contraseña "1234"

2.- En pestaña 1: hacer una compra de un artículo a la dirección por defecto.
    Comprobar el log del servidor para ver los detalles de la compra registrada.

3.- En pestaña 2: ver una página "inocente". Hay dos opciones:
     a) cargar el fichero "csrf.html" y pinchar en el enlace engañoso
        SESSION_COOKIE_SAMESITE = None
     b) cargar http://localhost:5000/pagina_inocente y pinchar en el enlace engañoso si
        SESSION_COOKIE_SAMESITE = 'Strict' o 
        SESSION_COOKIE_SAMESITE = 'Lax'
        
4.- Comprobar el log del servidor para ver que has realizado una compra sin
    darte cuenta.

El paso 3.b) es un poco forzado porque estás visitando una página del mismo dominio
localhost:5000, pero notad que el formulario oculto podría haber sido introducido 
mediante un XSS persistente o reflejado.
El paso 3.a) también es un poco forzado porque requiere que el servidor configure
el valor SAMESITE a None, lo que es un fallo grande

Funciona en:
* Firefox 132.0.1
* Chrome Versión 131.0.6778.69
"""

from flask import Flask, request, session, render_template, url_for, redirect
import sqlite3
import secrets


DBPATH = 'database.db'

app = Flask(__name__)


def reset_database():
    with sqlite3.connect(DBPATH) as conn:
        conn.executescript(
        """DROP TABLE IF EXISTS users;
           CREATE TABLE users (
               id INTEGER PRIMARY KEY AUTOINCREMENT, 
               username TEXT, 
               password TEXT,
               credit_card TEXT);
           INSERT INTO users(username, password, credit_card) VALUES 
               ('pepe', '1234', '1245789885632547');

           DROP TABLE IF EXISTS orders;
           CREATE TABLE orders (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user INTEGER NOT NULL REFERENCES users(id),
               num_items INTEGER NOT NULL,
               address TEXT,
               date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);""")
        conn.commit()


@app.route('/login', methods=['GET'])
def login_form():
    """ Devuelve el formulario para iniciar sesión """
    return render_template("login_form.html")
    

@app.route('/login', methods=['POST'])
def login():
    """ Autentica al usuario y envía a página para comprar patatas.
        PARA SIMPLIFICAR EL EJEMPLO no valida las entradas y almacena la 
        contraseña en texto plano PERO ESTO NUNCA HABRÍA QUE HACERLO
    """
    passwd = request.form['pass']
    user = request.form['user']

    query = "SELECT * FROM users WHERE username=:user"
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(query, {'user': user})
    row = cur.fetchone()
    conn.close()

    if row is not None and row[2] == passwd:
        # Usuario autenticado. **Obviamente en la vida real usaríamos hash+sal+ralentizado** y no texto plano
        session.clear()
        session['username'] = user
        return redirect(url_for('comprar_form'))
    else:
        return "Usuario o contraseña incorrectos"


@app.route('/comprar', methods=['GET'])
def comprar_form():
    """ Muestra la página principal con el formulario para comprar """
    if 'username' in session:
        # Versión insegura (no usa token antiCSRF):
        return render_template('principal.html', user=session['username'])
        
        # Version segura (inserta token antiCSRF en el formulario):
        # session['anticsrf'] = secrets.token_hex()
        # app.logger.info(f"Token antiCSRF para compras: {session['anticsrf']}")
        # return render_template('principal_safe.html', user=session['username'], 
        #                        anticsrf=session['anticsrf'])
    else:
        return redirect(url_for('login_form'))


@app.route('/comprar', methods=['POST'])
def comprar():
    """Página para realizar compras de usuarios autenticados. NO REALIZA VALIDACIÓN
       DE PARÁMETROS POR SIMPLICIDAD """
    if 'username' in session:    
        # Versión segura: comprueba el token antiCSRF que se recibe con el 
        #     formulario y lo compara con el almacenado en la sesión
        # anticsrf = request.form.get('anticsrf', '')
        # if session['anticsrf'] is None or anticsrf != session['anticsrf']:
        #     return 'Compra abortada porque el token antiCSRF no coincide'
        # session['anticsrf'] = None  # Evita reutilizar tokens
        
        insert = "INSERT INTO orders(user, num_items, address) VALUES (:user, :num_items, :address)"
        user = session['username']
        num_items = request.form['num_items']
        address = request.form['address']
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute(insert, {'user': user, 'num_items': num_items, 'address': address})
        app.logger.info(f'Se acaba de realizar una compra por {user} de {num_items} sacos de patatas a entregar'
                        f'en la dirección {address}')
        conn.commit()
        conn.close()
        return render_template('confirmacion.html', user=user, num_items=num_items, address=address)
    else:
        app.logger.info("Imposible procesar compra, usuario no autenticado")
        return "Imposible procesar compra, usuario no autenticado"
        
        
@app.route('/logout', methods=['GET'])
def logout():
    """Elimina los datos de la sesión actual y dirige a login"""
    session.clear()
    return redirect(url_for('login_form'))      



@app.route("/pagina_inocente", methods=['GET'])
def inocente():
    """ Esta página contiene un formulario con los datos escogidos por el atacante y un script que envía
        el formulario **automáticamente** en cuanto se carga la página inocente (petición falsificada).
        Tened en cuenta que el código de del formulario se podría haber 
        inyectado previamente mediante un ataque de XSS.
    """
    return render_template('pagina_inocente.html')


if __name__ == '__main__':
    reset_database()

    # Activa el depurador y recarga automáticamente
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['TEST'] = True
    # Imprescindible para usar sesiones
    app.config['SECRET_KEY'] = 'giw_clave_secreta'
    app.config['STATIC_FOLDER'] = 'static'
    app.config['TEMPLATES_FOLDER'] = 'templates'
    # Configuraciones de cookies de sesión
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # None, 'Lax', 'Strict'

    app.run()
