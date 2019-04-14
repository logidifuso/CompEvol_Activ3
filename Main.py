""" --------------------------------------------------------------------------
                            Importación de módulos
    -------------------------------------------------------------------------- """
import numpy as np
import interprete_gramatica
from Individuo import Individuo

""" --------------------------------------------------------------------------
                                Parámetros
    -------------------------------------------------------------------------- """
TAMANO_POBLACION = 3
LONG_MAX_GENOTIPO = 5
MAX_WRAPS = 2

U = 0.1
K0 = 1
K1 = 10

ARCHIVO_GRAMATICA = 'gramatica_nucleos.bnf'
""" --------------------------------------------------------------------------
                                Funciones
    -------------------------------------------------------------------------- """


def muestras_de_referencia(problema):
    if problema == 'Problema0':
        x_i, x_f = -2, 4
        m = 61
        x = np.arange(x_i, x_f, m)
        y = 8*np.exp(-2*(x-2)**2)+(2*x+1)+3*np.tanh(3*x+2)
        return x, y, m
    elif problema == 'Problema1':
        x_i, x_f = -1, 3
        m = 41
        x = np.arange(x_i, x_f, m)
        y = 2*np.exp(-2*(x-1)**2)-np.exp(-(x-1)**2)
        return x, y, m
    elif problema == 'Problema2':
        x_i, x_f = 0, 4
        m = 41
        x = np.arange(x_i, x_f, m)
        y = np.sqrt(x)
        return x, y, m
    elif problema == 'Problema3':
        x_i, x_f = 0, 4
        m = 41
        x = np.arange(x_i, x_f, m)
        y = np.exp(-x)*np.sin(2*x)
        return x, y, m
    elif problema == 'Problema4':
        x_i, x_f = 2, 6
        m = 41
        x = np.arange(x_i, x_f, m)
        y = np.log(np.log(x))
        return x, y, m
    elif problema == 'Problema5':
        x_i, x_f = 0, 10
        m = 101
        x = np.arange(x_i, x_f, m)
        y = 6*np.exp(-2*x)+2*np.sin(x)-np.cos(x)
        return x, y, m
    else:
        print("Error en la selección del problema")


def evaluar_fenotipo(individuo, x):
    exec(individuo.get_fenotipo(), globals())
    evaluacion = f(x)
    return evaluacion


def calcula_fitness(individuo, problema, U, K0, K1, x_referencia, y_referencia, m):
    y = evaluar_fenotipo(individuo, x_referencia)
    sumando = 0
    for i in range(m):
        if abs(y[i]-y_referencia[i]) <= U:
            sumando = K0 * abs(y[i]-y_referencia[i])
        else:
            sumando = K1 * abs(y[i]-y_referencia[i])
        sumando += sumando
    return sumando
















""" --------------------------------------------------------------------------
                            Lee Gramática e Inicializa población
    -------------------------------------------------------------------------- """
gramatica_bnf = interprete_gramatica.Gramatica(ARCHIVO_GRAMATICA)
poblacion = []
for _ in range(TAMANO_POBLACION):
    poblacion.append(Individuo(longitud_max=LONG_MAX_GENOTIPO))

""" --------------------------------------------------------------------------
                            Ciclo generacional
    -------------------------------------------------------------------------- """

for elem in poblacion:
    fenotipo, codones_usados = gramatica_bnf.generate(elem.get_genotipo(), max_wraps=MAX_WRAPS)
    elem.set_fenotipo(fenotipo)
    elem.set_codones_usados(codones_usados)




for elem in poblacion:
    print("\n\nIndividuo:\n", elem)


'''

    exec(fenotipo, globals())
    # Rango de x a evaluar (vectorización de la evaluación de los puntos)
    x = np.arange(-1, 1, 0.5)
    print("Puntos de evaluación:", x)
    evaluacion = f(x)
    print("El resultado de la evaluación ha sido:\n", evaluacion)
'''