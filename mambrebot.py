__author__ = 'Luis Mario'

import bot
from mambregaem import gaem

from socket import socket, AF_INET, SOCK_STREAM

# From RFC2812 Internet Relay Chat: Client Protocol
#  Section 2.3
#
# https://tools.ietf.org/html/rfc2812.html
#
# IRC messages are always lines of characters terminated with a
# CR-LF (Carriage Return - Line Feed) pair, and these messages SHALL
# NOT exceed 512 characters in length, counting all characters
# including the trailing CR-LF. Thus, there are 510 characters
# maximum allowed for the command and its parameters.  There is no
# provision for continuation of message lines.

SERVER = "irc.rizon.net"
CHANNEL = "#mambre"
NICK = "mambrebot"


class IRCSock:
    def __init__(self):
        self.client_sock = socket(AF_INET, SOCK_STREAM)
        self.bot = bot.Bot(self)

        self.bot.agregar_modulo(gaem)

        # for cmd in gaem.listar_tributos.comandos:
        #     self.bot.agregar_comando(cmd, gaem.listar_tributos)

        # for cmd in gaem.agregar_tributo.comandos:
        #     self.bot.agregar_comando(cmd, gaem.agregar_tributo)

        # for cmd in gaem.activar_mambre.comandos:
        #     self.bot.agregar_comando(cmd, gaem.activar_mambre)

        # for cmd in gaem.procesar_evento.comandos:
        #     self.bot.agregar_comando(cmd, gaem.procesar_evento)

    def conectar(self):
        self.client_sock.connect((SERVER, 6667))
        self.client_sock.send("USER {0} {0} {0} :MAMBRE BOT\r\n".format(NICK).encode('utf-8'))
        self.client_sock.send("NICK {0}\r\n".format(NICK).encode('utf-8'))

    def _join_channel(self):
        self.client_sock.send("JOIN {0} mambregaems\r\n".format(CHANNEL).encode('utf-8'))

    def ping(self):
        self.client_sock.send("PONG :Pong\r\n".encode('utf-8'))

    def enviar_msj(self, msj):
        self.client_sock.send("PRIVMSG {0} :{1}\r\n".format(CHANNEL, msj).encode('utf-8'))

    def hello(self):
        self.client_sock.send("PRIVMSG {0} :Hola!!\r\n".format(CHANNEL).encode('utf-8'))

    def irc_handler(self):
        self._join_channel()
        while True:
            irc_msj = self.client_sock.recv(2048)
            if irc_msj is None:
                continue
            irc_msj = irc_msj.decode('utf-8').strip('\r\n')
            print(irc_msj)

            mensaje = bot.MensajeIRC(irc_msj)

            if mensaje.mensaje.find(".Hola {0}".format(NICK)) != -1:
                self.enviar_msj("Hola {0}, gracias por saludar".format(mensaje.sender))

            if mensaje.mensaje.find("compy") != -1:
                self.enviar_msj("COMMMMPYYYYY")

            if mensaje.mensaje.find("ugh") != -1:
                self.enviar_msj("ughUGH**__--_{0}_--__**HGUhgu".format(mensaje.sender))

            if irc_msj.find("JOIN :") != -1:
                self.enviar_msj("Bienvenido {0}".format(mensaje.sender))

            if irc_msj.find("PING :") != -1:
                self.ping()

            msj_header = mensaje.mensaje.split(' ')[0]
            print(msj_header)
            if self.bot.es_comando(msj_header):
                print('Se detecto un posible comando')
                if self.bot.es_comando_valido(msj_header):
                    print('Se detecto un comando')
                    self.bot.ejecutar_comando(msj_header, mensaje.mensaje)


if __name__ == '__main__':
    irc = IRCSock()
    irc.conectar()
    irc.irc_handler()
