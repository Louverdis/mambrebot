"""
Created on 07/03/2015

@author: Luis Mario
"""

from mambregaem.entidades import Tributo, Arma, Trampa


def enum(*secuenciales, **kwarg):
    """Funcion que retorna Enumeraciones, funcionan de manera similar a
    los Enums de C.
    -Nota: En python 3.4, los Enums ya vienen implementados en la libreria
        estandar, pero en el PI solo se puede usar hasta python 3.2.
    """
    enums = dict(zip(secuenciales, range(len(secuenciales))), **kwarg)
    return type('Enum', (), enums)

    
Accion = enum(
    'COMBATE', 'INTERACCION', 'TRAMPA', 'TrampaMapa', 'Fiesta', 'FIESTA', 'Descanso',
    'Suicidio', 'Reflexion', 'SuicidoEnMasa', 'Raid', 'ARMA', 'BROMA'
)

acciones = enum('UNOaUNO', 'SOLO', 'GRUPAL', 'GRUPOaUNO')

armas = {
    'escopeta': Arma('escopeta', 'La escopeta destroza facilmente la cara de {1}.', 'Tiros en rapida sucesion perforan a cada uno de los atacantes sin dificultad.'), 
    'ventana': Arma('ventana', '{1} tras ser tirado por la ventana entra en otra dimension en donde cae a un abismo sin fondo por toda la eternidad.', "Desde la ventana aun se pueden escuchar los gritos de las victimas al caer a un abismo sin fondo."),
    'catapulta': Arma('catapulta', 'Tras un tiro friamente calculado por {0}, la catapulta aplasta a {1}.', 'La catapulta entra en modo multi-kill, tirando rafagas de tiros, aplastando a todos los atacantes.'),
    'piedra afilada': Arma('piedra afilada', 'Con la piedra, {0} perfora multiples veces en el pecho a {1} hasta matarlo.', 'La piedra adquiere propiedades de boomerang y atraviesa multiples cuerpos a la vez, acabando con todos.' ),
    'bomba': Arma('bomba', 'La bomba se activa, y vuela en pedazos a {1}, pero convenientemente no daña a {0}', 'La bomba se activa y destruye a todos los atacantes, afortunadamente los restos de los cuerpos bloquearon los escombros, y nadie mas salio herido.', consumible=True),
    'dardos envenenados': Arma('dardos envenenados', 'Multiples dardos aciertan en {1}, produciendo una muerte lenta y agonica', 'Multiples objetivos aciertan en los dardos, produciendo multiples muertes lentas y agonicas.', consumible=True),
    'lanza': Arma('lanza', 'La lanza atraviesa el corazon de {1},...{1} esta muerto.', 'Con la lanza se perforaron todos los corazones del grupo atacante, la lanza esta muy feliz.'),
    'pokebola': Arma('pokebola', 'POKEBOLA VE!!\nPikachu yo te elijo!!\n\tPikachu, usa IMPACTRUEENNOO\n\tPikachu:PiikaaaaCHUUUUUUUUUUU\nPickachu mato a {1}.','POKEBOLA VE!!\nPikachu yo te elijo!!\n\tPikachu, usa IMPACTRUEENNOO\n\tPikachu:PiikaaaaCHUUUUUUUUUUU\nPickachu mato a sus rivales.'),
    'amuleto': Arma('amuleto', 'El amuleto dispara un rayo de luz que fulmina al instante a {1}', 'El amuleto dispara multiples rayos de luz fulminadora, calcinando todo lo que se mueve.'),
    'robot': Arma('robot', 'El robot saca motocierras de sus manos y hace una carcineria con {1}, acto seguido el robot se pone a bailar junto a {0}', 'El robot se enoja y se autodestruye, matando todo ser vivo a la redonda(gromm protegio al usuario), luego se reconstruye, porque robot recordo que aun tenia cosas por hacer como para morir ahi.')
}

trampas = {
    'mina': Trampa('mina', 'texto', 'ejecucion', 'desarme', 'suicido'),
    'agua envenenada': Trampa('agua envenenada', 'texto', 'ejecucion', 'desarme', 'suicido'),
    'comida envenenda': Trampa('comida envenenda', 'texto', 'ejecucion', 'desarme', 'suicido'),
    'acido': Trampa('acido', 'texto', 'ejecucion', 'desarme', 'suicido')
}

acciones_activo_pasivo = [
    ("{0} Intenta atacar a {1}", Accion.COMBATE, ""),
    ("{0} Iracundo, corre a matar a {1}", Accion.COMBATE, ""),
    ("{0} En un ataque de locura golpea insesante a {1}", Accion.COMBATE, ""),
    ("{0} Reta formalmente a un duelo a {1}", Accion.COMBATE, ""),
    ("{0} Intenta emboscar a {1}", Accion.COMBATE, ""),
    ("{0} Saluda a {1}", Accion.INTERACCION, "Compartio un saludo"),
    ("{0} Pasa un momento amistoso con {1}", Accion.INTERACCION, "Paso un momento amistoso"),
    ("{0} Mira con rencor a {1}", Accion.INTERACCION, "Compartio miradas con rencor"),
    #(" Coloca una mina en el campamento de ", Accion.TRAMPA, ""),
    #(" Envenena el agua de ", Accion.TRAMPA, ""),
    #(" Envenena la comida de ", Accion.TRAMPA, ""),
    #(" Cambia las medicinas por acido de ", Accion.TRAMPA, "")
]

acciones_solo = [
    (" Decide explorar", Accion.Reflexion, ""),
    (" Decide recuperar fuerzas descansando", Accion.Descanso, ""),
    #(" Intenta construir una catapulta, pero una rama le cae ensima y lo mata", Accion.Suicidio, ""),
    (" Intenta construir una catapulta, y lo consigue", Accion.ARMA, armas["catapulta"]),
    #(" Se tropieza y cae por un acantilado de piedras filosas, no logra sobrevivir la caida.", Accion.Suicidio, ""),
    (" Se tropieza y cae por un acantilado de piedras filosas, sin embargo logra sobrevivir y se lleba una piedra de recuerdo.", Accion.ARMA, armas["piedra afilada"]),
    #(" Intenta armar una bomba, pero le explota en la cara y muere", Accion.Suicidio, ""),
    (" Le aparece el dios VeneREAL y lo manda el reino de las sombras", Accion.Suicidio, ""),
    (" Intenta armar una bomba, y despues de 20 minutos obtiene una bomba activa", Accion.ARMA, armas["bomba"]),
    (" Encuentra una casa abandonada y decide arrancar una ventana.", Accion.ARMA, armas["ventana"]),
    (" Encuentra una casa abandonada y decide arrancar una ventana.", Accion.ARMA, armas["ventana"]),
    (" Encuentra una casa abandonada y decide arrancar una ventana, PERO se corta con los vidrios y muere lentamente.", Accion.Suicidio, ""),
    #(" Intenta crear veneno, pero se entoxica a si mismo y muere", Accion.Suicidio, ""),
    (" Intenta crear veneno, y despues de rato, envenena y guarda un par de dardos", Accion.ARMA, armas["dardos envenenados"]),
    (" Mientras afila una rama, esta se le resbala y se apunala a si mismo, muriendo", Accion.Suicidio, ""),
    (" Afila una rama, consiguiendo armar una lanza de madera", Accion.ARMA, armas["lanza"]),
    (" Contempla como seria la vida si ganara los juegos", Accion.Reflexion, ""),
    (" Sufre un ataque de panico y grita por ayuda", Accion.Reflexion, ""),
    (" Le importa un carajo los juegos, decide ponerse a pescar", Accion.Reflexion, ""),
    (" Extrana su casa", Accion.Reflexion, ""),
    (" Se resbala caminando cerca del rio y llora por una hora", Accion.Reflexion, ""),
    (" Esta tan feliz que se pone a bailar en la cima de una roca", Accion.Reflexion, ""),
    (" Encuentra una escopeta tirada por ahi.", Accion.ARMA, armas["escopeta"]),
    (" Encuentra una escopeta tirada por ahi.", Accion.ARMA, armas["escopeta"]),
    (" Sufre violentas alucinaciones.", Accion.Reflexion, ""),
    (" Es visitado por el dios Gromm.", Accion.Reflexion, ""),
    (" Se desmaya.", Accion.Reflexion, ""),
    (" Se encuentra una pokebola entre unas rocas.", Accion.ARMA, armas["pokebola"]),
    (" Se encuentra una pokebola entre las ramas de un arbol.", Accion.ARMA, armas["pokebola"]),
    (" Se encuentra una pokebola en sus pantalones.", Accion.ARMA, armas["pokebola"]),
    (" Se encuentra una pokebola en sus pantalones.", Accion.ARMA, armas["pokebola"]),
    (" Se encuentra una pokebola en sus pantalones.", Accion.ARMA, armas["pokebola"]),
    (" Cae por un hoyo profundo, Sin embargo, logra sobrevivir, ademas encuentra un raro amuleto en aquel hoyo.", Accion.ARMA, armas["amuleto"]),
    (" Cae por un hoyo profundo, Sin embargo, logra sobrevivir, ademas encuentra un raro amuleto en aquel hoyo.", Accion.ARMA, armas["amuleto"]),
    (" Le aparece el dios Gromm, diciendole -Grab this shit yo- *amuleto get*.", Accion.ARMA, armas["amuleto"]),
    (" Recuerda su epoca como ingeniero y decide construir un robot.", Accion.ARMA, armas["robot"]),
    (" Recuerda su epoca como ingeniero y decide construir un robot.", Accion.ARMA, armas["robot"]),
    (" Ve al dios veneREAL tropesarse, tirando un raro robot, cuando el dios se va, consigue quedarse con el robot.", Accion.ARMA, armas["robot"]),
    
]

acciones_grupales = [
    (" Deciden acampar juntos", Accion.FIESTA, "acampo"),
    (" Se cuentan historias sobre sus anios de gloria", Accion.FIESTA, "conto sus gloriosas historias"),
    (" Se encuentran un esqueleto y corren horrorizados", Accion.FIESTA, "huyo de un equeleto horrorisado"),
    (" Les aparece el dios VeneREAL, persiguiendolos mientras grita -GET REAL-", Accion.FIESTA, "obtivieron el REAL del dios cruel"),
    (" Deciden jugar a patear la lata", Accion.FIESTA, "jugo al divertido juego de patear la lata"),
    #(" Intentan armar una fogata, pero lo hacen mal, creando un incendio y mueren", Accion.SuicidoEnMasa),
    #(" Hacen un caldo con hierbas silvestres. Desgraciadamente, la mayoria de las hierbas eran venenosas y mueren entoxicados.", Accion.SuicidoEnMasa),
    (" Hacen un caldo con hierbas silvestres.", Accion.FIESTA, "comio ese delicioso caldo"),
    (" Corren en circulos en un campo de maiz cantando canciones de sus pueblos", Accion.FIESTA, "compartio ese magico momento con las canciones por los campos"),
    (" Deciden hacer una terapia grupal", Accion.FIESTA, "confeso sus miedos en la terapia"),
    (" Se gritan entre si", Accion.FIESTA, "grito ferosmente")
]

acciones_grupo_pasivo = [
    (" Encuentran el paradero de ", Accion.INTERACCION),
    (" Deciden emboscar a ", Accion.Raid),
    (" Deciden hacer un ataque frontal a ", Accion.Raid),
    (" Persiguen a ", Accion.BROMA)
]

tributos = [
    #Tributo("Luis Mario"),
    #Tributo("Andre"),
    #Tributo("Jeff"),
    #Tributo("Lorenzo", frase_asesinato="OYE ZHY", frase_counter="OYE KE TE PASA"),
    #Tributo("Carlos", frase_asesinato="...", frase_counter="..."),
    #Tributo("Rolando"),
    #Tributo("Roberto"),
    #Tributo("Heriberto"),
    #Tributo("Dr Reicho", frase_asesinato="HAY SENIOR", frase_counter="HAY CARAMBA"),
    #Tributo("EspantaMuertos", frase_asesinato="HAY SENIOR", frase_counter="HAY CARAMBA"),
    #Tributo("Celtic", frase_asesinato="HAY SENIOR", frase_counter="HAY CARAMBA"),
    #Tributo("ZHAKAZULU el blanco", frase_asesinato="Soy blanco", frase_counter="No eras blanco"),
    #Tributo("WARSPAKTRUM", frase_asesinato="HAY SENIOR", frase_counter="HAY CARAMBA"),
    #Tributo("Jaraxxus", frase_asesinato="HAY SENIOR", frase_counter="HAY CARAMBA"),
    #Tributo("Bonifacio", frase_asesinato="HAY SENIOR", frase_counter="Orale cuate"),
    #Tributo("El Rabano Picante", frase_asesinato="...", frase_counter="..."),
    
    #Tributo("ARBOL", frase_asesinato="...", frase_counter="..."),
    #Tributo("Frank Mafia", frase_asesinato="Esto es algo que tenia que hacerse. Entiendes? Si, entiendes", frase_counter="Parece que no entiendes, endiendes?"),
    #Tributo("El Choriquezo", frase_asesinato="OORALLEE MORRO", frase_counter="PERATEEEE"),
    #Tributo("CDI Mario", frase_asesinato="You know what they say. All toasters toast toasts", frase_counter="Nou"),
    Tributo("Benito", frase_asesinato="Yo soy solo una victima", frase_counter="Esta me la ensenio don gato"),
    #Tributo("Fogo: El mimo triste", frase_asesinato="*carita_trsite*", frase_counter="*carita_mas_trsite*"),
    #Tributo("Pastel de Frutas", frase_asesinato="...", frase_counter="..."),
    #Tributo("El jinete sin caballo", frase_asesinato="Esto es solo justicia", frase_counter="No necesito de un caballo para ser un jinete"),
    Tributo("Tom six: el vaquero mas lento del este", frase_asesinato="eeeey creeeoo que estaas acabadooo", frase_counter="Podreee ser lento pero eso no significa que no sea raaapido"),
    #Tributo("Un plato de avena fria", frase_asesinato="...", frase_counter="..."),
    #Tributo("Quaker: El Lord de la avena", frase_asesinato="Siente el poder de la avena", frase_counter="Recibe la furia de todos los cereales"),
    #Tributo("Gorilaman", frase_asesinato="*gritos incomprensibles*", frase_counter="*gritos incomprensibles*"),
    Tributo("El REY de hyrule", frase_asesinato="This is the power every warrioe strives for", frase_counter="Mah Boi"),
    #Tributo("CDI Green Mario", frase_asesinato="Spagettiii", frase_counter="Mama Luigi for you"),
    Tributo("Don Gato", frase_asesinato="Matute no tiene porque enterarse de esto", frase_counter="Si alguien pregunta, dire que fue benito"),
    #Tributo("Velo el velociraptor", frase_asesinato="KEUGH KEEUGH", frase_counter="KEEUUUUGH"),
    #Tributo("Atila el I-II", frase_asesinato="Tan sencillo como conquistar babilonia", frase_counter="Los segundos siempre seran los primers. GWAARH"),
    #Tributo("Chabelo", frase_asesinato="Orale cuate!", frase_counter="Deja te lo catafixeo"),
    Tributo("El Defenestrador", frase_asesinato="El defenestrador hace su parte", frase_counter="Nadie va a salir por la puerta"),
    #Tributo("Squicky el Payaso", frase_asesinato="*squik*", frase_counter="*squik**squik*"),
    #Tributo("Pingu", frase_asesinato="*Knog-Knog*", frase_counter="*pitido raro* MODAFUKA"),
    #Tributo("Skeletor", frase_asesinato="No me gusta ser bueno!", frase_counter="NiMergas!"),
    Tributo("Elmo", frase_asesinato="Elmo sabia donde vives", frase_counter="No seas malo con elmo"),
    Tributo("Ranger rojo", frase_asesinato="TIRANOSAURIO", frase_counter="ESPADA DE PODER"),
    Tributo("Michel Jordan", frase_asesinato="DUnked", frase_counter="SLLammed"),
    #Tributo("Capitan crunch", frase_asesinato="Crujientizado", frase_counter="Parte de un desayuno completo"),
    #Tributo("Peque: el pirata enano", frase_asesinato="Yargg", frase_counter="Por burlarte de mis piernas pequenias"),
    #Tributo("El conejo de andre", frase_asesinato="GIMME FOOD ASSHOLE", frase_counter="Im ALWAYS HUNGRY"),
    
    Tributo("Matute", frase_asesinato="DONNGAAATOOOO", frase_counter="Falsa alarma"),
    Tributo("Mr T *ovacion*", frase_asesinato="Mr T only needs one letter!", frase_counter="I pitty the foo"),
    Tributo("Trigre tonio(tm)", frase_asesinato="Rrrrrriquisimo", frase_counter="Tengo la energia para ganar!"),
    Tributo("Ripster the street shark", frase_asesinato="JAWSOME", frase_counter="SHARK and ROLL"),
    Tributo("Mighty Max", frase_asesinato="El poder esta en mi gorra", frase_counter="Yo soy el elegido!"),
    Tributo("Golden Age Batman", frase_asesinato="Si, comisionado", frase_counter="Nooooo, comisionadooo!"),
    #Tributo("T-Bone", frase_asesinato="Radical", frase_counter="Bingo"),
    Tributo("Indiana Jones", frase_asesinato="Serpientes?!", frase_counter="Nazis...odio a esos tipos"),
    Tributo("Mad Maxx", frase_asesinato="Esto es un circo de ratas, y comienza a gustarme", frase_counter="Demosle a la tormenta una cucharada de su propia arena"),
    Tributo("Birdman", frase_asesinato="Con el poder del sol!", frase_counter="VENGADOR...traele a Birdman un cafe"),
    Tributo("El fantasma del espacio", frase_asesinato="Nunca descansare hasta que lleve justicia!", frase_counter="MOLTAR?!"),
    Tributo("Capitan planeta", frase_asesinato="Por sus poderes unidos yo soy el capitan planeta!", frase_counter="El poder es tuyo!"),
    Tributo("Pilon", frase_asesinato="Una hamburguesa porfavor", frase_counter="Con gusto pagare el martes"),
    Tributo("Rubik: El cubo del demonio", frase_asesinato="My name is ruuuuubick", frase_counter="That was soooo fun"),
    Tributo("Hulk Hogan", frase_asesinato="IM HERE BROTHA", frase_counter="IM HERE TO WRECK SOME NONGOLS"),
]


