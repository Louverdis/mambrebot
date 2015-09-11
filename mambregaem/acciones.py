# -*- coding: UTF-8 -*-

__author__ = 'Luis Mario Reyes'

import random

from mambregaem.entidades import Arma


class Interaccion:
    """Clase que representa los objetos de Interaccion.
    Estos objetos son usados durante las interacciones amistosas entre
    los tributos.

    Parametros:
        @texto: str. Texto usado para representar la interaccion.
        @identificador: str. Texto usado para referenciar la interaccion
            en otros contextos
        @*tributos: Integrantes de la interaccion.
    """

    def __init__(self, texto, identificador, *tributos):
        self.tributos = tributos
        self.texto = texto.format(*tributos)
        self.identificador = identificador

    def ejecutar_interaccion(self):
        """Retorna: Texto representante de la interaccion.
        """
        for tributo in self.tributos:
            tributo.agregar_intereaccion(self)
        return self.texto


class Combate:
    """Clase combate
    Accion entre dos Tributos con resultados normalmente fatales.
    Se toma encuenta las armas e interacciones pasadas para resolver
    el resultao de esta.
    """

    def __init__(self, activo, pasivo, texto):
        super(Combate, self).__init__()
        self.activo = activo
        self.pasivo = pasivo
        self.texto = texto.format(activo.nombre, pasivo.nombre)

    def ejecutar_combate(self, interacciones_activas):
        """Metodo encargado de calcular los resultado de un combate entre
        los dos tributos. Se asume que el tributo activo es quien
        inicia el combate.

        Retorna: tupla(str,Tributo). Texto que representa los resultados
            del combate y tributo eliminado
        """
        _str = self.texto + ". "

        # Se buscan interacciones pasadas. Si hay un positivo, el evento
        # no tiene resultados fatales.
        interaccion = self.activo.buscar_interaccion(self.pasivo)
        # print("Debug en interacciones, combate:")
        # print(interacciones_activas)
        if (interaccion is not None) and interacciones_activas:
            _str += (
                "Pero " + self.activo.nombre + " recuerda cuando " +
                interaccion.identificador + " con " + self.pasivo.nombre +
                " y decide detenerse."
            )
            self.activo.quitar_interaccion(interaccion)
            return _str, None

        # Verificacion y resolucion de combate armado
        objetos_activo = self.activo.inventario.objetos
        objetos_pasivo = self.pasivo.inventario.objetos
        arma_activo = self.activo.arma
        arma_pasivo = self.pasivo.arma

        # Caso a: Activo esta armado y Pasivo desarmado
        if arma_activo is not None and arma_pasivo is None:
            r = random.randrange(0, 100)
            # Muere Pasivo (80%)
            if r <= 80:
                _str += (
                    self.activo.nombre + " hace uso de su " + arma_activo.nombre + ". " +
                    arma_activo.ejecutar().format(self.activo.nombre, self.pasivo.nombre) + ".\n" +
                    "\"{0}\"-Dice {1} mientras se retira".format(
                        self.activo.frase_asesinato, self.activo.nombre)
                )
                # Actualizar inventario
                if arma_activo.consumible:
                    self.activo.inventario.quitar_objeto(arma_activo)
                    self.activo.actualizar_arma()
                # Registrar asesinato
                self.activo.agregar_asesinato(self.pasivo)
                return _str, self.pasivo

            # Escapa pasivo(10%)
            elif 80 < r <= 90:
                _str += (
                    "Pero a {0} se le escapa el objetivo.".format(
                        self.activo.nombre)
                )
                return _str, None

            # Muere Activo(10%)
            else:
                _str += (
                    "Pero a {0} no le parecio divertido, asi que le quita a {1} su {2} y lo ataca.\n".format(
                        self.pasivo.nombre, self.activo.nombre, arma_activo.nombre) +
                    arma_activo.ejecutar().format(self.pasivo.nombre, self.activo.nombre) + ".\n" +
                    "\"{0}\"-Dice {1} mientras ser burla del cadaver.\n".format(
                        self.pasivo.frase_counter, self.pasivo.nombre)
                )
                if not arma_activo.consumible:
                    # Actualizar inventarios.
                    r = self.pasivo.inventario.agregar_objeto(arma_activo)
                    if r:
                        _str += ("Por sus molestias {0} decide quedarse con el arma.".format(self.pasivo.nombre))
                    else:
                        _str += ("{0} Intenta tomar el arma, pero ya no tiene espacio en donde guardarla.".format(
                            self.pasivo.nombre))
                # Registrar asesinato
                self.pasivo.agregar_asesinato(self.activo)
                return _str, self.activo

        # Caso b: Activo esta desarmado y Pasivo armado
        if arma_activo is None and arma_pasivo is not None:
            _str += (
                "Pero {0} no noto que {1} tenia en manos su {2} quien contrataca.\n".format(
                    self.activo.nombre, self.pasivo.nombre, arma_pasivo.nombre)
            )
            r = random.randrange(0, 100)
            # Muere Activo (80%)
            if r <= 80:
                _str += (
                    arma_pasivo.ejecutar().format(self.pasivo.nombre, self.activo.nombre) + "\n" +
                    "\"{0}\"-Dice {1} mientras mira con rencor al cadaver.".format(
                        self.pasivo.frase_counter, self.pasivo.nombre)
                )
                # Actualizar inventario
                if arma_pasivo.consumible:
                    self.pasivo.inventario.quitar_objeto(arma_pasivo)
                    self.pasivo.actualizar_arma()
                # Registrar asesinato
                self.pasivo.agregar_asesinato(self.activo)
                return _str, self.activo

            # Escapa Activo(10%)
            elif 80 < r <= 90:
                _str += (
                    "Afortunadamente, {0} logra ser mas rapido y escapa.".format(
                        self.activo.nombre)
                )
                return _str, None

            # Muere Pasivo(10%)
            else:
                _str += (
                    "Pero {0} demuestra una astusia superior leyendo todos los movimientos de {1}. {0} rapidamente se "
                    "cansa de jugar y le quita el arma a {1}.\n".format(
                        self.activo.nombre, self.pasivo.nombre, arma_pasivo.nombre) +
                    arma_pasivo.ejecutar().format(self.activo.nombre, self.pasivo.nombre) + "\n" +
                    "\"{0}\"-Dice {1} de brazos cruzados, como si le diera una leccion al cadaver de su "
                    "rival.\n".format(
                        self.activo.frase_counter, self.activo.nombre)
                )
                if not arma_pasivo.consumible:
                    # Actualizar inventarios.
                    r = self.activo.inventario.agregar_objeto(arma_pasivo)
                    if r:
                        _str += ("Por sus molestias {0} decide quedarse con el arma.".format(self.activo.nombre))
                    else:
                        _str += ("{0} Intenta tomar el arma, pero ya no tiene espacio en donde guardarla.".format(
                            self.activo.nombre))
                # Registrar asesinato
                self.pasivo.agregar_asesinato(self.activo)
                return _str, self.activo

        # Caso c: Activo y Pasivo estan armados
        if arma_activo is not None and arma_pasivo is not None:
            # Obteniendo datos necesarios
            armas_activo = [arma_activo]
            armas_pasivo = [arma_pasivo]

            for objeto in objetos_activo:
                if type(objeto) is Arma:
                    armas_activo.append(objeto)

            for objeto in objetos_pasivo:
                if type(objeto) is Arma:
                    armas_pasivo.append(objeto)

            # print("Debug de combate, caso C:")
            # print(len(armas_activo))
            # print(objetos_activo)
            # print(len(armas_pasivo))
            # print(objetos_pasivo)
            # Caso c.1: Activo posee mas armas que Pasivo
            if len(armas_activo) > len(armas_pasivo):
                r = random.randrange(0, 100)
                # Muere pasivo(95%)
                if r <= 95:
                    _str += (
                        "{0} Avanza amenazante con su {1}.\nEn respuesta {2} prepara su {3}. {0} No se deja vencer, "
                        "mostrando el resto de su arsenal: {4}\n{2} Queda sorprendido, y justo en ese momento {0} Usa "
                        "en conjunto todo lo que tiene, destruyendo todo a su paso. {2} Es vencido en un "
                        "instante.\n".format(
                            self.activo.nombre, arma_activo.nombre, self.pasivo.nombre, arma_pasivo.nombre,
                            " y ".join([a.nombre for a in armas_activo])
                        ) +
                        "\"{0}\"-Dice {1} Mientras mira los no existentes restos de su oponente.\n".format(
                            self.activo.frase_asesinato, self.activo.nombre)
                    )
                    # Registrar asesinato
                    self.activo.agregar_asesinato(self.pasivo)
                    return _str, self.pasivo

                # Escapa pasivo(5%)
                else:
                    _str += (
                        "{0} Se rinde al notar todas la armas de {1}.\n{0} Decide arrojar su {1} a modo de distraccion "
                        "y logra escapar.".format(
                            self.pasivo.nombre, arma_pasivo.nombre
                        )
                    )
                    # Actualizar Inventario
                    self.pasivo.inventario.quitar_objeto(arma_pasivo)
                    self.pasivo.actualizar_arma()
                    return _str, None

            # Caso c.2: Pasivo posee mas armas que Activo
            if len(armas_activo) < len(armas_pasivo):
                r = random.randrange(0, 100)
                # Muere Activo(95%)
                if r <= 95:
                    _str += (
                        "{0} Corre confiado contra {1}.\nSin embargo {1} solo mira encantado a su atacante antes de "
                        "comenzar a reir como un loco.\n {1} Bruscamente tira todo su arsenal al suelo, el cual "
                        "consiste de: {3}\n.{0} nervioso frena en seco al ver como todas las armas cobran vida y "
                        "arremeten contra el, y sin piedad lo hacen trisas.\n{1} Mira complacido todo el "
                        "espectaculo".format(
                            self.activo.nombre, self.pasivo.nombre, arma_pasivo.nombre,
                            " y ".join([a.nombre for a in armas_pasivo])
                        ) +
                        " \"{0}\"-Dice {1} Mientras mira los no existentes restos de su oponente.\n".format(
                            self.pasivo.frase_counter, self.pasivo.nombre)
                    )
                    # Registrar asesinato
                    self.pasivo.agregar_asesinato(self.activo)
                    return _str, self.activo

                # Escapa Activo(5%)
                else:
                    _str += (
                        "{0} Se rinde al notar todas la armas de {1}.\n{0} Decide arrojar su {1} a modo de "
                        "distraccion y logra escapar.".format(
                            self.activo.nombre, arma_activo.nombre
                        )
                    )
                    # Actualizar Inventario
                    self.activo.inventario.quitar_objeto(arma_activo)
                    self.activo.actualizar_arma()
                    return _str, None

            # Caso c.3: Ambos poseen el mismo numero de armas
            else:
                _str += (
                    "Pero {0} amenasante saca su {1}.{2} responde sacando su {3}. Ambos contricantes sostienen un "
                    "combate epico por 2 horas que termina en empate.".format(
                        self.pasivo.nombre, arma_pasivo.nombre, self.activo.nombre, arma_activo.nombre
                    )
                )
                i = Interaccion("", "Tuvo ese duelo lleno de GLORIA", self.pasivo, self.activo)
                self.activo.agregar_intereaccion(i)
                self.pasivo.agregar_intereaccion(i)
                return _str, None

        # Caso d: Activo y Pasivo estan desarmados
        else:
            r = random.randrange(0, 100)
            # Muere pasivo(50%)
            if r <= 50:
                _str += (
                    "{0} logra matarlo.\n".format(self.activo.nombre) +
                    "\"{0}\"-Dice {1} mientras se retira".format(
                        self.activo.frase_asesinato, self.activo.nombre)
                )
                # Registrar asesinato
                self.activo.agregar_asesinato(self.pasivo)
                return _str, self.pasivo

            # Escapa pasivo(30%)
            elif 50 < r <= 80:
                _str += ("Pero a {0} se le escapa el objetivo.".format(self.activo.nombre))
                return _str, None

            # Muere Activo(20%)
            else:
                _str += (
                    "Pero a {0} no le importa, y termina matando a {1}.".format(
                        self.pasivo.nombre, self.activo.nombre
                    ) +
                    "\"{0}\"-Dice {1} mientras mira con indiferencia al cadaver.".format(
                        self.pasivo.frase_counter, self.pasivo.nombre
                    )
                )
                # Registrar asesinato
                self.pasivo.agregar_asesinato(self.activo)
                return _str, self.activo
