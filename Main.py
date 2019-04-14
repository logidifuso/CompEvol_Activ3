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

ARCHIVO_GRAMATICA = 'gramatica_nucleos.bnf'
""" --------------------------------------------------------------------------
                                Funciones
    -------------------------------------------------------------------------- """

'''
def muestras_de_referencia(problema):
    referencia = []
    if problema == 'Problema0':
        x_i, x_f = -2, 4
        M = 61
        x = np.arange(-2, 4, M)
        y = 8
'''

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