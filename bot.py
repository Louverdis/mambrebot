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
    def __init__(self, raw_input):
        self.raw = raw_input

