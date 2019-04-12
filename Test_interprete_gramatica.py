import interprete_gramatica
import numpy as np


VERBOSE = False
CODON_SIZE = 127
ELITE_SIZE = 1
POPULATION_SIZE = 100
GENERATION_SIZE = 100
GENERATIONS = 30
MUTATION_PROBABILITY = 0.01
CROSSOVER_PROBABILITY = 0.7


GRAMMAR_FILE = 'gramatica_nucleos.bnf'


# Read grammar
bnf_grammar = interprete_gramatica.Gramatica(GRAMMAR_FILE)
print(bnf_grammar)

# Genoma para testear las funciones en la clase Gramatica
genoma_prueba = [1, 0, 1, 2, 1, 3, 5, 6, 1, 9, 8, 9, 0, 3, 0, 3, \
                 1, 3, 3, 0, 5, 8, 8, 0, 1, 7, 7, 0, 2, 4, 4, 0, \
                 6, 6, 0, 2, 3, 3, 1, 8, 2, 2, 0, 9, 1]
fenotipo, codones_usados = bnf_grammar.generate(genoma_prueba)


print("El número de codones usados ha sido: ", codones_usados)
print("El fenotipo que ha quedado tras decodificar es:\n", fenotipo)

exec(fenotipo, globals())
# Rango de x a evaluar (vectorización de la evaluación de los puntos)
x = np.arange(-1, 1, 0.5)
print("Puntos de evaluación:", x)
evaluacion = f(x)
print("El resultado de la evaluación ha sido:\n", evaluacion)



def testecillo(x):
    return +2.2e-3*np.exp(-6.6e-9*(9.9e+3 - x)**2)\
           -4.3e+5*((9.8e+1*x + 8.7e+2)**4)\
           +7.6e+2*np.tanh(4.3e-8*x + 3.2e+9)

punto = 0
resul = testecillo(0)
print("Comprobación de que la evaluación es correcta.\nLa evaluación en el punto {0} es: {1}"
      .format(str(punto), str(resul)))
