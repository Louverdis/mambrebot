__author__ = 'Luis Mario'


def comando(*comandos):
    """
    Funcion decoradora.
    Asigna un atributo llamado -comandos- con los valores de la lista de argumentos

    :param comandos: lista de str
    :return: callable object
    """
    def asignar_comandos(funcion):
        if not hasattr(funcion, 'comandos'):
            funcion.comandos = []
        funcion.comandos.extend(comandos)
        return funcion

    return asignar_comandos


class MensajeIRC:
    def __init__(self, irc_input):
        self.raw = irc_input

        self.sender = None
        self.host = None
        self.comando = None
        self.mensaje = None

        # Usuario envia mensaje:
        # :Bonifacio!~luismario@26280F2.B9600A42.6C8DACE8.IP PRIVMSG #mambre :test

        # Usuario entra al canal:
        # :Bonifacio!~luismario@26280F2.B9600A42.6C8DACE8.IP JOIN :#mambre
        # :ChanServ!service@rizon.net MODE #mambre +o Bonifacio

        # Usuario sale de canal:
        # :Bonifacio!~luismario@26280F2.B9600A42.6C8DACE8.IP PART #mambre

    def _procesar_input(self):
        if self.raw.startswith(':'):
            # existe un sender
            sender, tail = self.raw.split('!', maxsplit=1)
            self.sender = sender.strip(':')

            # se obtiene mensaje
            cuerpo, self.mensaje = tail.split(':', maxsplit=1)

            # se obtiene comando y host
            self.host, self.comando = cuerpo.split(' ', maxsplit=1)

        else:
            return


class Bot:
    def __init__(self, irc_sock):
        super(Bot, self).__init__()
        self.irc_sock = irc_sock
        self.comandos = {}

        # Atributos para mambregaems
        self.mambre_activo = False
        self.interacciones_activas = True
        self.n_eventos = 0
        self.dia = 1

    def agregar_comando(self, cmd, funcion):
        self.comandos[cmd] = funcion

    def agregar_modulo(self, modulo):
        pass

    def isCommand(self, cmd):
        if cmd in self.comandos:
            return True
        else:
            return False

    def ejecutar_comando(self, cmd, irc_input):
        self.comandos[cmd](self, irc_input)






