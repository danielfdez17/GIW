"""
TODO: rellenar

Asignatura: GIW
Práctica 5
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

from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import mechanicalsoup

URL = 'https://books.toscrape.com/'
DICC_VALORACIONES = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

# APARTADO 1 #
def explora_categoria(url):
    """ A partir de la URL de la página principal de una categoría, devuelve el nombre
        de la categoría y el número de libros """
    res = requests.get(url, timeout=5)
    res.encoding = res.apparent_encoding
    html = res.text
    soup = BeautifulSoup(html, "html.parser")
    categoria = soup.strong.text.strip()
    resultados = soup.form.strong.text.strip()
    return (categoria, resultados)


def categorias():
    """ Devuelve un conjunto de parejas (nombre, número libros) de todas las categorías """
    res = requests.get(URL, timeout=5)
    res.encoding = res.apparent_encoding
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    lista_categorias = soup.css.select_one("ul.nav-list").li.ul
    lista = [categoria for categoria in lista_categorias if categoria.name == "li"]
    conjunto = set()
    for li in lista:
        conjunto.add(explora_categoria(URL + li.a.get("href", None)))

    return sorted(conjunto)

# APARTADO 2 #
def url_categoria(nombre):
    """ Devuelve la URL de la página principal de una categoría a partir de su nombre (ignorar
        espacios al principio y final y también diferencias en mayúsculas/minúsculas) 
        strip(): Limpia los espacios en blanco    
        lower(): Convierte el texto a minúsculas
    """
    if nombre is None:
        return None
    res = requests.get(URL, timeout=5)#tiempo de espera de 5 segundos, sugerencia del PyLint
    if res.status_code != 200:#Si no devuelve un 200, no tratamos el html, sugerencia del PyLint
        return None

    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    lista_categorias = soup.css.select_one("ul.nav-list").li.ul
    nombre = nombre.strip().lower()
    for categoria in lista_categorias:
        if categoria is None or categoria.text is None:
            continue
        nombre_categoria = categoria.text.strip().lower()
        if nombre_categoria == nombre and categoria.a is not None:
            return URL + categoria.a.get("href")

    return None

def todas_las_paginas(url):
    """ Sigue la paginación recopilando todas las URL *absolutas* atravesadas 
    NOTA: sabemos que lo podemos hacer tanto con beautiful soup como con mechanical soup
        y que solo sería necesario cambiar pocas líneas para hacer que funcione con beautiful soup.
        Queríamos esperar al laboratorio para preguntarte cuál era mejor opción 
        (a pesar que no es necesario rellenar ningún campo) y nos comentaste 
        que te lo dijéramos al realizar la entrega. 
    """
    browser = mechanicalsoup.StatefulBrowser()
    paginas = [url]
    browser.open(url)
    next_button = browser.page.find('li', class_='next')

    while next_button:
        next_url = next_button.find('a')['href']
        next_url = urljoin(browser.get_url(), next_url)
        paginas.append(next_url)
        browser.open(next_url)
        next_button = browser.page.find('li', class_='next')

    return paginas

def libros_categoria(nombre):
    """ Dado el nombre de una categoría, devuelve un conjunto de tuplas 
        (titulo, precio, valoracion), donde el precio será un número real y la 
        valoración un número natural """

    url = url_categoria(nombre)
    if not url:
        return set()

    paginas = todas_las_paginas(url)
    tuplas = set()


    for pag in paginas:

        try:
            response = requests.get(pag, timeout=5)
            response.encoding = 'utf-8'
            html = response.text
        except requests.RequestException:
            continue

        soup = BeautifulSoup(html, 'html.parser')

        libros = soup.find_all("article", class_="product_pod")

        for libro in libros:
            titulo = libro.find("h3").find("a")["title"]

            precio_aux = libro.find("p", class_="price_color").get_text(strip=True)
            precio = float(precio_aux.replace('Â£', '').replace('£', '').strip())

            valoracion_aux = libro.find("p", class_="star-rating")["class"][1]
            valoracion = DICC_VALORACIONES.get(valoracion_aux, 0)

            tuplas.add((titulo, precio, valoracion))

    return tuplas
