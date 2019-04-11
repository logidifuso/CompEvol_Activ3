import interprete_gramatica


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

GRAMMAR_FILE = ramatica_nucleos.bnf

def mane():
    """ Run program """
    # Read grammar
    bnf_grammar = interprete_gramatica.Gramatica(GRAMMAR_FILE)
    if VERBOSE:
        print(bnf_grammar)
    # Create Individuals
    individuals = initialise_population(POPULATION_SIZE)
    # Loop
    best_ever = search_loop(GENERATIONS, individuals, bnf_grammar,
                            generational_replacement, tournament_selection,
                            FITNESS_FUNCTION)
    print("Best " + str(best_ever))
