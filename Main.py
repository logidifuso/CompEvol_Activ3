""" --------------------------------------------------------------------------
                            Importación de módulos
    -------------------------------------------------------------------------- """
import random
import numpy as np
import interprete_gramatica
from Individuo import Individuo

""" --------------------------------------------------------------------------
                                Parámetros
    -------------------------------------------------------------------------- """
TAMANO_POBLACION = 2
LONG_MAX_GENOTIPO = 45
MAX_WRAPS = 2

U = 0.1
K0 = 1
K1 = 10

S = 0.5

ARCHIVO_GRAMATICA = 'gramatica_nucleos.bnf'
PROBLEMA_TIPO = 'Problema1'

p_mutacion = 0.0001  # todo: decidir si es una constante o se usa en algo memético
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
    for i in range(m):
        if abs(y[i]-y_referencia[i]) <= u:
            sumando = k0 * abs(y[i]-y_referencia[i])
        else:
            sumando = k1 * abs(y[i]-y_referencia[i])
        suma += sumando
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


def paso_generacional(_poblacion, prob_mutacion):

    tamano_poblacion = len(_poblacion)
    # 1) Busqueda y selección
    # TODO: Implemento solo SUS de momento. Opciones: if para elegir o \
    # varias funciones paso_generacional

    # 1.a) Asignación de las probabilidades de seleccion
    _poblacion.sort()
    pos = 0
    acum = 0

    for _elem in _poblacion:
        _elem.set_prob_lin(pos, S, tamano_poblacion)
        acum += _elem.get_prob_padre()
        _elem.set_prob_padre_acumulada(acum)
        pos += 1

    # 1.b) Selección de padres
    lista_padres = seleccion_sus(_poblacion)
    # 2) Cruzes y mutaciones
    # TODO: De momento solo con cruze de 1punto fijo!!
    random.shuffle(lista_padres)  # Barajamos los padres --> cruze aleatorio
    elite = max(_poblacion)  # Reservo el mejor de la población por si debemos aplicar elitismo
    hijos = []  # Reseteo de la población - aplicamos relevo generacional

    i = 0
    while i < (tamano_poblacion - 1):
        padres = [lista_padres[i], lista_padres[i+1]]
        hijo1, hijo2 = Individuo.crossover_1pt_fijo(padres, codones_por_kernel=15)
        hijos.append(hijo1)
        hijos.append(hijo2)
        # 3) Mutaciones
        hijos[i].muta_en_kernel(prob_mutacion, codones_por_kernel=15)
        hijos[i+1].muta_en_kernel(prob_mutacion, codones_por_kernel=15)
        # 4) Mapeo y evaluación del fitness de los hijos
        mapeo_y_fitness(hijos[i], U, K0, K1, X_REF, Y_REF, M)
        mapeo_y_fitness(hijos[i + 1], U, K0, K1, X_REF, Y_REF, M)
        i += 2

    mejor_hijo = max(hijos)

    if elite > mejor_hijo:
        peor_hijo = min(_poblacion)
        _poblacion.remove(peor_hijo)
        _poblacion.append(elite)

    return hijos


""" --------------------------------------------------------------------------
  1. Lee Gramática
  2. Genera referencias para el cálculo de fitness según el tipo de problema
  3. Inicializa población:    
      3.1 Genera individuos
      3.2 Mapea a fenotipos
                                                                                
    -------------------------------------------------------------------------- """
gramatica_bnf = interprete_gramatica.Gramatica(ARCHIVO_GRAMATICA)
poblacion = []

X_REF, Y_REF, M = muestras_de_referencia(PROBLEMA_TIPO)

for _ in range(TAMANO_POBLACION):
    poblacion.append(Individuo(longitud_max=LONG_MAX_GENOTIPO))

""" --------------------------------------------------------------------------
                            Ciclo generacional
    -------------------------------------------------------------------------- """



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