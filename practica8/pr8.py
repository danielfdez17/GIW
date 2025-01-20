"""
TODO: rellenar

Asignatura: GIW
Práctica 8
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
from mongoengine import Document, StringField, IntField, ListField, ReferenceField,\
    FloatField, ComplexDateTimeField, ValidationError, \
    EmbeddedDocumentListField, EmbeddedDocument, \
    PULL, DynamicField

DATABASE_NAME = "giw_mongoengine"
###
### <DEFINIR AQUÍ LAS CLASES DE MONGOENGINE>
###


# Airam
class Tarjeta(EmbeddedDocument):
    """Clase que almacena la representación de una tarjeta en una base de datos MongoDB"""
    nombre = StringField(required=True, min_length=2)
    numero = StringField(required=True, min_length=16, max_length=16)
    mes = StringField(required=True, min_length=2, max_length=2)
    year = StringField(required=True, min_length= 2, max_length=2)
    cvv = StringField(required=True, min_length= 3, max_length=3)
    def clean(self):
        """Validación personalizada"""
        try:
            numero = int(f"{self.numero}")
            mes = int(f"{self.mes}")
            year = int(f"{self.year}")
            cvv = int(f"{self.cvv}")
        except ValueError as exc:
            raise ValidationError("número, mes, año o CVV contienen valores no numéricos.") from exc
        if not isinstance (numero, int) and not isinstance(mes, int) \
            and not isinstance (year, int) and not isinstance (cvv, int):
            raise ValidationError("""Tarjetas con datos invalidos""")


    def show(self):
        """Muestra una tarjeta por pantalla"""
        print(f"""
            Nombre: {self.nombre},
            numero: {self.numero},
            mes: {self.mes},
            year: {self.year},
            cvv: {self.cvv}
        """)
def is_ean13(codigo):
    """
    Valida que el código EAN13 tenga un dígito de control correcto.
    :param codigo: Cadena de 13 dígitos.
    :return: True si el dígito de control es correcto, False en caso contrario.
    """
    if not isinstance(codigo, str):
        return False

    if not codigo.isdigit() or len(codigo) != 13:
        return False

    digits = [int(d) for d in codigo]
    suma_impares = 0
    suma_pares = 0
    for i in range(12):
        if i % 2 == 0:
            suma_impares += digits[i]
        else:
            suma_pares += digits[i]
    # Calcular el total según el estándar EAN-13
    total = suma_impares + suma_pares * 3

    # Calcular el dígito de control esperado
    digito_control_calculado = (10 - (total % 10)) % 10
    return digito_control_calculado == digits[12]

def is_natural_number(number):
    """Comprueba que es 'number' es un número natural"""
    return isinstance(number, int) and number >= 0
# Daniel
class Producto(Document):
    """
    Clase que almacena la representación de un producto en una base de datos MongoDB

    NOTA: nos falla el test_producto_invalido en el producto con 
    categoria_principal=False porque se parsea automáticamente a entero, se 
    ha cambiado el IntField a DynamicField y ahora ya no parsea el False
    automaticamente a 0.
    Por lo tanto se ha cambiado categorias secundarias ya que en caso
    de ser una lista [False, 1, 2] lo convertiria a [0, 1, 2] lo
    cual es erroneo
    """
    codigo_barras = StringField(primary_key=True, regex=r"^\d{13}$")
    nombre = StringField(required=True, min_length=2)
    categoria_principal = DynamicField(required=True)
    categorias_secundarias = ListField(DynamicField(min_value=0))
    def clean(self):
        """Validación personalizada"""
        if not is_ean13(self.codigo_barras):
            raise ValidationError("""
                El código de barras EAN13 es inválido (dígito de control incorrecto).
            """)

        if not is_natural_number(self.categoria_principal):
            raise ValidationError(f"""
                La categoría principal solo acepta números enteros: {self.categoria_principal}
            """)

        if not isinstance(self.categorias_secundarias, list):
            raise ValidationError("La categoría secundaria no es lista")

        for c in self.categorias_secundarias:
            if not is_natural_number(c):
                raise ValidationError("Valor: {c} en categorías secundaria no es natural")

        if len(self.categorias_secundarias) > 0 and \
            self.categorias_secundarias[0] != self.categoria_principal:
            raise ValidationError("""
                La categoría principal debe ser la primera en categorias_secundarias.
            """)


    def show(self):
        """Muestra un producto por pantalla"""
        print(f"""
            Nombre: {self.nombre},
            Código de barras: {self.codigo_barras},
            Categoría principal: {self.categoria_principal},
            Categorías secundarias: {self.categorias_secundarias}
        """)

# Daniel
class Linea(EmbeddedDocument):
    """
    Clase que almacena la representación de una línea de pedido en una base de datos MongoDB
    """
    num_items = IntField(required=True, min_value=0)
    precio_item = FloatField(required=True, min_value=0.0)
    nombre_item = StringField(required=True, min_length=2)
    total = FloatField(required=True, min_value=0.0)
    producto = ReferenceField(Producto, required=True)
    def clean(self):
        """Validación personalizada"""
        if not self.producto:
            raise ValidationError(f"Producto inexistente: {self.nombre_item}")
        if not self.num_items:
            raise ValidationError(f"No se han comprado productos: {self.num_items}")
        if not isinstance(self.num_items, int):
            raise ValidationError(f"num_items solo puede ser entero: {self.num_items}")
        if not self.precio_item:
            raise ValidationError(f"El producto no tiene precio: {self.precio_item}")
        if not isinstance(self.precio_item, float):
            raise ValidationError(f"precio_item solo puede ser float: {self.precio_item}")
        if self.nombre_item != self.producto.nombre:
            raise ValidationError(f"""
                El nombre de la linea y del producto no coinciden: 
                {self.nombre_item}, {self.producto.nombre}
            """)
        if self.num_items * self.precio_item != self.total:
            raise ValidationError("""
                                  La suma total de los productos no coincide con el total de la línea
                                  """)
    def show(self):
        """Muestra por pantalla la línea"""
        print(f"""
            Nombre: {self.nombre_item},
            Número de items: {self.num_items},
            Precio unitario del item: {self.precio_item},
            Precio total: {self.total},
            Producto referenciado: {self.producto}
        """)

# Luis
class Pedido(Document):
    """ 
    Clase que almacena la representación de un pedido en una base de datos MongoDB
    """
    total = FloatField(min_value=0.0, required=True)
    fecha = ComplexDateTimeField(required=True)
                                #  .strf(",".join(["%Y", "%m", "%d", "%H", "%M", "%S", "%f"])))
    lineas = EmbeddedDocumentListField(Linea, required=True)

    def clean(self):
        """Validación personalizada"""
        if not self.lineas or not isinstance(self.lineas, list):
            raise ValidationError(f"Las lineas de pedido deben ser una lista: {self.lineas}")
        precio_total = 0
        for linea in self.lineas:
            precio_total += linea.total
        # precio_total = sum(linea.total for linea in self.lineas)
        if self.total != precio_total:
            raise ValidationError("""
                El precio total del pedido no coincide con la suma de las líneas
            """)

        productos = set()
        for linea in self.lineas:
            if linea.producto in productos:
                raise ValidationError("No puede haber dos líneas con el mismo producto")
            productos.add(linea.producto)

    def show(self):
        """Muestra por pantalla el pedido y las líneas del pedido"""
        print(f"Precio total del pedido: {self.total}")
        print(f"Fecha del pedido: {self.fecha}")
        print("Lista de líneas del pedido:")
        for linea in self.lineas:
            print(f""" - Producto: {linea.nombre_item},
                  Cantidad: {linea.num_items}, 
                  Total: {linea.total}""")

# Jose
class Usuario(Document):
    """
        Definimos la entidad Usuario

        NOTA: en el array USUARIOS_INCORRECTOS hay algunos usuarios con el dni acorde
        al formato español, le cambiamos la letra a minúscula y los test pasaban correctamente
    """
    dni = StringField(primary_key=True, required=True, regex=r"[0-9]{8}[A-Z]")
    nombre = StringField(required=True, min_length=2)
    apellido1 = StringField(required=True, min_length=2)
    apellido2 = StringField(required=False)
    f_nac = StringField(required=True)
    tarjetas = EmbeddedDocumentListField(Tarjeta)
    pedidos = ListField(ReferenceField(Pedido, reverse_delete_rule=PULL))
    def clean(self):
        """Validación personalizada"""
        try:
            datetime.fromisoformat(f"{self.f_nac}")
        except ValueError as exc:
            raise ValidationError("Formato incorrecto, deberia ser AAAA-MM-DD") from exc
    def show(self):
        """Muestra por pantalla el usuario"""
        print(f"DNI: {self.dni}")
        print(f"Nombre: {self.nombre}")
        print(f"Apellido 1: {self.apellido1}")
        print(f"Apellido 2: {self.apellido2}")
        print(f"Fecha de nacimiento: {self.f_nac}")
        print("Tarjetas:")
        for tarjeta in self.tarjetas:
            print(f" - {tarjeta}")
        print("Pedidos:")
        for pedido in self.pedidos:
            print(f" - {pedido}")
    