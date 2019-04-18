

def inicia_rhh(_tamano_poblacion, min_ramp, long_max_genotipo):
    """
    Crea una población del tamanno '_tamano_poblacion' usando el algoritmo ramped
    half-and-half
    :param _tamano_poblacion: Debe ser un número par, sino, se annadirá 1
    :param min_ramp
    :param long_max_genotipo
    :return: La población de individuos generada
    """

    longitudes_fenotipos = range(min_ramp+1, long_max_genotipo+1)

    poblacion = []

    if _tamano_poblacion%2 != 0:
        _tamano_poblacion +=1
        print("Se annadió 1 individuo para tener una población par")

    if _tamano_poblacion/2 < len(longitudes_fenotipos)
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



