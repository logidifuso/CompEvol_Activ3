import random


class Individuo(object):

    MAX_VAL_CODON = 256
    PEOR_FITNESS = 1e9

    tag = 0

    def __init__(self, genotipo, longitud=90):
        if genotipo is None:
            self.genotipo = [random.randint(0, Individuo.MAX_VAL_CODON)
                             for _ in range(longitud)]
        else:
            self.genotipo = genotipo
        self.fenotipo = None
        self.codones_usados = 0
        self.fenotipo_compilado = False
        self.fitness = Individuo.PEOR_FITNESS
        self.id = Individuo.tag
        Individuo.tag += 1

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __str__(self):
        print("Individuo ID: ", self.id)
        print("Genotipo:", self.genotipo)
        print("Fenotipo Compilado?:", self.fenotipo_compilado)
        print("Fenotipo:\n{1}".format(self.fenotipo). format(self.fenotipo))
        print("Valor de fitness: ", self.fitness)
        print("Número de codones usados:", self.codones_usados)


# ***********************   MÉTODOS GETTERS ***************************
    def get_genotipo(self):
        return self.genotipo

    def get_fitness(self):
        return self.fitness

    def get_id(self):
        return self.id

    def get_fenotipo(self):
        return self.fenotipo

# **********************   MÉTODOS SETTERS *****************************
    def set_genotipo(self, genotipo):
        self.genotipo = genotipo

    def set_fenotipo(self, fenotipo):
        self.fenotipo = fenotipo
        self.fenotipo_compilado = True

    def set_codones_usados(self, codones_usados):
        self.codones_usados = codones_usados

    def set_fitness(self, fitness):
        self.fitness = fitness

# ----------------------------------------------------------------------------
#                        MÉTODOS DE VARIACIÓN
# ----------------------------------------------------------------------------

# ************************* MUTACIONES ***************************************
    def muta_en_kernel(self, p_mut, long_kernel):
        """
        Muta el genoma de un individuo escogiendo aleatoriamente un valor
        entero con probabilidad p_mut en cada uno de los kernels, pero SIN
        MODIFICAR EL TIPO DE KERNEL.
        Sólo se consideran los codones usados
        :param p_mut: probabilidad de mutación
        :param long_kernel: número de codones usados por kernel (15 en este caso)
        """
        for i in range(0, self.codones_usados):
            while i % long_kernel != 0:
                if random.random() < p_mut:
                    self.genotipo[i] = random.randint(0, Individuo.MAX_VAL_CODON)

    def muta_n_veces_por_indiv(self, p_mut, num_mutaciones):
        """
        Muta aleatoriamente el genoma de un individuo un número de veces dado por
        n_mutaciones. Las posiciones de los codones mutados son aleatorias. Sólo
        se consideran los codones usados para obtener el fenotipo.
        :param p_mut: pr
        :param num_mutaciones: número de mutaciones a realizar en el individuo
        """
        for _ in range(num_mutaciones):
            pos = random.randint(0, self.codones_usados)
            self.genotipo[pos] = random.randint(0, Individuo.MAX_VAL_CODON)

    def muta_en_kernel













































