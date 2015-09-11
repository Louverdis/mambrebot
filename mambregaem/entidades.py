# -*- coding: UTF-8 -*-
"""
Creado el 20/03/2015

@autor: Luis Mario Reyes
"""
import random


class Tributo:
    """Clase que representa a los participantes del juego"""

    def __init__(self, nombre, frase_asesinato=None, frase_counter=None):
        # Datos basicos
        self.nombre = nombre
        self.frase_asesinato = frase_asesinato
        self.frase_counter = frase_counter

        # Datos de control
        self.arma = None
        self.asesinatos = []
        self.interacciones = []
        self.inventario = Inventario()

    def __repr__(self, *args, **kwargs):
        return self.nombre

    def agregar_intereaccion(self, interaccion):
        self.interacciones.append(interaccion)

    def actualizar_arma(self):
        """Metodo que actualiza el arma equipada del tributo
        tras desechar la anterior
        """
        nueva_arma = None
        for objeto in self.inventario.objetos:
            if objeto is Arma:
                nueva_arma = objeto
                break
        self.arma = nueva_arma

    def set_arma_actual(self, arma):
        self.arma = arma

    def agregar_asesinato(self, tributo):
        self.asesinatos.append(tributo)

    def agregar_asesinatos(self, tributos):
        self.asesinatos.extend(tributos)

    def buscar_interaccion(self, tributo):
        """Metodo que busca alguna interaccion con el tributo dado.

        Parametros:
            @tributo: Tributo. El objeto usado para buscar la interaccion.

        Retorna: Interaccion.
        """
        for interaccion in self.interacciones:
            if tributo in interaccion.tributos:
                return interaccion
        return None

    def quitar_interaccion(self, interaccion):
        self.interacciones.remove(interaccion)


class Objeto:
    """Clase base para definir a los objetos utilizables por los
    tributos

    Parametros:
        @nombre: str. Nombre del objeto, usado para identificarlo
        @consumible: Boolean, indica si el objeto se descarta despues de
            usarse.
    """

    def __init__(self, nombre, consumible):
        self.nombre = nombre
        self.consumible = consumible

    def __repr__(self, *args, **kwargs):
        return self.nombre


class Arma(Objeto):
    """Clase que representa a las Armas, objetos que modifican el
    comportamiento de los combates

    Parametros:
        @nombre: str.
        @ejecucion: str. Cadena utilizada cuando se gana un combate con el
            arma.
        @ejecucion_multiple: str. Cadena utilizada cuando se gana un
            combate con el arma contra multiples oponentes.
    """

    def __init__(self, nombre, ejecucion, ejecucion_multiple, consumible=False):
        super(Arma, self).__init__(nombre, consumible)
        self.ejecucion = ejecucion
        self.ejecucion_multiple = ejecucion_multiple

    def ejecutar(self, multiple=False):
        if multiple:
            return self.ejecucion_multiple
        else:
            return self.ejecucion


class Trampa(Objeto):
    """Clase que representa a los objetos trampa.
    Son objetos utilizables por los tributos, siempre son consumibles, y
    poseen tres posibles resultados.

    Parametros:
        @texto: str. Texto desplegado al usar la trampa
        @ejecucion: str. Texto usado cuando el arma tiene exito.
        @desarme: str. Texto usado cuando el objetivo logra evitar la
            trampa.
        @suicidio: str. Texto usado cuando el tributo cae en su propia
            trampa.
    """

    def __init__(self, nombre, texto, ejecucion, desarme, suicidio):
        super(Trampa, self).__init__(nombre, True)
        self.texto = texto
        self.ejecucion = ejecucion
        self.desarme = desarme
        self.suicidio = suicidio

    def ejecutar_accion(self, activo, pasivo):
        """Metodo que acciona la trampa. Se decide que resultado
        tendra esta accion.

        Parametros:
            @activo: Tributo. El tributo que pretende accionar la trampa.
            @pasivo: Tributo. El tributo objetivo.

        Retorna: tupla, (str, tributo). Tupla que representa el texto
            del resultado de la trampa, junto al Tributo eliminado.
        """
        _str = self.texto.format(activo.nombre, pasivo.nombre) + ". "

        interaccion = activo.buscar_interaccion(pasivo)

        if interaccion is not None:
            _str += (
                "Pero " + activo.nombre + " recuerda cuando " +
                interaccion.identificador + " con " + pasivo.nombre +
                " y opta por quitar la trampa."
            )
            activo.quitar_interaccion(interaccion)
            return _str, None

        r = random.randrange(0, 100)

        if r <= 40:
            _str += self.ejecucion.format(activo.nombre, pasivo.nombre)
            activo.agregar_asesinato(pasivo)
            return _str, pasivo

        elif r > 40 or r <= 80:
            _str += self.desarme.format(activo.nombre, pasivo.nombre)
            return _str, None

        else:
            _str += self.suicidio.format(activo.nombre, pasivo.nombre)
            pasivo.agregar_asesinato(activo)
            return _str, activo


class Inventario:
    """Clase para el control de inventarios de los tributos
    """

    def __init__(self, capacidad=3):
        self.objetos = []
        self._capacidad = capacidad

    @property
    def capacidad(self):
        return self._capacidad

    @capacidad.setter
    def capacidad(self, value):
        if value < 0:
            self._capacidad = 0
        else:
            self._capacidad = value

    def agregar_objeto(self, objeto):
        """Metodo que agrega un objeto al inventario solo cuando es posible.
        Reporta el resultado.
        """
        if len(self.objetos) == self.capacidad:
            return False
        self.objetos.append(objeto)
        return True

    def quitar_objeto(self, objeto):
        self.objetos.remove(objeto)
