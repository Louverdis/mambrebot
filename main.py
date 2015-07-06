__author__ = 'Luis Mario'


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

            if irc_msj.find(".Hola {0}".format(NICK)) != -1:
                self.hello()

            if irc_msj.find("PING :") != -1:
                self.ping()


if __name__ == '__main__':
    irc = IRCSock()
    irc.conectar()
    irc.irc_handler()
