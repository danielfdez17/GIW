# -*- coding: utf-8 -*-
"""
@author: Enrique Martín Martín
@email: emartinm@ucm.es
"""

from flask import Flask, request, render_template
import sqlite3
import os
import re

DBPATH = 'database.db'
SQLPATH = 'database.sql'

app = Flask(__name__)


def reset_database():
    """Elimina el fichero database.db (si existe) y lo crea con los valores por defecto"""
    try:
        os.remove(DBPATH)
    except FileNotFoundError:
        pass

    with sqlite3.connect(DBPATH) as conn:
        # cur = conn.cursor()
        with open(SQLPATH, 'r', encoding='ascii') as script_file:
            script = script_file.read()
            conn.executescript(script)
            conn.commit()


# Uso legítimo: pedidos de un usuario
# * http://localhost:5000/orders?user=pepe@gmail.com
# * http://localhost:5000/orders?user=eva@yahoo.es
#
# Inyección SQL:
# * Mostrar los pedidos de todos los usuarios
# http://localhost:5000/orders?user=NADA' or 'a'='a
# * Mostrar los contenidos de la tabla de usuarios, incluyendo emails y hashes
# http://localhost:5000/orders?user=NADA' union select -99, email, password from users--
# * Mostrar los contenidos de la tabla de usuarios, incluyendo emails y hashes pero también paises
# http://localhost:5000/orders?user=NADA' union select -99, country, email || '---' || password from users--
# * Mostrar la definición de todas las tablas de la BD:
# http://localhost:5000/orders?user=NADA' union select -99, sql, 'dummy' from sqlite_master--


@app.route('/orders', methods=['GET'])
def orders():
    u = request.args.get('user')
    query = f"SELECT id, user, item FROM orders WHERE user='{u}'"

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(query)
    results = cur.fetchall()
    conn.close()

    return render_template("items.html", query=query, results=results)


def safe_user(user):
    """Comprueba que user es un email válido usando regex"""
    return (re.match(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", user)) is not None
    # return True


@app.route('/orders_safer', methods=['GET'])
def orders_safer():
    u = request.args.get('user')
    if not safe_user(u):
        return "Error en los parmámetros"
    # Usamos consulta preconstruida para mitigar inyección SQL
    query = f"SELECT id, user, item FROM orders WHERE user=:user"

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(query, {'user': u})
    results = cur.fetchall()
    conn.close()

    return render_template("items.html", query=query, results=results)


if __name__ == '__main__':
    # Activa el depurador y recarga automáticamente
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['TEST'] = True

    # Imprescindible para usar sesiones
    app.config['SECRET_KEY'] = 'giw_clave_secreta'

    app.config['STATIC_FOLDER'] = 'static'
    app.config['TEMPLATES_FOLDER'] = 'templates'

    app.run()
