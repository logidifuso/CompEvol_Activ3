import interprete_gramatica
from Individuo import Individuo
import numpy as np

VERBOSE = False
CODON_SIZE = 127
ELITE_SIZE = 1
POPULATION_SIZE = 100
GENERATION_SIZE = 100
GENERATIONS = 30
MUTATION_PROBABILITY = 0.01
CROSSOVER_PROBABILITY = 0.7


GRAMMAR_FILE = '../gramatica_nucleos.bnf'

# Read grammar
bnf_grammar = interprete_gramatica.Gramatica(GRAMMAR_FILE)
'''
print(bnf_grammar)
print("\n\n\n")
'''

# Generación de individuo 1
genoma_prueba1 = [1, 0, 1, 2, 1, 3, 5, 6, 1, 9, 8, 9, 0, 3, 0,
                  3, 1, 3, 3, 0, 5, 8, 8, 0, 1, 7, 7, 0, 2, 4,
                  4, 0, 6, 6, 0, 2, 3, 3, 1, 8, 2, 2, 0, 9, 2, 3, 8]
fenotipo, codones_usados = bnf_grammar.generate(genoma_prueba1)


Indiv0 = Individuo(genoma_prueba1)
Indiv0.set_fenotipo(fenotipo)
Indiv0.set_codones_usados(codones_usados)
# print("\nEl primer individuo es:\n", Indiv0)

# Generación de individuo2
genoma_prueba2 = [1, 0, 1, 1, 1, 3, 1, 1, 1, 9, 1, 1, 0, 3, 0,
                  3, 1, 1, 1, 0, 5, 1, 1, 0, 1, 1, 1, 0, 2, 4,
                  4, 0, 1, 1, 0, 2, 1, 1, 1, 1, 0, 0, 0, 8, 0]
fenotipo, codones_usados = bnf_grammar.generate(genoma_prueba2)


Indiv1 = Individuo(genoma_prueba2)
Indiv1.set_fenotipo(fenotipo)
Indiv1.set_codones_usados(codones_usados)
# print("\nEl segundo individuo es:\n", Indiv1)

'''
# Mutación en kernel
print("\n\n\n")
print("Individuo original:\n", Indiv0)
print("\n")
'''
Indiv0.muta_en_kernel(0.999, 15)
'''
print("El nuevo genotipo es:", Indiv0.get_genotipo())
fenotipo, codones_usados = bnf_grammar.generate(Indiv0.get_genotipo())
print(fenotipo)
input("Pulsa Enter para continuar")

# Mutación n veces por individuo
print("\n\n\n")
print("Individuo original:\n", Indiv1)
print("\n")
Indiv1.muta_n_veces_por_indiv(4)
print("El nuevo genotipo es:", Indiv1.get_genotipo())
fenotipo, codones_usados = bnf_grammar.generate(Indiv1.get_genotipo())
print(fenotipo)
input("Pulsa Enter para continuar")
'''

'''
# Comprobación del crossover de 1pt fijo
padres = [Indiv0, Indiv1]
print("\nPadre1:\n", padres[0])
print("\nPadre2:\n", padres[1])
Indiv2, Indiv3 = Individuo.crossover_1pt_fijo(padres, 15)
#print("\n\n\n\n", Indiv2)
fenotipo, codones_usados = bnf_grammar.generate(Indiv2.get_genotipo())
Indiv2.set_fenotipo(fenotipo)
Indiv2.set_codones_usados(codones_usados)

fenotipo, codones_usados = bnf_grammar.generate(Indiv3.get_genotipo())
Indiv3.set_fenotipo(fenotipo)
Indiv3.set_codones_usados(codones_usados)

print("\n\nEl primer hijo es:\n", Indiv2)
input("Pulsa Enter para continuar")
print("\n\nEl segundo hijo es:\n", Indiv3)
'''

'''
# Comprobación del crossover de 2pts fijo
padres = [Indiv0, Indiv1]
print("\nPadre1:\n", padres[0])
print("\nPadre2:\n", padres[1])
Indiv2, Indiv3 = Individuo.crossover_2pt_fijo(padres, 15)

fenotipo, codones_usados = bnf_grammar.generate(Indiv2.get_genotipo())
Indiv2.set_fenotipo(fenotipo)
Indiv2.set_codones_usados(codones_usados)

fenotipo, codones_usados = bnf_grammar.generate(Indiv3.get_genotipo())
Indiv3.set_fenotipo(fenotipo)
Indiv3.set_codones_usados(codones_usados)

print("\n\nEl primer hijo es:\n", Indiv2)
input("Pulsa Enter para continuar")
print("\n\nEl segundo hijo es:\n", Indiv3)
'''

'''
genoma_prueba3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                  3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]

genoma_prueba4 = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                  5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                  6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]

Padre1 = Individuo(genoma_prueba3)
Padre2 = Individuo(genoma_prueba4)
Padre1.set_codones_usados(45)
Padre2.set_codones_usados(45)

padres = [Padre1, Padre2]
print("\nPadre1:\n", padres[0])
print("\nPadre2:\n", padres[1])
Indiv4, Indiv5 = Individuo.crossover_1pt_variable(padres, 15)

fenotipo, codones_usados = bnf_grammar.generate(Indiv4.get_genotipo())
Indiv4.set_fenotipo(fenotipo)
Indiv4.set_codones_usados(codones_usados)

fenotipo, codones_usados = bnf_grammar.generate(Indiv5.get_genotipo())
Indiv5.set_fenotipo(fenotipo)
Indiv5.set_codones_usados(codones_usados)

print("\n\nEl primer hijo es:\n", Indiv4)
input("Pulsa Enter para continuar")
print("\n\nEl segundo hijo es:\n", Indiv5)


print("Padre1: ", padres[0].get_genotipo())
print("Padre2: ", padres[1].get_genotipo())
print("Hijo1:  ", Indiv4.get_genotipo())
print("Hijo2:  ", Indiv5.get_genotipo())
'''

genoma_prueba3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                  2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                  3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]

genoma_prueba4 = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                  5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                  6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
                  7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                  8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]

Padre1 = Individuo(genoma_prueba3)
Padre2 = Individuo(genoma_prueba4)
Padre1.set_codones_usados(45)
Padre2.set_codones_usados(75)

padres = [Padre1, Padre2]
print("\nPadre1:\n", padres[0])
print("\nPadre2:\n", padres[1])
Indiv4, Indiv5 = Individuo.crossover_uniforme(padres)

fenotipo, codones_usados = bnf_grammar.generate(Indiv4.get_genotipo())
Indiv4.set_fenotipo(fenotipo)
Indiv4.set_codones_usados(codones_usados)

fenotipo, codones_usados = bnf_grammar.generate(Indiv5.get_genotipo())
Indiv5.set_fenotipo(fenotipo)
Indiv5.set_codones_usados(codones_usados)
'''
print("\n\nEl primer hijo es:\n", Indiv4)
input("Pulsa Enter para continuar")
print("\n\nEl segundo hijo es:\n", Indiv5)
'''

print("Padre1: ", padres[0].get_genotipo())
print("Padre2: ", padres[1].get_genotipo())
print("Hijo1:  ", Indiv4.get_genotipo())
print("Hijo2:  ", Indiv5.get_genotipo())


























