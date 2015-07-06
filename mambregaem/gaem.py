# -*- coding: UTF-8 -*-
"""
Created on 05/03/2015

@author: Luis Mario
"""
import random

from mambregaem.constantes import Accion, acciones, acciones_activo_pasivo, acciones_solo
from mambregaem.constantes import acciones_grupales, acciones_grupo_pasivo, tributos
from mambregaem.entidades import Trampa, Arma
from mambregaem.acciones import Combate, Interaccion

tributos_log = []


def final_destination():
    for _tributo in tributos:
        _tributo.inventario.capacidad = 100


if __name__ == '__main__':
    INTERACCIONES_ACTIVAS = True
    dia = 1
    while len(tributos) > 1:
        print("\nMAMBRE GAEMSS, DIA: " + str(dia))
        if dia == 25:
            print(
                "De pronto, los cielos se pusieron obscuros. pero en el centro, se podia ver la enorme silueta de "
                "una rara entidad...\n"
                "Era Gromm, quien dijo: Que los juegos realmente comienzeeeeeen! Yo decreto: NO mas piedad! "
                "No mas limites!\n"
                "Ahora nadie se detiene ante nada en una pelea, ahora todos pueden tomar cuantas armas deseen!!\n"
                "LEEETSS RUUUMMMMMMBLEEEEEEE!!\n\n"
            )
            INTERACCIONES_ACTIVAS = False
            final_destination()

        for i in range(5):
            input("...")
            r = random.randrange(0, 100)
            if r <= 30:
                tipo_accion = acciones.UNOaUNO
            elif 30 < r <= 60:
                tipo_accion = acciones.SOLO
            elif 60 < r <= 85:
                tipo_accion = acciones.GRUPAL
            else:
                tipo_accion = acciones.GRUPOaUNO
            # tipo_accion = random.randrange(0,4)

            if tipo_accion == acciones.UNOaUNO:
                participantes = random.sample(tributos, 2)
                tributo_activo = participantes[0]
                tributo_pasivo = participantes[1]

                texto, accion, arg = random.choice(acciones_activo_pasivo)

                # Combates
                if accion == Accion.COMBATE:
                    combate = Combate(tributo_activo, tributo_pasivo, texto)
                    texto, resultado = combate.ejecutar_combate(INTERACCIONES_ACTIVAS)
                    print(texto)
                    if resultado is not None:
                        tributos.remove(resultado)
                        tributos_log.append(resultado)

                # Trampas
                elif accion == Accion.TRAMPA:
                    trampa = Trampa(tributo_activo, tributo_pasivo, texto, "", "")
                    resultado = trampa.ejecutar_accion(tributo_activo, tributo_pasivo)
                    if resultado is not None:
                        tributos.remove(resultado)
                        tributos_log.append(resultado)

                # Interacciones
                else:
                    interaccion = Interaccion(texto, arg, tributo_activo, tributo_pasivo)
                    texto = interaccion.ejecutar_interaccion()
                    print(texto)

            elif tipo_accion == acciones.SOLO:
                tributo = random.choice(tributos)
                texto, accion, arg = random.choice(acciones_solo)

                print(tributo.nombre + texto, end=". ")
                if accion == Accion.Suicidio:
                    print()
                    tributos.remove(tributo)
                    tributos_log.append(tributo)

                if accion == Accion.ARMA:
                    r = tributo.inventario.agregar_objeto(arg)
                    if not r:
                        print("Desafortunadamente, no tenia el espacio suficiente y tira el objeto.")
                    tributo.set_arma_actual(arg)

            elif tipo_accion == acciones.GRUPAL:
                n = random.randrange(2, 4)
                if n > len(tributos):
                    n = len(tributos)
                grupo = random.sample(tributos, n)
                texto, accion, arg = random.choice(acciones_grupales)

                for tributo in grupo:
                    print(tributo.nombre, end=", ")
                print(texto)

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
                    continue

                n = random.randrange(3, 5)
                if n > len(tributos):
                    n = len(tributos)
                grupo = random.sample(tributos, n)
                victima = grupo.pop()
                texto, accion = random.choice(acciones_grupo_pasivo)

                for tributo in grupo:
                    print(tributo.nombre, end=", ")
                print(texto + victima.nombre, end=". ")

                if accion == Accion.Raid:
                    interaccion = None
                    aliado = None
                    for atacante in grupo:
                        interaccion = atacante.buscar_interaccion(victima)
                        if interaccion is not None:
                            aliado = atacante
                            break

                    if (interaccion is not None) and INTERACCIONES_ACTIVAS:
                        print(
                            "Sin embargo, {0} recuerda cuando {1} con {2}. Así que convence al grupo de cancelar la "
                            "operacion.\n".format(aliado.nombre, interaccion.identificador, victima.nombre)
                        )
                        aliado.quitar_interaccion(interaccion)
                        continue

                    # Evento cuando victima esta fuertemente armada
                    n_armas = 0
                    for objeto in victima.inventario.objetos:
                        if type(objeto) is Arma:
                            n_armas += 1

                    if n_armas > 1:
                        print(
                            "Sin embargo {0} solo mira encantado a sus atacantes antes de comenzar a "
                            "arrojar bruscamente todo su arsenal.\n"
                            "Las armas arremeten contra todos los atacantes, haciendolos trisas. "
                            "{0} Mira complacido todo el espectaculo".format(victima.nombre)
                        )
                        victima.agregar_asesinatos(grupo)
                        for tributo in grupo:
                            tributos.remove(tributo)
                            tributos_log.append(tributo)
                        continue

                        # Evento regular
                    r = random.randrange(0, 100)
                    if r <= 50:
                        print("Logran acabar con el.")
                        tributos.remove(victima)
                        tributos_log.append(victima)
                        for tributo in grupo:
                            tributo.agregar_asesinato(victima)

                    elif 50 < r <= 75:
                        print("Pero se les escapa su victima al no organizar bien su ataque.")

                    else:
                        if victima.arma is not None:
                            print(
                                "Sin embargo, {0}, haciendo uso de su {1} y astucia, decide contraatacar. Acabando "
                                "con todos sus atacantes.".format(victima.nombre, victima.arma.nombre)
                            )
                            victima.arma.ejecutar(multiple=True)
                            if victima.frase_counter is not None:
                                print(
                                    "\t\"{0} \"-Dice {1} mientras rie como un loco en medio de la "
                                    "masacre.".format(victima.frase_counter, victima.nombre)
                                )
                            else:
                                print()
                        else:
                            print(
                                "Pero {0} Estaba de mal humor ese dia, asi que asesino a todo el grupo por atreverse a "
                                "molestarlo.".format(victima.nombre)
                            )
                            if victima.frase_counter is not None:
                                print(
                                    "\t\"{0} \"-Dice {1}  mientras mira furioso a sus inhertes "
                                    "atacantes.".format(victima.frase_counter, victima.nombre)
                                )
                            else:
                                print()
                        victima.agregar_asesinatos(grupo)
                        for tributo in grupo:
                            tributos.remove(tributo)
                            tributos_log.append(tributo)

                if accion == Accion.BROMA:
                    r = random.randrange(0, 4)
                    if r == 0:
                        print("Todo por sus buenos pantalones.")
                    elif r == 1:
                        print("Pues creen que el es el dios Gromm.")
                    elif r == 2:
                        print("Pues tiene una araña en la cara y quieren decirle.")
                    else:
                        print("Todo por su sedoso cabello.")

                else:
                    print()

            if len(tributos) <= 1:
                break
        dia += 1
        input("Proceder...")

    if len(tributos) == 0:
        print("\nTODOS MURIERROOON!")
    else:
        print("\nEL GANADOR ES: " + tributos[0].nombre)
        tributos_log.append(tributos[0])

    input("Mostrar resultados...")
    print("\n\nResultados:")
    for tributo in tributos_log:
        print(tributo.nombre + "-> Aesesinatos: " + str(len(tributo.asesinatos)), end=" . Victimas: ")
        if len(tributo.asesinatos) == 0:
            print("Ninguna.")
        else:
            print(tributo.asesinatos)
