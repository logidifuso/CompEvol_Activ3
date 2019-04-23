""" --------------------------------------------------------------------------
                            Importación de módulos
    -------------------------------------------------------------------------- """
import random
import numpy as np
import time
import csv
import matplotlib.pyplot as plt
import interprete_gramatica
from Individuo import Individuo
import graficos_progreso as graf
from inicialización import inicia_rhh
from parametros import params
import pandas as pd

""" --------------------------------------------------------------------------
                                Parámetros
    -------------------------------------------------------------------------- """
# TODO: De momento leo estos parámetros y los dejo como variables por si luego queremos
# implementar algún tipo de algoritmo memético con ellos
U = params['U']
K0 = params['K0']
K1 = params['K1']
S = params['S']

p_mutacion = 0.05  # todo: decidir si es una constante o se usa en algo memético

# TAMANO_POBLACION = 5000
# LONG_MAX_GENOTIPO = 240
# MAX_WRAPS = 2
# ARCHIVO_GRAMATICA = 'gramatica_nucleos.bnf'
# PROBLEMA_TIPO = 'Problema1'
# OPCION_SELECCION = "Torneo"
# TAMANO_TORNEO = 2
# NUM_EJECUCIONES = 5
# MAX_GENERACIONES = 8
""" --------------------------------------------------------------------------
                                Funciones
    -------------------------------------------------------------------------- """


def muestras_de_referencia(problema):
    if problema == 'Problema0':
        x_i, x_f = -2, 4
        m = 61
        x = np.linspace(x_i, x_f, m)
        y = 8*np.exp(-2*(x-2)**2)+(2*x+1)+3*np.tanh(3*x+2)
        return x, y, m
    elif problema == 'Problema1':
        x_i, x_f = -1, 3
        m = 41
        x = np.linspace(x_i, x_f, m)
        y = 2*np.exp(-2*(x-1)**2)-np.exp(-(x-1)**2)
        return x, y, m
    elif problema == 'Problema2':
        x_i, x_f = 0, 4
        m = 41
        x = np.linspace(x_i, x_f, m)
        y = np.sqrt(x)
        return x, y, m
    elif problema == 'Problema3':
        x_i, x_f = 0, 4
        m = 41
        x = np.linspace(x_i, x_f, m)
        y = np.exp(-x)*np.sin(2*x)
        return x, y, m
    elif problema == 'Problema4':
        x_i, x_f = 2, 6
        m = 41
        x = np.linspace(x_i, x_f, m)
        y = np.log(np.log(x))
        return x, y, m
    elif problema == 'Problema5':
        x_i, x_f = 0, 10
        m = 101
        x = np.linspace(x_i, x_f, m)
        y = 6*np.exp(-2*x)+2*np.sin(x)-np.cos(x)
        return x, y, m
    else:
        print("Error en la selección del problema")


def evaluar_fenotipo(individuo, x):
    exec(individuo.get_fenotipo(), globals())
    resul = f(x)
    return resul


def calcula_fitness(individuo, u, k0, k1, x_referencia, y_referencia, m):
    if individuo.get_fenotipo() is None:
        return 1.0e32   # Retorna un número elevado si el individuo es inválido
    y = evaluar_fenotipo(individuo, x_referencia)
    suma = 0
    for j in range(m):
        if abs(y[j]-y_referencia[j]) <= u:
            sumando = k0 * abs(y[j]-y_referencia[j])
        else:
            sumando = k1 * abs(y[j]-y_referencia[j])
        suma += sumando
    suma /= m
    return suma


def mapeo_y_fitness(individuo, u, k0, k1, x_referencia, y_referencia, m):
    # 1) Mapear genotipo a fenotipo y asignarlo al individuo -> generate -> set_fenotipo
    _genotipo = individuo.get_genotipo()
    _fenotipo, _codones_usados = gramatica_bnf.generate(_genotipo)
    individuo.set_fenotipo(_fenotipo)
    individuo.set_codones_usados(_codones_usados)
    # 2) evaluar y apuntar el fitness al individuo --> calcula_fitness
    fitness_indiv = calcula_fitness(individuo, u, k0, k1,
                                    x_referencia, y_referencia, m)
    individuo.set_fitness(fitness_indiv)


def seleccion_sus(_poblacion):
    """
    Selección de padres usando el algoritmo estocástico universal (SUS)
    :param _poblacion:
    :return: lista_padres
    """
    validos = [_i for _i in _poblacion
               if _i.get_genotipo() is not None]
    validos.sort()
    pos = 0
    acum = 0

    for _elem in validos:
        _elem.set_prob_lin(pos, S, len(validos))
        acum += _elem.get_prob_padre()
        _elem.set_prob_padre_acumulada(acum)
        pos += 1

    seleccion_padres = 0
    # tamano_poblacion = len(_poblacion)
    # En nuestro caso lamdda = al tamanno de la población,
    # pero dejo la variable para posibles futuros experimentos
    lambda_padres = len(validos)
    indice = 0
    r = np.random.uniform(0, 1/lambda_padres)
    lista_padres = []

    while seleccion_padres < lambda_padres:
        while r <= _poblacion[indice].get_prob_padre_acumulada():
            lista_padres.append(_poblacion[indice])
            r = r + 1/lambda_padres
            seleccion_padres += 1
        indice += 1
    return lista_padres


def seleccion_torneo(_poblacion, tamano_torneo):
    """
    Dada una población, realiza una selección por torneos, retornando
    a los vencedores. Sólamente individuos válidos pueden ser seleccionados
    :param _poblacion:
    :param tamano_torneo: número de oponentes en cada torneo
    :param
    :return: ganadores: lista de los vencedores de los torneos.
    """
    # TODO: Ponyge2 da la opción de poder seleccionar indiv no válidos (flag:Invalid selection) --> tú también?
    seleccion_padres = 0
    tamano_poblacion = len(_poblacion)
    # En nuestro caso lamdda = al tamanno de la población,
    # pero dejo la variable para posibles futuros experimentos
    lambda_padres = tamano_poblacion
    ganadores = []
    validos = [_i for _i in _poblacion
               if _i.get_fenotipo() is not None]

    while seleccion_padres < lambda_padres:
        oponentes = random.sample(validos, tamano_torneo)
        ganadores.append(min(oponentes))
        seleccion_padres += 1
    return ganadores


def evalua_poblacion(_poblacion, _target_fitness):
    fitnesses = []
    for el in _poblacion:
        fitnesses.append(el.get_fitness())
    media_fitness = np.average(fitnesses)
    peor = max(fitnesses)
    mejor = min(fitnesses)
    # varianza = np.var(fitnesses)
    desviacion = np.std(fitnesses)
    mejor_indiv = min(_poblacion)   # _poblacion[0] :todo: correcto??
    if mejor <= _target_fitness:
        hit = True
    else:
        hit = False
    return hit, mejor_indiv, media_fitness, mejor, peor, desviacion


def paso_generacional(_poblacion, prob_mutacion, opc_seleccion):

    tamano_poblacion = len(_poblacion)

    # 1.b) Selección de padres
    # TODO: Implemento solo SUS de momento. Opciones: if para elegir o \
    if opc_seleccion == "Torneo":
        lista_padres = seleccion_torneo(_poblacion, params['TAMANO_TORNEO'])
    else:
        lista_padres = seleccion_sus(_poblacion)
    # 2) Cruzes y mutaciones
    # TODO: De momento solo con cruze de 1punto fijo!!
    random.shuffle(lista_padres)  # Barajamos los padres --> cruze aleatorio
    elite = min(_poblacion)  # Reservo el mejor de la población por si debemos aplicar elitismo
    hijos = []  # Reseteo de la población - aplicamos relevo generacional

    j = 0
    while j < (tamano_poblacion - 1):
        padres = [lista_padres[j], lista_padres[j+1]]
        hijo1, hijo2 = Individuo.crossover_1pt_fijo(padres, codones_por_kernel=15)
        # hijo1, hijo2 = Individuo.crossover_2pt_fijo(padres, codones_por_kernel=15) #todo: cambiado el tipo cruze
        # hijo1, hijo2 = Individuo.crossover_uniforme(padres, codones_por_kernel=15, umbral=0.5)
        hijos.append(hijo1)
        hijos.append(hijo2)
        # 3) Mutaciones
        hijos[j].muta_en_kernel(prob_mutacion, codones_por_kernel=15)
        hijos[j+1].muta_en_kernel(prob_mutacion, codones_por_kernel=15)
        # 4) Mapeo y evaluación del fitness de los hijos
        mapeo_y_fitness(hijos[j], U, K0, K1, X_REF, Y_REF, M)
        mapeo_y_fitness(hijos[j + 1], U, K0, K1, X_REF, Y_REF, M)
        j += 2

    peor_hijo = max(hijos)
    if elite < peor_hijo:
        hijos.remove(peor_hijo)
        hijos.append(elite)

    '''
    # 1) Ordenación por fitness y asignación de probabilidades de selección
    # TODO: Implemento solo SUS de momento. Opciones: if para elegir o \
    # varias funciones paso_generacional
    # 1.a) Asignación de las probabilidades de seleccion
    hijos.sort()
    pos = 0
    acum = 0
    
    for _elem in hijos:
        _elem.set_prob_lin(pos, S, tamano_poblacion)
        acum += _elem.get_prob_padre()
        _elem.set_prob_padre_acumulada(acum)
        pos += 1
        
    '''
    return hijos


def ejecucion(max_generaciones):
    """
1. Inicializa población: genera individuos, mapea a fenotipos, ordena
y asigna probabilidades de selección
2. Bucle generacional: Itera max_generaciones el proceso
(función paso_generacional)

    :param max_generaciones:
    :return:
    '''
    '''
    :param max_generaciones:
    :return: _primer_hit (generación que consiguió un "Hit completo" o False si
no alcanzó), estadisticas de cada generación
    """
    _primer_hit = False
    estadisticas = []
    # poblacion_actual = []
    # TODO: Implementar Ramp half-and-half
    poblacion_actual = inicia_rhh(params['TAMANO_POBLACION'],
                                  params['MIN_LONG_FENOTIPO_INICIAL'],
                                  params['MAX_LONG_FENOTIPO_INICIAL'])
    for indiv in poblacion_actual:
        mapeo_y_fitness(indiv, U, K0, K1, X_REF, Y_REF, M)
    '''
    for _ in range(TAMANO_POBLACION):
        nuevo_individuo = Individuo(longitud_max=LONG_MAX_GENOTIPO)
        mapeo_y_fitness(nuevo_individuo, U, K0, K1, X_REF, Y_REF, M)
        poblacion_actual.append(nuevo_individuo)
    '''

    # -------------------    Inicializa población    -------------------------
    # 1) Ordenación por fitness y asignación de probabilidades de selección
    # TODO: Implemento solo SUS de momento. Opciones: if para elegir o \
    # varias funciones paso_generacional
    # 1.a) Asignación de las probabilidades de seleccion
    poblacion_actual.sort()
    pos = 0
    acum = 0

    for _elem in poblacion_actual:
        _elem.set_prob_lin(pos, S, params['TAMANO_POBLACION'])
        acum += _elem.get_prob_padre()
        _elem.set_prob_padre_acumulada(acum)
        pos += 1

    estadistica_actual = evalua_poblacion(poblacion_actual, TARGET_FITNESS)
    estadisticas.append(estadistica_actual)
    # ----------------- Bucle generacional  ----------------------------------
    num_generacion = 1
    while num_generacion < max_generaciones:
        nueva_generacion = paso_generacional(poblacion_actual, p_mutacion,
                                             params['OPCION_SELECCION'])
        poblacion_actual = nueva_generacion
        # print("\n\n", min(nueva_generacion)) # todo: A quitar
        estadistica_actual = evalua_poblacion(nueva_generacion, TARGET_FITNESS)
        if (estadistica_actual[0] is True) and (_primer_hit is False):
            _primer_hit = num_generacion
        estadisticas.append(estadistica_actual)
        num_generacion += 1
    return _primer_hit, estadisticas


""" --------------------------------------------------------------------------
                        EJECUCIÓN DEL EXPERIMENTO      
    __________________________________________________________________________
  1. Lee Gramática
  2. Genera referencias para el cálculo de fitness según el tipo de problema
  3. Fija un target fitness
  4. Inicializa población:    
      3.1 Genera individuos
      3.2 Mapea a fenotipos
                                                                                
    -------------------------------------------------------------------------- """
gramatica_bnf = interprete_gramatica.Gramatica(params['ARCHIVO_GRAMATICA'])


X_REF, Y_REF, M = muestras_de_referencia(params['PROBLEMA_TIPO'])
TARGET_FITNESS = K0 * U  # TODO: OJO!!! que esto no garantiza un hit completo
# TODO: Podria ser que todos los errores fueran 0 y uno "grande"

'''
poblacion_test = inicia_rhh(8, 2, 4)
for el in poblacion_test:
    mapeo_y_fitness(el,U, K0, K1, X_REF, Y_REF, M)
    print("\n", el)

input("A ver si salió...")
'''
'''
TESTEO

genotipo_testeo = [208, 164, 238,  70,  73,
                   52,  60, 202,  22, 157,
                   63, 190, 157, 179, 238,
                   48]
testeo = Individuo(genotipo_testeo)
mapeo_y_fitness(testeo, U, K0, K1, X_REF, Y_REF, M)
print(testeo)
input("chimpún!!!")
'''


ejecuciones = []
AES = 0
SR = 0
for i in range(params['NUM_EJECUCIONES']):
    start = time.time()
    primer_hit, estad_ejecucion = ejecucion(params['MAX_GENERACIONES'])
    if primer_hit is not False:
        AES += primer_hit * params['TAMANO_POBLACION']
        SR += 1
    end = time.time()
    ejecuciones.append(estad_ejecucion)

AES /= params['NUM_EJECUCIONES']
SR = (100*SR) / params['NUM_EJECUCIONES']

# ###################### CALCULO DE ESTADÍSTICAS ######################
ejecuciones = np.asarray(ejecuciones)   # Typecast como np array para facilitar los cálculos de las estadísticas
MBF = ejecuciones[0, params['MAX_GENERACIONES'] - 1, 3]
mejor_individuo = ejecuciones[0, params['MAX_GENERACIONES'] - 1, 1]
fitness_candidato = ejecuciones[0, params['MAX_GENERACIONES'] - 1, 3]
'''
mi_dataframe = pd.DataFrame(ejecuciones)
mi_dataframe.to_csv('foo.csv', index=False)
pd.DataFrame(ejecuciones).to_csv("ejecuciones.csv")
'''
i = 1
while i < params['NUM_EJECUCIONES']:
    MBF += ejecuciones[i, params['MAX_GENERACIONES'] - 1, 3]
    if ejecuciones[i, params['MAX_GENERACIONES'] - 1, 3] < fitness_candidato:
        mejor_individuo = ejecuciones[i, params['MAX_GENERACIONES'] - 1, 1]
    i += 1
MBF /= params['NUM_EJECUCIONES']

# Muestra resultados
print("Tiempo requerido: %s" % (end - start))
print("\nNumero de ""runs"": ", params['NUM_EJECUCIONES'])
print("Usando como criterio de exito un valor de fitness máximo =", TARGET_FITNESS)
print("El AES obtenido es:", AES)
print("El SR (Success Rate) obtenido es: " + str(SR) + "%")
print("El MBF obtenido es: ", MBF)
print("\nEl mejor individuo es:", mejor_individuo)

vector_hits = ejecuciones[:, :, 0]  # donde cada elem del vector corresponde a una ejecución del experimento
vector_mejores = ejecuciones[:, :, 1]
vector_medias_fitness = ejecuciones[:, :, 2]
vector_mejor_fitness = ejecuciones[:, :, 3]
vector_peor_fitness = ejecuciones[:, :, 4]
vector_desviacion = ejecuciones[:, :, 5]

mi_dataframe = pd.DataFrame(vector_mejores)
mi_dataframe.to_csv('foo.csv', index=False)
pd.DataFrame(vector_mejores).to_csv("ejecuciones.csv")

media_medias_fitness = np.average(vector_medias_fitness, 0)
media_mejor_fitness = np.average(vector_mejor_fitness, 0)  # Mean Best fitness
media_peor_fitness = np.average(vector_peor_fitness, 0)
media_desviacion = np.average(vector_desviacion, 0)

mejor_mejores_fitness = np.amin(vector_mejor_fitness, 0)  # Best ever case per generation
peor_peores_fitness = np.amax(vector_peor_fitness, 0)  # Worst ever case per generation


def graf_mejor_aproximacion(x_ref, y_ref, problema_tipo, _mejor_individuo):
    fig, ax = plt.subplots()

    line1, = ax.plot(x_ref, y_ref, label=problema_tipo)
    # print("\n\nEl fenotipo del mejor individuo que vamos a evaluar es:\n", mejor_individuo.get_fenotipo())
    # input("Pulsa enter para continuar")
    line2, = ax.plot(x_ref, evaluar_fenotipo(_mejor_individuo, x_ref),
                     "o", label='Mejor individuo')

    ax.set_xlim([min(x_ref), max(x_ref)])

    ax.set_title("Función objetivo y aproximación")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid()

    ax.legend()
    plt.show(block=False)
    return


graf_mejor_aproximacion(X_REF, Y_REF, params['PROBLEMA_TIPO'], mejor_individuo)

graf.graf_medias_fitness_por_generacion(params['MAX_GENERACIONES'], media_medias_fitness,
                                        media_mejor_fitness, media_peor_fitness)

graf.graf_delta_fitess_por_generacion(params['MAX_GENERACIONES'], media_mejor_fitness,
                                      mejor_mejores_fitness, peor_peores_fitness)

graf.graf_media_desviacion_por_generacion(params['MAX_GENERACIONES'], media_desviacion)

graf.graf_mejor_fitness_por_generacion(params['MAX_GENERACIONES'], ejecuciones, params['NUM_EJECUCIONES'])
