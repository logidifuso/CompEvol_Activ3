import interprete_gramatica
import math
import numpy as np


VERBOSE = False
CODON_SIZE = 127
ELITE_SIZE = 1
POPULATION_SIZE = 100
GENERATION_SIZE = 100
GENERATIONS = 30
MUTATION_PROBABILITY = 0.01
CROSSOVER_PROBABILITY = 0.7
# GRAMMAR_FILE, FITNESS_FUNCTION = "grammars/hofBoolean.pybnf", EvenNParityFitness(3)
# GRAMMAR_FILE, FITNESS_FUNCTION = "grammars/letter.bnf", StringMatch("golden")
# GRAMMAR_FILE, FITNESS_FUNCTION = "grammars/arithmetic.pybnf", MaxFitness()
# GRAMMAR_FILE, FITNESS_FUNCTION = "grammars/boolean.pybnf", XORFitness()

GRAMMAR_FILE = 'gramatica_nucleos.bnf'


# Read grammar
bnf_grammar = interprete_gramatica.Gramatica(GRAMMAR_FILE)
print(bnf_grammar)

# Genoma para testear las funciones en la clase Gramatica
genoma_prueba = [1, 0, 1, 2, 1, 3, 5, 6, 1, 9, 8, 9, 0, 3, 0, 3, \
                 1, 3, 3, 0, 5, 8, 8, 0, 1, 7, 7, 0, 2, 4, 4, 0, \
                 6, 6, 0, 2, 3, 3, 1, 8, 2, 2, 0, 9, 1]
fenotipo, codones_usados = bnf_grammar.generate(genoma_prueba)

# individuals = initialise_population(POPULATION_SIZE)
# Loop
# best_ever = search_loop(GENERATIONS, individuals, bnf_grammar,
#                         generational_replacement, tournament_selection,
#                        FITNESS_FUNCTION)
# print("Best " + str(best_ever))
print('ein?')
print(codones_usados)
print(fenotipo)

#mate = math.exp(1)
#print(mate)
"""
funcion_testeo = '''
import math
def f(x):
    return 2.0e+2*math.exp(1.0e+1*(1.0e+0 - x)**2)'''

scope = {}
exec(funcion_testeo, scope)
resultado = scope['f'](0)
print(resultado)
"""

funcion_testeo = '''
def f(x):
    return 1.0e+1*math.exp(1.0e+1*(1.0e+0 - x)**2)'''


exec(funcion_testeo, globals())
resultado = f(0)
print(resultado)

funcion_testeo = '''
def f(x):
    return 1.0e+2*math.exp(1.0e+1*(1.0e+0 - x)**2)'''

exec(funcion_testeo, globals())
resultado = f(0)
print(resultado)






x = np.arange(4)

def funcion(y):
    return y**2+np.exp(x)

h = funcion(x)
print(h)



resultado2 = f(x)
print("El resultado 2 es:", resultado2)

a='''
def x():
  print(42)
'''
scope = {}
exec(a, scope)
scope['x']()