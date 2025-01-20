"""
TODO: rellenar

Asignatura: GIW
Práctica 6
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
from datetime import datetime
import requests

URL = 'https://gorest.co.in/'
TOKEN_GOREST = "token"

def inserta_usuarios(datos, token):
    """ Inserta todos los usuarios de la lista 
        y devuelve el número de usuarios insertados con éxito
    """
    if not isinstance(datos, list) or not isinstance(token, str):
        return 0
    cont_user = 0
    for user in datos:
        response = requests.post(f"{URL}public/v2/users",
                                 headers = { 'Authorization': f"Bearer {token}" },
                                 json=user,
                                 timeout=10)
        if response.status_code == 201:
            cont_user += 1

    return cont_user


def get_ident_email(email, token):
    """ Devuelve el identificador del usuario cuyo email sea *exactamente* el pasado como parámetro.
        En caso de que ese usuario no exista devuelve None """
    if not isinstance(email, str) or not isinstance(token, str):
        return None
    response = requests.get(f"{URL}public/v2/users?email={email}",
                            headers={'Authorization': f"Bearer {token}"},
                            timeout=10)
    if response.status_code == 200 and len(response.json()) > 0:
        return response.json()[0]['id']
    return None


def borra_usuario(email, token):
    """ Elimina el usuario cuyo email sea *exactamente* el pasado como parámetro. 
        En caso de éxito en el borrado devuelve True. 
        Si no existe tal usuario devolverá False """
    user_id = get_ident_email(email, token)
    if user_id is None:
        return False
    response = requests.delete(f"{URL}public/v2/users/{user_id}",
                            headers= {'Authorization':  f"Bearer {token}" },
                            timeout=10)
    return response.status_code == 204


def inserta_todo(email, token, title, due_on, status='pending'):
    """ Inserta un nuevo ToDo para el usuario con email exactamente igual al pasado. 
        Si el ToDo ha sido insertado con éxito devolverá True, en otro caso devolverá False """
    if email is None or token is None:
        return False

    ident = get_ident_email(email, token)
    if ident is None:
        return False

    return requests.post(f"{URL}/public/v2/users/{ident}/todos",
                        headers={"Authorization": f"Bearer {token}"},
                        data={"title": title,
                              "due_on": due_on,
                              "status": status}, 
                        timeout=5).status_code == 201


def lista_todos(email, token):
    """ Devuelve una lista de diccionarios con todos los ToDo asociados al usuario con el 
        email pasado como parámetro """
    user_id = get_ident_email(email, token)
    if user_id is None:
        return []
    response = requests.get(f"{URL}public/v2/users/{user_id}/todos",
                            headers={'Authorization' : f"Bearer {token}"},
                            timeout=10)
    if response.status_code == 200:
        return response.json()
    return []

def lista_todos_no_cumplidos(email, token):
    """ Devuelve una lista de diccionarios con todos los ToDo asociados al usuario con el 
        email pasado como parámetro que están pendientes (status=pending) y cuya fecha 
        tope (due_on) es anterior a la fecha y hora actual. Para comparar las fechas 
        solo hay que tener en cuenta el dia, la hora y los minutos; es decir, 
        ignorar los segundos, microsegundos y el uso horario """

    todas_tareas = lista_todos(email, token)
    tareas_no_cumplidas = []
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M')

    for todo in todas_tareas:
        if todo["due_on"] is not None:
            # due_on = todo['due_on'].strftime('%Y-%m-%d %H:%M')
            due_on = datetime.strptime(todo['due_on'],
                                    '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%Y-%m-%d %H:%M')

            if todo['status'] == 'pending' and due_on >= fecha_actual:
                tareas_no_cumplidas.append(todo)

    return tareas_no_cumplidas
