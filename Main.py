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

""" --------------------------------------------------------------------------
                                Parámetros
    -------------------------------------------------------------------------- """
TAMANO_POBLACION = 400
LONG_MAX_GENOTIPO = 240
MAX_WRAPS = 2

U = 0.1
K0 = 1
K1 = 10

S = 1.8

ARCHIVO_GRAMATICA = 'gramatica_nucleos.bnf'
PROBLEMA_TIPO = 'Problema1'

p_mutacion = 0.05  # todo: decidir si es una constante o se usa en algo memético

NUM_EJECUCIONES = 1
MAX_GENERACIONES = 40
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
    :return:
    """
    seleccion_padres = 0
    tamano_poblacion = len(_poblacion)
    # En nuestro caso lamdda = al tamanno de la población,
    # pero dejo la variable para posibles futuros experimentos
    lambda_padres = tamano_poblacion
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


def seleccion_torneo(_poblacion):
    # TODO: Implementar la selección por torneo. Referencia ponyge2
    aux = _poblacion
    return aux


def evalua_poblacion(_poblacion, _target_fitness):
    fitnesses = []
    for el in _poblacion:
        fitnesses.append(el.get_fitness())
    media_fitness = np.average(fitnesses)
    peor = max(fitnesses)
    mejor = min(fitnesses)
    # varianza = np.var(fitnesses)
    desviacion = np.std(fitnesses)
    mejor_indiv = _poblacion[0]
    if mejor <= _target_fitness:
        hit = True
    else:
        hit = False
    return hit, mejor_indiv, media_fitness, mejor, peor, desviacion


def paso_generacional(_poblacion, prob_mutacion):

    tamano_poblacion = len(_poblacion)

    # 1.b) Selección de padres
    # TODO: Implemento solo SUS de momento. Opciones: if para elegir o \
    lista_padres = seleccion_sus(_poblacion)
    # 2) Cruzes y mutaciones
    # TODO: De momento solo con cruze de 1punto fijo!!
    random.shuffle(lista_padres)  # Barajamos los padres --> cruze aleatorio
    elite = min(_poblacion)  # Reservo el mejor de la población por si debemos aplicar elitismo
    hijos = []  # Reseteo de la población - aplicamos relevo generacional

    j = 0
    while j < (tamano_poblacion - 1):
        padres = [lista_padres[j], lista_padres[j+1]]
        #hijo1, hijo2 = Individuo.crossover_1pt_fijo(padres, codones_por_kernel=15)
        #hijo1, hijo2 = Individuo.crossover_2pt_fijo(padres, codones_por_kernel=15) #todo: cambiado el tipo cruze
        hijo1, hijo2 = Individuo.crossover_uniforme(padres, codones_por_kernel=15, umbral=0.5)
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

    return hijos


def ejecucion(max_generaciones):
    _primer_hit = False
    estadisticas = []
    poblacion_actual = []
    for _ in range(TAMANO_POBLACION):
        poblacion_actual.append(Individuo(longitud_max=LONG_MAX_GENOTIPO))

    # ----------------------    GENERACIÓN CERO    -------------------------
    # 1) Ordenación por fitness y asignación de probabilidades de selección
    # TODO: Implemento solo SUS de momento. Opciones: if para elegir o \
    # varias funciones paso_generacional
    # 1.a) Asignación de las probabilidades de seleccion
    poblacion_actual.sort()
    pos = 0
    acum = 0

    for _elem in poblacion_actual:
        _elem.set_prob_lin(pos, S, TAMANO_POBLACION)
        acum += _elem.get_prob_padre()
        _elem.set_prob_padre_acumulada(acum)
        pos += 1

    estadistica_actual = evalua_poblacion(poblacion_actual, TARGET_FITNESS)
    estadisticas.append(estadistica_actual)
    # ---------------------------------------------------------------------
    num_generacion = 1
    while num_generacion < max_generaciones:
        nueva_generacion = paso_generacional(poblacion_actual, p_mutacion)
        poblacion_actual = nueva_generacion
        #print("\n\n", min(nueva_generacion)) # todo: A quitar
        estadistica_actual = evalua_poblacion(nueva_generacion, TARGET_FITNESS)
        if (estadistica_actual[0] is True) and (_primer_hit is False):
            _primer_hit = num_generacion
        estadisticas.append(estadistica_actual)
        num_generacion += 1
    return _primer_hit, estadisticas


""" --------------------------------------------------------------------------
  1. Lee Gramática
  2. Genera referencias para el cálculo de fitness según el tipo de problema
  3. Inicializa población:    
      3.1 Genera individuos
      3.2 Mapea a fenotipos
                                                                                
    -------------------------------------------------------------------------- """
gramatica_bnf = interprete_gramatica.Gramatica(ARCHIVO_GRAMATICA)


X_REF, Y_REF, M = muestras_de_referencia(PROBLEMA_TIPO)
TARGET_FITNESS = K0 * U  # TODO: OJO!!! que esto no garantiza un hit completo
# TODO: Podria ser que todos los errores fueran 0 y uno "grande"


ejecuciones = []
AES = 0
SR = 0
for i in range(NUM_EJECUCIONES):
    # print("ejecucion número: ", i)  todo: A quitar
    start = time.time()
    primer_hit, estad_ejecucion = ejecucion(MAX_GENERACIONES)
    if primer_hit is not False:
        AES += primer_hit * TAMANO_POBLACION
    end = time.time()
    ejecuciones.append(estad_ejecucion)

print("Tiempo requerido: %s" % (end-start))

AES /= NUM_EJECUCIONES
SR = (100*SR) / NUM_EJECUCIONES
print("\nNumero de ""runs"": ", NUM_EJECUCIONES)
print("Usando como criterio de exito un valor de fitness máximo =", TARGET_FITNESS)
print("El AES obtenido es:", AES)
print("El SR (Success Rate) obtenido es: " + str(SR) + "%")

ejecuciones = np.asarray(ejecuciones)   # Typecast como np array para facilitar los cálculos de las estadísticas


'''
#####################################################################################################
# Obtener parámetros de la lista de parámetros para usar en los plots y cálculo de estadísticas
#####################################################################################################
#num_generaciones = int(lista_param[18]) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
num_generaciones = ex.max_generaciones
tipo_funcion = ex.tipo_funcion
x_i = ex.x_i
x_f = ex.x_f
num_muestras = ex.num_muestras
kernels = ex.kernels
#tipo_funcion = lista_param[1]
#x_i = float(lista_param[6])
#x_f = float(lista_param[7])
#num_muestras = int(lista_param[8])
#kernels = int(lista_param[5])

'''


####################################################################################################
# 1. Cálculo del MBF
# 2. Plot la mejor aproximación
# Nota: como mejor individuo por ejecución escojo el mejor de la última generación (excepto en algún caso
# raro y aparente además, como por ejemplo con selección (lambda, mu) y pocas generaciones será correcto)
####################################################################################################

def chinpun(_ejecuciones):
    MBF = _ejecuciones[0, MAX_GENERACIONES - 1, 3]
    mejor_individuo = _ejecuciones[0, MAX_GENERACIONES - 1, 1]
    fitness_candidato = _ejecuciones[0, MAX_GENERACIONES - 1, 3]
    print("Mejor individuo propuesto:\n", mejor_individuo)
    #input()

    i = 1
    while i < NUM_EJECUCIONES:
        MBF += _ejecuciones[i, MAX_GENERACIONES - 1, 3]
        if _ejecuciones[i, MAX_GENERACIONES - 1, 3] < fitness_candidato:
            mejor_individuo = _ejecuciones[i, MAX_GENERACIONES - 1, 1]
        i += 1
    MBF /= NUM_EJECUCIONES
    print("El MBF obtenido es: ", MBF)
    print("El mejor individuo es:", mejor_individuo)
    #input()

#   -------------   Gráfico con la mejor aproximación ---------------
    fig, ax = plt.subplots()

    line1, = ax.plot(X_REF, Y_REF, label=PROBLEMA_TIPO)
    print("\n\nEl fenotipo del mejor individuo que vamos a evaluar es:\n", mejor_individuo.get_fenotipo())
    #input("Pulsa enter para continuar")
    line2, = ax.plot(X_REF, evaluar_fenotipo(mejor_individuo, X_REF),
                     "o", label='Mejor individuo')

    ax.set_xlim([min(X_REF), max(X_REF)])

    ax.set_title("Función objetivo y aproximación")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid()

    ax.legend()
    plt.show()
    return

chinpun(ejecuciones)

################################## CALCULO DE ESTADÍSTICAS ###################################################
vector_hits = ejecuciones[:, :, 0]  # donde cada elem del vector corresponde a una ejecución del experimento
vector_mejores = ejecuciones[:, :, 1]
vector_medias_fitness = ejecuciones[:, :, 2]
vector_mejor_fitness = ejecuciones[:, :, 3]
vector_peor_fitness = ejecuciones[:, :, 4]
vector_desviacion = ejecuciones[:, :, 5]

media_medias_fitness = np.average(vector_medias_fitness, 0)
media_mejor_fitness = np.average(vector_mejor_fitness, 0)  # Mean Best fitness
media_peor_fitness = np.average(vector_peor_fitness, 0)
media_desviacion = np.average(vector_desviacion, 0)

mejor_mejores_fitness = np.amin(vector_mejor_fitness, 0)  # Best ever case per generation
peor_peores_fitness = np.amax(vector_peor_fitness, 0)  # Worst ever case per generation

#####################################################################################################
############################### PLOTS DE PROGRESO O CONVERGENCIA   ##################################
#####################################################################################################

###########################  Medias del fitness por generación    ###################################
x = np.arange(MAX_GENERACIONES)
fig, ax = plt.subplots()

line1 = ax.plot(x, media_medias_fitness, label='Media del fitness')
line2 = ax.plot(x, media_mejor_fitness, label='Media del mejor')
# line3 = ax.plot(x, mejor_mejores_fitness, label='Mejores individuo')
# line4 = ax.plot(x, peor_peores_fitness, label='Peores individuos')
line5 = ax.plot(x, media_peor_fitness, label='Media del peor')

ax.set_ylim([0.001, 10])
ax.set_xlim([0, MAX_GENERACIONES])

ax.set_title("Medias de los fitness por generacion")
ax.set_xlabel("Generacion")
ax.set_ylabel("Valor del error")

ax.set_yscale('log')

ax.grid(True)
ax.legend()
plt.show()

#########################  Variación máxima del fitness por generación  ###############################
fig, ax = plt.subplots()

# line1 = ax.plot(x, media_medias_fitness, label='Media del fitness')
line2 = ax.plot(x, media_mejor_fitness, label='Media del mejor')
line3 = ax.plot(x, mejor_mejores_fitness, label='Mejores individuo')
line4 = ax.plot(x, peor_peores_fitness, label='Peores individuos')
# line5 = ax.plot(x, media_peor_fitness, label='Media del peor')

ax.set_ylim([0.001, 10])
ax.set_xlim([0, MAX_GENERACIONES])

ax.set_title("Variación máxima del fitness por generación")
ax.set_xlabel("Generacion")
ax.set_ylabel("Valor del error")

ax.set_yscale('log')

ax.grid(True)
ax.legend()
plt.show()

##################  Media de la desviación típica del fitness por generación  #########################
fig, ax = plt.subplots()

line1 = ax.plot(x, media_desviacion, label='Media de la desviacion típica')

ax.set_ylim([0.0001, 0.1])
ax.set_xlim([0, MAX_GENERACIONES])

ax.set_title("Media de la desviación típica de la función de error")
ax.set_xlabel("Generacion")
ax.set_ylabel("Valor del error")

ax.set_yscale('log')

ax.grid(True)
ax.legend()
plt.show()

##################  Mejor fitness por generación de cada ejecución  #########################
fig, ax = plt.subplots()

for i in range(MAX_GENERACIONES):
    ej_mejor_fitness = ejecuciones[i, :, 3]
    etiqueta = str("Run %i" % i)
    line1 = ax.plot(x, ej_mejor_fitness, label=etiqueta)

ax.set_ylim([0.001, 10])
ax.set_xlim([0, MAX_GENERACIONES])

ax.set_title("Mejor fitness por generacion")
ax.set_xlabel("Generacion")
ax.set_ylabel("Valor del error")

ax.set_yscale('log')

ax.grid(True)
ax.legend()
plt.show()

# print(ejecuciones)














































# poblacion = []
# for _ in range(TAMANO_POBLACION):
#    poblacion.append(Individuo(longitud_max=LONG_MAX_GENOTIPO))

""" --------------------------------------------------------------------------
                            Ciclo generacional
    -------------------------------------------------------------------------- """

'''
print("\n\n\n\n")
_hijos = paso_generacional(poblacion, p_mutacion)


for elem in poblacion:
    mapeo_y_fitness(elem, U, K0, K1, X_REF, Y_REF, M)
    print("\n\nIndividuo:\n", elem)   # todo: quitar print

for elem in _hijos:
    print(elem)
    print("\n")

# for elem in hijos:
#    print("\n\nIndividuo hijo:\n", elem)   # todo: quitar print
'''

'''
GRAMMAR_FILE = 'gramatica_nucleos.bnf'
# Read grammar
bnf_grammar = interprete_gramatica.Gramatica(GRAMMAR_FILE)
print(bnf_grammar)

# Genoma para testear las funciones en la clase Gramatica
genoma_prueba = [1, 0, 1, 2, 1, 3, 5, 6, 1, 9, 8, 9, 1, 2, 0, 3, \
                 1, 3, 3, 0, 1, 8, 8, 1, 1, 7, 7, 1, 2, 1, 4, 0, \
                 6, 6, 0, 2, 3, 3, 1, 8, 2, 2, 0, 1, 1]
fenotipo, codones_usados = bnf_grammar.generate(genoma_prueba)


# print("El número de codones usados ha sido: ", codones_usados)
print("El fenotipo que ha quedado tras decodificar es:\n", fenotipo)

exec(fenotipo, globals())
# Rango de x a evaluar (vectorización de la evaluación de los puntos)
x_test = np.arange(-1, 1, 0.5)
print("Puntos de evaluación:", x_test)
evaluacion = f(x_test)
print("El resultado de la evaluación ha sido:\n", evaluacion)
'''
'''
x_referencia = [-1.  -0.5  0.   0.5]#
y_referencia 

def calcula_fitness(individuo, U, K0, K1, x_referencia, y_referencia, m):
'''
'''
x_ref = np.array([-1., -0.5, 0.,  0.5])
y_ref = np.array([798.4012, 777.3312, 756.2612, 735.1912])

indiv = Individuo(genoma_prueba)
indiv.set_fenotipo(fenotipo)
indiv.set_codones_usados(codones_usados)
print(indiv)

print("\n\n\n\n\n")

fitness = calcula_fitness(indiv, U, K0, K1, x_ref, y_ref, m=3)

print("El fitness calculado es:", fitness)
'''