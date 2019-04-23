from Individuo import Individuo
from parametros import params
import random


def inicia_rhh(_tamano_poblacion, min_long_fenotipo, max_long_fenotipo):
    """
    Crea una población del tamanno '_tamano_poblacion' usando el algoritmo ramped
    half-and-half
    :param _tamano_poblacion: Debe ser un número par, sino, se annadirá 1
    :param min_long_fenotipo
    :param max_long_fenotipo
    :return: La población de individuos generada
    """

    longitudes_fenotipos = range(min_long_fenotipo + 1, max_long_fenotipo + 1)

    poblacion = []

    if _tamano_poblacion % 2 != 0:
        _tamano_poblacion += 1
        print("Se annadió 1 individuo para tener una población par")

    if _tamano_poblacion/2 < len(longitudes_fenotipos):
        # La población es demasiado pequenna para cubrir todas las
        # longitudes de genotipos. Hay que recortar estas longitudes
        longitudes_fenotipos = longitudes_fenotipos[:int(_tamano_poblacion/2)]

    # Calculamos el número de individuos a generar con cada uno de los 2
    # métodos (ramp y completo)
    num_vueltas = int((_tamano_poblacion/2)/len(longitudes_fenotipos))
    resto = int(_tamano_poblacion/2 - (num_vueltas * len(longitudes_fenotipos)))

    # Creacción de los individuos del num_vueltas (ramped half and half)
    for longitud in longitudes_fenotipos:
        for i in range(num_vueltas):
            # Genera individuo con el métod "Grow"
            genotipo = genera_indiv_aleat(longitud)
            poblacion.append(Individuo(genotipo))

            # Genera individuo con el método "Full"
            genotipo = genera_indiv_full(longitud)
            poblacion.append(Individuo(genotipo))

    if resto:  # si aún no se ha llegado a completar la población deseada
        longitudes_fenotipos = list(longitudes_fenotipos)
        random.shuffle(longitudes_fenotipos)

    for i in range(resto):
        longitud = longitudes_fenotipos.pop()

        genotipo = genera_indiv_aleat(longitud)
        poblacion.append(Individuo(genotipo))

        genotipo = genera_indiv_full(longitud)
        poblacion.append(Individuo(genotipo))

    return poblacion


def genera_indiv_full(longitud_fenotipo, codones_kernel=15, expresiones=[1, 3, 5]):
    genotipo = []
    chequeo5 = 5
    chequeo9 = 9
    chequeo13 = 13
    chequeo14 = 14
    for i in range((longitud_fenotipo - 1) * codones_kernel):
        if i % codones_kernel == 0:
            #genotipo.append(1)
            genotipo.append(random.choice(expresiones))
        elif i == chequeo5:  # --> Condiciones para exponentes son posibles, p.e.
            genotipo.append(0)
            chequeo5 += 15
        elif i == chequeo9:
            genotipo.append(0)
            chequeo9 += 15
        elif i == chequeo13:
            genotipo.append(0)
            chequeo13 += 15
        elif i == chequeo14:
            genotipo.append(1)
            chequeo14 += 15
        else:
            genotipo.append(random.randint(0, params['MAX_VAL_CODON']))
    # El último grupo de 15 codones se genera de entre las opciones que no
    # extenderían más el fenotipo en un 75% de los casos. En un 25% se sigue
    # alargando el fenotipo
    if random.random() < 0.75:
        genotipo.append(random.choice([0, 2, 4]))
    else:
        genotipo.append((random.choice(expresiones)))
    # Para evitar individuos inválidos se annaden 2 codones más de los
    # necesarios si la elección anterior cayó en el 25% de los casos
    # todo: ojo a la modificación, a ver si va o luego la quieres quitar
    for i in range(codones_kernel+2):
        if i == chequeo5:
            genotipo.append(0)
            chequeo5 += 15
        elif i == chequeo9:
            genotipo.append(0)
            chequeo9 += 15
        elif i == chequeo13:
            genotipo.append(0)
            chequeo13 += 15
        elif i == chequeo14:
            genotipo.append(1)
            chequeo14 += 15
        else:
            genotipo.append(random.randint(0, params['MAX_VAL_CODON']))
    return genotipo


def genera_indiv_aleat(longitud_fenotipo, codones_kernel=15):
    genotipo = [random.randint(0, Individuo.MAX_VAL_CODON)
                for _ in range(random.randint(longitud_fenotipo*codones_kernel,
                                              params['LONG_MAX_GENOTIPO']))]
    return genotipo


'''
test = genera_indiv_full(5)
print(test)
'''

'''
import interprete_gramatica

gramatica_bnf = interprete_gramatica.Gramatica("gramatica_nucleos.bnf")
test2 = inicia_rhh(8, 1, 2)


for individuo in test2:
    _genotipo = individuo.get_genotipo()
    _fenotipo, _codones_usados = gramatica_bnf.generate(_genotipo)
    individuo.set_fenotipo(_fenotipo)
    individuo.set_codones_usados(_codones_usados)

print("\n\n\n")
for el in test2:
    print("\n", el)

'''