# -*- coding: UTF-8 -*-
"""
Created on 05/03/2015

@author: Luis Mario
"""
import random

import bot

from mambregaem.constantes import Accion, acciones, acciones_activo_pasivo, acciones_solo
from mambregaem.constantes import acciones_grupales, acciones_grupo_pasivo, tributos
from mambregaem.entidades import Trampa, Arma, Tributo
from mambregaem.acciones import Combate, Interaccion

tributos_log = []

evento = ['Madrugada', 'Mañana', 'Mediodia', 'Tarde', 'Noche', 'Media noche']


def final_destination():
    for _tributo in tributos:
        _tributo.inventario.capacidad = 100


@bot.comando('.tributos')
def listar_tributos(bot, mensaje):
    bot.irc_sock.enviar_msj("Tributos actuales:")
    for tributo in tributos:
        bot.irc_sock.enviar_msj(tributo.nombre)


@bot.comando('.tributo')
def agregar_tributo(bot, mensaje):
    mensaje = mensaje.strip('.tributo')
    tokens = mensaje.split(' ')
    tributos.append(Tributo(tokens[0], frase_asesinato=tokens[1], frase_counter=[2]))


@bot.comando('.mambregaems')
def activar_mambre(bot, mensaje):
    if len(tributos) < 2:
        bot.irc_sock.enviar_msj("No hay suficientes TRIBUTOS, agrega mas tributos con el comando .tributo")
    bot.irc_sock.enviar_msj("QUE LOS GAEMS COMIENZEN")
    bot.mambre_activo = True


@bot.comando('.siguiente', '.next')
def procesar_evento(bot, mensaje):
    if not bot.mambre_activo:
        bot.irc_sock.enviar_msj("Es necesario activar una sesion de juego primero (.mambegaem)")
        return

    if len(tributos) > 1:
        _str = ("MAMBRE GAEMSS, DIA {0} - {1}".format(str(dia), evento[bot.n_eventos]))
        if bot.dia == 25:
            bot.irc_sock.enviar_msj(
                "De pronto, los cielos se pusieron obscuros. pero en el centro, se podia ver la enorme silueta de "
                "una rara entidad...")
            bot.irc_sock.enviar_msj(
                "Era Gromm, quien dijo: Que los juegos realmente comienzeeeeeen! Yo decreto: NO mas piedad! "
                "No mas limites!")
            bot.irc_sock.enviar_msj(
                "Ahora nadie se detiene ante nada en una pelea, ahora todos pueden tomar cuantas armas deseen!!")
            bot.irc_sock.enviar_msj("LEEETSS RUUUMMMMMMBLEEEEEEE!!")

            bot.interacciones_activas = False
            final_destination()

        r = random.randrange(0, 100)
        if r <= 30:
            tipo_accion = acciones.UNOaUNO
        elif 30 < r <= 60:
            tipo_accion = acciones.SOLO
        elif 60 < r <= 85:
            tipo_accion = acciones.GRUPAL
        else:
            tipo_accion = acciones.GRUPOaUNO

        if tipo_accion == acciones.UNOaUNO:
            participantes = random.sample(tributos, 2)
            tributo_activo = participantes[0]
            tributo_pasivo = participantes[1]

            texto, accion, arg = random.choice(acciones_activo_pasivo)

            # Combates
            if accion == Accion.COMBATE or accion == Accion.TRAMPA:
                combate = Combate(tributo_activo, tributo_pasivo, texto)
                texto, resultado = combate.ejecutar_combate(bot.interacciones_activas)
                bot.irc_sock.enviar_msj(texto)
                if resultado is not None:
                    tributos.remove(resultado)
                    tributos_log.append(resultado)

            # Trampas
            # elif accion == Accion.TRAMPA:
            #    trampa = Trampa(tributo_activo, tributo_pasivo, texto, "", "")
            #    resultado = trampa.ejecutar_accion(tributo_activo, tributo_pasivo)
            #    if resultado is not None:
            #        tributos.remove(resultado)
            #        tributos_log.append(resultado)

            # Interacciones
            else:
                interaccion = Interaccion(texto, arg, tributo_activo, tributo_pasivo)
                texto = interaccion.ejecutar_interaccion()
                bot.irc_sock.enviar_msj(texto)

        elif tipo_accion == acciones.SOLO:
            tributo = random.choice(tributos)
            texto, accion, arg = random.choice(acciones_solo)

            bot.irc_sock.enviar_msj(tributo.nombre + texto + ". ")
            if accion == Accion.Suicidio:
                tributos.remove(tributo)
                tributos_log.append(tributo)

            if accion == Accion.ARMA:
                r = tributo.inventario.agregar_objeto(arg)
                if not r:
                    bot.irc_sock.enviar_msj(
                        "Desafortunadamente, no tenia el espacio suficiente y tira el objeto.")
                tributo.set_arma_actual(arg)

        elif tipo_accion == acciones.GRUPAL:
            n = random.randrange(2, 4)
            if n > len(tributos):
                n = len(tributos)
            grupo = random.sample(tributos, n)
            texto, accion, arg = random.choice(acciones_grupales)

            for tributo in grupo:
                bot.irc_sock.enviar_msj(tributo.nombre + ", ")
            bot.irc_sock.enviar_msj(texto)

            if accion == Accion.SuicidoEnMasa:
                for tributo in grupo:
                    tributos.remove(tributo)
                    tributos_log.append(tributo)

            # Interaccion grupal
            if accion == Accion.Fiesta:
                i = Interaccion(texto, arg, *grupo)
                for tributo in grupo:
                    tributo.agregar_intereaccion(i)

        # Eventos tipo Grupo a Uno
        else:
            if len(tributos) < 3:
                return

            n = random.randrange(3, 5)
            if n > len(tributos):
                n = len(tributos)
            grupo = random.sample(tributos, n)
            victima = grupo.pop()
            texto, accion = random.choice(acciones_grupo_pasivo)

            for tributo in grupo:
                bot.irc_sock.enviar_msj(tributo.nombre + ", ")
            bot.irc_sock.enviar_msj(texto + victima.nombre + ". ")

            if accion == Accion.Raid:
                interaccion = None
                aliado = None
                for atacante in grupo:
                    interaccion = atacante.buscar_interaccion(victima)
                    if interaccion is not None:
                        aliado = atacante
                        break

                if (interaccion is not None) and bot.interacciones_activas:
                    bot.irc_sock.enviar_msj(
                        "Sin embargo, {0} recuerda cuando {1} con {2}. Así que convence al grupo de cancelar la "
                        "operacion.\n".format(aliado.nombre, interaccion.identificador, victima.nombre)
                    )
                    aliado.quitar_interaccion(interaccion)
                    return

                # Evento cuando victima esta fuertemente armada
                n_armas = 0
                for objeto in victima.inventario.objetos:
                    if type(objeto) is Arma:
                        n_armas += 1

                if n_armas > 1:
                    bot.irc_sock.enviar_msj(
                        "Sin embargo {0} solo mira encantado a sus atacantes antes de comenzar a "
                        "arrojar bruscamente todo su arsenal.\n"
                        "Las armas arremeten contra todos los atacantes, haciendolos trisas. "
                        "{0} Mira complacido todo el espectaculo".format(victima.nombre)
                    )
                    victima.agregar_asesinatos(grupo)
                    for tributo in grupo:
                        tributos.remove(tributo)
                        tributos_log.append(tributo)
                    return

                # Evento regular
                r = random.randrange(0, 100)
                if r <= 50:
                    bot.irc_sock.enviar_msj("Logran acabar con el.")
                    tributos.remove(victima)
                    tributos_log.append(victima)
                    for tributo in grupo:
                        tributo.agregar_asesinato(victima)

                elif 50 < r <= 75:
                    bot.irc_sock.enviar_msj(
                        "Pero se les escapa su victima al no organizar bien su ataque.")

                else:
                    if victima.arma is not None:
                        bot.irc_sock.enviar_msj(
                            "Sin embargo, {0}, haciendo uso de su {1} y astucia, decide contraatacar. Acabando "
                            "con todos sus atacantes.".format(victima.nombre, victima.arma.nombre)
                        )
                        victima.arma.ejecutar(multiple=True)
                        if victima.frase_counter is not None:
                            bot.irc_sock.enviar_msj(
                                "\t\"{0} \"-Dice {1} mientras rie como un loco en medio de la "
                                "masacre.".format(victima.frase_counter, victima.nombre)
                            )
                    else:
                        bot.irc_sock.enviar_msj(
                            "Pero {0} Estaba de mal humor ese dia, asi que asesino a todo el grupo por atreverse a "
                            "molestarlo.".format(victima.nombre)
                        )
                        if victima.frase_counter is not None:
                            bot.irc_sock.enviar_msj(
                                "\t\"{0} \"-Dice {1}  mientras mira furioso a sus inhertes "
                                "atacantes.".format(victima.frase_counter, victima.nombre)
                            )

                    victima.agregar_asesinatos(grupo)
                    for tributo in grupo:
                        tributos.remove(tributo)
                        tributos_log.append(tributo)

            if accion == Accion.BROMA:
                r = random.randrange(0, 4)
                if r == 0:
                    bot.irc_sock.enviar_msj("Todo por sus buenos pantalones.")
                elif r == 1:
                    bot.irc_sock.enviar_msj("Pues creen que el es el dios Gromm.")
                elif r == 2:
                    bot.irc_sock.enviar_msj(
                        "Pues tiene una araña en la cara y quieren decirle.")
                else:
                    bot.irc_sock.enviar_msj("Todo por su sedoso cabello.")

        bot.n_eventos += 1
        if bot.n_eventos == 5:
            bot.dia += 1
            bot.n_eventos = 0

    if len(tributos) == 0:
        bot.irc_sock.enviar_msj("TODOS MURIERROOON!")
        bot.mambre_activo = False

    else:
        bot.irc_sock.enviar_msj("EL GANADOR ES: " + tributos[0].nombre)
        tributos_log.append(tributos[0])
        bot.mambre_activo = False

    if not bot.mambre_activo:
        bot.irc_sock.enviar_msj("Resultados:")
        for tributo in tributos_log:
            bot.irc_sock.enviar_msj(
                tributo.nombre + "-> Aesesinatos: " + str(len(tributo.asesinatos)) + " . Victimas: ")

            if len(tributo.asesinatos) == 0:
                bot.irc_sock.enviar_msj("Ninguna.")

            else:
                bot.irc_sock.enviar_msj(tributo.asesinatos)
