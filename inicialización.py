from Individuo import Individuo
from parametros import params
import random
'''
def inicia_rhh(_tamano_poblacion, min_long_fenotipo, max_long_fenotipo, codones_kernel = 15):
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

    if _tamano_poblacion%2 != 0:
        _tamano_poblacion +=1
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
            indiv = genera_indiv_aleat(longitud)
            poblacion.append(indiv)

            # Genera individuo con el método "Full"
            indiv = genera_indiv_full(longitud)
            poblacion.append(indiv)

    return poblacion

'''
def genera_indiv_full(longitud_fenotipo, codones_kernel = 15, expresiones = [1, 3, 5]):
    genotipo = []
    for i in range(longitud_fenotipo * codones_kernel):
        if i % codones_kernel == 0:
            genotipo.append(random.choice(expresiones))
        elif (i + 5) % codones_kernel == 0: # --> Condiciones para exponentes son posibles, p.e.
            genotipo.append(1)
        else:
            genotipo.append(random.randint(10, 20))

    return genotipo

def genera_indiv_aleat(longitud_fenotipo, codones_kernel = 15, expresiones = [1, 3, 5])
    genotipo = [random.randint(0, Individuo.MAX_VAL_CODON)
                 for _ in range(random.randint(longitud_fenotipo*codones_kernel,
                                               params['LONG_MAX_GENOTIPO']))]



test = genera_indiv_full(5)
print(test)
