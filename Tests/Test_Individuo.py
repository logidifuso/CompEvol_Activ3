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
print(bnf_grammar)
print("\n\n\n")

# Generación de individuo 1
genoma_prueba1 = [1, 0, 1, 2, 1, 3, 5, 6, 1, 9, 8, 9, 0, 3, 0,
                  3, 1, 3, 3, 0, 5, 8, 8, 0, 1, 7, 7, 0, 2, 4,
                  4, 0, 6, 6, 0, 2, 3, 3, 1, 8, 2, 2, 0, 9, 2]
fenotipo, codones_usados = bnf_grammar.generate(genoma_prueba1)


Indiv1 = Individuo(genoma_prueba1)
Indiv1.set_fenotipo(fenotipo)
Indiv1.set_codones_usados(codones_usados)
print("\nEl primer individuo es:\n", Indiv1)

# Generación de individuo2
genoma_prueba2 = [1, 0, 1, 1, 1, 3, 1, 1, 1, 9, 1, 1, 0, 3, 0,
                  3, 1, 1, 1, 0, 5, 1, 1, 0, 1, 1, 1, 0, 2, 4,
                  4, 0, 1, 1, 0, 2, 1, 1, 1, 1, 0, 0, 0, 8, 0]
fenotipo, codones_usados = bnf_grammar.generate(genoma_prueba2)


Indiv2 = Individuo(genoma_prueba2)
Indiv2.set_fenotipo(fenotipo)
Indiv2.set_codones_usados(codones_usados)
print("\nEl segundo individuo es:\n", Indiv2)

print("\n\n\n")
Indiv1.muta_en_kernel(0.999, 15)
print("El nuevo genotipo es:", Indiv1.get_genotipo())
fenotipo, codones_usados = bnf_grammar.generate(Indiv1.get_genotipo())
print(fenotipo)

Indiv2.muta_n_veces_por_indiv(4)
print("El nuevo genotipo es:", Indiv2.get_genotipo())
fenotipo, codones_usados = bnf_grammar.generate(Indiv2.get_genotipo())
print(fenotipo)


padres = [Indiv1, Indiv2]
Indiv3, Indiv4 = Individuo.crossover_1pt_fijo(padres, 15)
print("\n\n\n\n", Indiv3)
fenotipo, codones_usados = bnf_grammar.generate(Indiv3.get_genotipo())
Indiv3.set_fenotipo(fenotipo)
Indiv3.set_codones_usados(codones_usados)
print("\n\n\n\n", Indiv3)











# print("El número de codones usados ha sido: ", codones_usados)
# print("El fenotipo que ha quedado tras decodificar es:\n", fenotipo)
# print("\n\n\n")