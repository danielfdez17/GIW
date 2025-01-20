"""
TODO: rellenar

Asignatura: GIW
Práctica 7
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

from flask import Flask, request, jsonify
from jsonschema import validate, ValidationError
app = Flask(__name__)



#Creamos una clase Fake que simule una base de datos
class AsignaturasFakeDB:
    """
        Clase que simula una base de datos de asignaturas
        Tendremos una lista de asignaturas y un contador de ids para asignar a cada asignatura
    """
    def __init__(self):
        self.asignaturas = {}
        self.contar_ids = 0
    def reset(self):
        """
        Elimina todas las asignaturas de la lista.
        """
        self.asignaturas = {}
        self.contar_ids = 0
    def add(self, asignatura):
        """
        Añade una asignatura a la lista y le asigna un ID único.
        """
        self.contar_ids += 1
        asignatura['id'] = self.contar_ids
        self.asignaturas[self.contar_ids] = asignatura
    def get(self):
        """
        Devuelve una lista de asignaturas
        """
        return list(self.asignaturas.values())
    def delete_asig(self, ident):
        """
        Borra una asignatura dado su identificador si existe
        """
        if ident not in self.asignaturas:
            return False
        del self.asignaturas[ident]
        return True

    def get_asig(self, ident):
        """
        Devuelve la asignatura con el identificador 'ident' o None si no existe
        """
        return self.asignaturas.get(ident, None)

    def replace_asig(self, ident, asignatura):
        """
        Actualiza el contenido de la asignatura con identificador 'ident' si existe
        Si la asignatura existe, se actualiza y devuelve True. Devuelve False en caso contrario
        """
        if ident in self.asignaturas:
            asignatura['id'] = ident
            self.asignaturas[ident] = asignatura
            return True
        return False

asignaturas_db = AsignaturasFakeDB()

###
### <DEFINIR AQUI EL SERVICIO REST>
###
ASIG_SCHEMA = {
    "type": "object",
    "properties": {
        "nombre": {"type": "string"},
        "numero_alumnos": {"type": "number"},
        "horario": {"type": "array"}
    }
}
def check_input(data):
    """
    Devuelve True si la asignatura está bien formada para se añadida
    a la BD, y False en caso contrario
    """
    validate(instance=data, schema=ASIG_SCHEMA)
    return True
    # return len(data) == 3 and isinstance(data, dict) \
    # and "nombre" in data \
    # and isinstance(data["nombre"], str) \
    # and "numero_alumnos" in data \
    # and isinstance(data["numero_alumnos"], int) \
    # and "horario" in data \
    # and isinstance(data["horario"], list) \
    # and len(data["horario"]) != 0

HORARIO_SCHEMA = {
    "type": "object",
    "properties": {
        "dia": {"type": "string"},
        "hora_inicio": {"type": "number"},
        "hora_final": {"type": "number"}
    }
}


def check_horario(horario):
    """
    Devuelve True si el horario está bien formado, y False en caso
    contrario
    """
    validate(instance=horario, schema=HORARIO_SCHEMA)
    return True
    # return isinstance(horario, dict) \
    # and "dia" in horario \
    # and isinstance(horario["dia"], str) \
    # and "hora_inicio" in horario \
    # and isinstance(horario["hora_inicio"], int) \
    # and not isinstance(horario["hora_inicio"], bool) \
    # and "hora_final" in horario \
    # and isinstance(horario["hora_final"], int) \
    # and not isinstance(horario["hora_final"], bool)

@app.route('/asignaturas', methods=['DELETE'])
def delete_all_asignaturas():
    """
    Elimina todas las asignaturas que existan en la lista de asignaturas
    Returns: Devuelve un 204 si se ha eliminado correctamente
    """
    asignaturas_db.reset()
    return '', 204

@app.route('/asignaturas', methods=['POST'])
def add_asignatura():
    """
    Añade una asignatura a la lista de asignaturas.
    Si la asignatura no cumple con el esquema o tiene
    tipos incorrectos en los campos, se devolverá el código «400 Bad Request»
    Returns: Devuelve un 201 si se ha añadido correctamente.
    """
    try:
        data = request.get_json()
        if not check_input(data):
            return '', 400

        for horario in data['horario']:
            if not check_horario(horario):
                return '', 400

        asignaturas_db.add(data)
        dicc_id = {'id': data['id']}
        return dicc_id, 201
    except ValueError:
        return '', 400

@app.route('/asignaturas', methods=['GET'])
def get_asignaturas():
    """
    Devuelve la lista de asignaturas.
    Returns: Devuelve un 200 si se ha devuelto correctamente.
    """
    try:
        page = request.args.get('page', type=int)
        per_page = request.args.get('per_page', type=int)
        alumnos_gte = request.args.get('alumnos_gte', type=int)
        if (page is None and per_page is not None) or \
           (page is not None and per_page is None):
            raise ValueError('Parámetros incorrectos')
        asignaturas_filter = asignaturas_db.get()
        total_asignaturas = len(asignaturas_filter)
        if alumnos_gte is not None:
            asignaturas_filter = [
                asignatura for asignatura in asignaturas_filter
                if asignatura['numero_alumnos'] >= alumnos_gte
            ]
        if page is not None and per_page is not None:
            inicio_filtro = (page - 1) * per_page
            end_filtro = inicio_filtro + per_page
            asignaturas_filter = asignaturas_filter[inicio_filtro:end_filtro]
        total_asignaturas_filtradas = len(asignaturas_filter)
        status_code = 200 if total_asignaturas == total_asignaturas_filtradas else 206
        resultado = {
            "asignaturas": [f"/asignaturas/{a['id']}" for a in asignaturas_filter]
        }
        return resultado, status_code
    except TypeError:
        return '', 400
    except ValueError:
        return '', 400

@app.route("/asignaturas/<int:ident>", methods=["DELETE"])
def delete_asignatura(ident):
    """
    Elimina una asignatura específica dado su ID.
    Returns: Devuelve un 204 si la asignatura se ha eliminado correctamente,
    o un 404 si la asignatura no existe.
    """
    is_deleted = asignaturas_db.delete_asig(ident)
    if is_deleted:
        return "", 204
    return "", 404

@app.route("/asignaturas/<int:ident>", methods=["GET"])
def get_asignatura(ident):
    """
    Obtiene una asignatura específica dado su ID.
    Returns: Devuelve un 200 si la asignatura se ha encontrado correctamente,
    o un 404 si la asignatura no existe.
    """

    asignatura = asignaturas_db.get_asig(ident)

    if asignatura:
        return jsonify(asignatura), 200
    return jsonify({"error": "Asignatura no encontrada"}), 404

@app.route("/asignaturas/<int:ident>", methods=["PUT"])
def put_asignatura(ident):
    """
    Reemplaza una asignatura específica dada su ID.
    Returns: Devuelve un 200 si la asignatura se ha reemplazado correctamente,
    un 404 si la asignatura no existe, o un 400 si la petición está mal formada.
    """
    asignatura = asignaturas_db.get_asig(ident)
    if not asignatura:
        return '', 404

    data = request.get_json()

    try:
        if not check_input(data):
            return '', 400

        for horario in data['horario']:
            if not check_horario(horario):
                return '', 400

        if asignaturas_db.replace_asig(ident, data):
            return jsonify(data), 200
        return '', 404

    except ValidationError:
        return '', 400


@app.route("/asignaturas/<int:ident>", methods=["PATCH"])
def patch_asignatura(ident):
    """
    Actualiza un campo específico de una asignatura dada su ID.
    Returns: Devuelve un 200 si la asignatura se ha actualizado correctamente,
    un 404 si la asignatura no existe, o un 400 si la petición está mal formada.
    """
    asignatura = asignaturas_db.get_asig(ident)
    if asignatura is None:
        return jsonify({"error": "La asignatura no se ha encontrado"}), 404

    data = request.get_json()
    if not isinstance(data, dict) or len(data) != 1:
        return jsonify ({"error": "La petición está mal formada, tiene más de un campo"}), 400

    campos_esperados = {
        "nombre": str,
        "numero_alumnos": int,
        "horario": list
    }
    key, value = list(data.items())[0]
    print(f"key: {key}, value: {value}")
    if key in campos_esperados and isinstance(value, campos_esperados[key]):
        if key == "horario":
            for horario in value:
                if not check_horario(horario):
                    return jsonify({"error": "La petición está mal formada"}), 400
        asignatura[key] = value
    else:
        return jsonify({"error": "Campo no válido o tipo incorrecto"}), 400

    return jsonify(asignatura), 200

@app.route("/asignaturas/<int:ident>/horario", methods=["GET"])
def get_horario_asignatura(ident):
    """
    Obtiene el horario de una asignatura específica dada su ID.
    Returns: Devuelve un 200 si el horario se ha encontrado correctamente,
    o un 404 si la asignatura no existe.
    """
    asignatura = asignaturas_db.get_asig(ident)
    if asignatura:
        return jsonify({"horario": asignatura["horario"]}), 200
    return jsonify({"error": "La asignatura no se ha encontrado"}), 404


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
