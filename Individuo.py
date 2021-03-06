import random
import numpy as np
import random


class Individuo(object):

    MAX_VAL_CODON = 256
    PEOR_FITNESS = 1.0e32

    tag = 0

    def __init__(self, genotipo = None, longitud_max=90):
        if genotipo is None:
            self.genotipo = [random.randint(0, Individuo.MAX_VAL_CODON)
                             for _ in range(random.randint(16, longitud_max))]
            # genera un individuo con un genotipo de longitud entre 16 y el
            # máximo establecido. La idea es evitar comenzar con un gran número
            # de individuos inválidos.
            # TODO: en randint arriba el mínimo es 1. (0 puede dar errores) --> Que valor dejas? 15? 30?
        else:
            self.genotipo = genotipo
        self.fenotipo = None
        self.codones_usados = 0
        self.fenotipo_compilado = False
        self.fitness = Individuo.PEOR_FITNESS
        self.id = Individuo.tag
        self.mating_prob = None
        self.prob_acumulada = None
        Individuo.tag += 1

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __str__(self):
        return ("Individuo ID: {0}\nGenotipo: {1}\nFenotipo Compilado: {2}\n"
                "Fenotipo:\n{3}\nValor de fitness: {4}\n"
                "Número de codones usados: {5}\n"
                "Probabilidad lineal de cruze: {6}:\n"
                "Probabilidad acumulada para cruze: {7}:"
                .format(self.id,
                        self.genotipo,
                        self.fenotipo_compilado,
                        self.fenotipo,
                        self.fitness,
                        self.codones_usados,
                        self.mating_prob,
                        self.prob_acumulada))


# ***********************   MÉTODOS GETTERS ***************************

    def get_genotipo(self):
        return self.genotipo

    def get_fitness(self):
        return self.fitness

    def get_id(self):
        return self.id

    def get_fenotipo(self):
        return self.fenotipo

    def get_prob_padre(self):
        return self.mating_prob

    def get_prob_padre_acumulada(self):
        return self.prob_acumulada

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

    def set_prob_lin(self, rank, s=1.5, mu=10):
        self.mating_prob = (2 - s) / mu + (2 * rank * (s - 1)) / (mu * (mu - 1))

    def set_prob_padre_acumulada(self, prob):
        self.prob_acumulada = prob

        # Funciones "getter" para acceder a los atributos de datos.

    # ----------------------------------------------------------------------------
#                        MÉTODOS DE VARIACIÓN
# ----------------------------------------------------------------------------

# ************************* MUTACIONES ***************************************
    def muta_en_kernel(self, p_mut, codones_por_kernel=15):
        """
        Muta el genoma de un individuo escogiendo aleatoriamente un valor
        entero con probabilidad p_mut en cada uno de los kernels, pero SIN
        MODIFICAR EL TIPO DE KERNEL.
        :param p_mut: probabilidad de mutación
        :param codones_por_kernel: número de codones usados por kernel (15 en este caso)
        """
        pos_max = len(self.get_genotipo())
        for i in range(0, pos_max):
            # if random.random() < p_mut:
            #     self.genotipo[i] = random.randint(0, Individuo.MAX_VAL_CODON)
            if i % codones_por_kernel != 0:
                if random.random() < p_mut:
                    self.genotipo[i] = random.randint(0, Individuo.MAX_VAL_CODON)

    def muta_n_veces_por_indiv(self, num_mutaciones):
        """
        Muta aleatoriamente el genoma de un individuo un número de veces dado por
        n_mutaciones. Las posiciones de los codones mutados son aleatorias.
        :param num_mutaciones: número de mutaciones a realizar en el individuo
        """
        pos_max = len(self.get_genotipo())
        for _ in range(num_mutaciones):
            pos = random.randint(0, pos_max)
            self.genotipo[pos] = random.randint(0, Individuo.MAX_VAL_CODON)

# ************************** RECOMBINACIÓN **********************************
    def crossover_1pt_fijo(padres, codones_por_kernel=15):
        """
        Crossover de 1punto fijo. Produce 2 hijos usando recombinación de punto
        fijo. Uno de los hijos tendrá la misma longitud que uno de los padres y
        el otro hijo tendrá la misma longitud que el otro padre.
        !!!!!!!!!!:param other:
        !!!!!!!!!!!:return:
        """
        long_pad1 = len(padres[0].get_genotipo())
        long_pad2 = len(padres[1].get_genotipo())
        punto_crossover_max = min(long_pad1, long_pad2)
        punto_crossover = random.randint(1, punto_crossover_max//codones_por_kernel)
        punto_crossover *= codones_por_kernel
        h1 = np.array([])
        h2 = np.array([])

        h1 = np.append(h1, padres[0].genotipo[0:punto_crossover])
        h1 = np.append(h1, padres[1].genotipo[punto_crossover:])

        h2 = np.append(h2, padres[1].genotipo[0:punto_crossover])
        h2 = np.append(h2, padres[0].genotipo[punto_crossover:])

        hijo1 = Individuo(h1.astype(int))
        hijo2 = Individuo(h2.astype(int))

        return hijo1, hijo2

    def crossover_2pt_fijo(padres, codones_por_kernel=15):
        """
        Crossover de 2 puntos fijos. Uno de los hijos tendrá la misma longitud
        que uno de los padres y el otro hijo tendrá la misma longitud que el
        otro padre. Los 2 puntos de crossover se encuentra dentro de la porción
        de genoma usado por los 2 padres.
        :param codones_por_kernel:
        :return:
        """
        long_pad1 = len(padres[0].get_genotipo())
        long_pad2 = len(padres[1].get_genotipo())
        punto_crossover_max = min(long_pad1, long_pad2)

        #punto_crossover_max = min(padres[0].codones_usados, padres[1].codones_usados)
        punto1_crossover = random.randint(0, punto_crossover_max//codones_por_kernel)
        punto2_crossover = random.randint(0, punto_crossover_max//codones_por_kernel)


        while punto1_crossover == punto2_crossover:
            punto2_crossover = random.randint(0, punto_crossover_max//codones_por_kernel)
        if punto2_crossover < punto1_crossover:
            aux = punto1_crossover
            punto1_crossover = punto2_crossover
            punto2_crossover = aux

        punto1_crossover *= codones_por_kernel
        punto2_crossover *= codones_por_kernel

        h1 = np.array([])
        h2 = np.array([])

        h1 = np.append(h1, padres[0].genotipo[0:punto1_crossover])
        h1 = np.append(h1, padres[1].genotipo[punto1_crossover:punto2_crossover])
        h1 = np.append(h1, padres[0].genotipo[punto2_crossover:])

        h2 = np.append(h2, padres[1].genotipo[0:punto1_crossover])
        h2 = np.append(h2, padres[0].genotipo[punto1_crossover:punto2_crossover])
        h2 = np.append(h2, padres[1].genotipo[punto2_crossover:])

        hijo1 = Individuo(h1.astype(int))
        hijo2 = Individuo(h2.astype(int))

        return hijo1, hijo2

    def crossover_1pt_variable(padres, codones_por_kernel=15):
        """
        Crossover de 1 punto. En este caso se utiliza un punto de crossover
        diferente para cada uno de los padres. Esto permite que los genomas
        de los hijos sean de longitudes mayores o menores que los de los
        padres. El punto de crossover para ambos padres se escoje de entre
        la porción de genoma usado.
        :param codones_por_kernel:
        :return:
        """
        punto_crossover_max1 = padres[0].codones_usados
        punto_crossover_max2 = padres[1].codones_usados

        punto1_crossover = codones_por_kernel * \
                           random.randint(1, punto_crossover_max1//codones_por_kernel)
        punto2_crossover = codones_por_kernel * \
                           random.randint(1, punto_crossover_max2//codones_por_kernel)

        h1 = np.array([])
        h2 = np.array([])

        h1 = np.append(h1, padres[0].genotipo[0:punto1_crossover])
        h1 = np.append(h1, padres[1].genotipo[punto2_crossover:])

        h2 = np.append(h2, padres[1].genotipo[0:punto2_crossover])
        h2 = np.append(h2, padres[0].genotipo[punto1_crossover:])

        hijo1 = Individuo(h1.astype(int))
        hijo2 = Individuo(h2.astype(int))

        return hijo1, hijo2

    def  crossover_uniforme(padres, codones_por_kernel=15, umbral = 0.5):
        """
        Realiza un crossover uniforme. Para cada Kernel usado en los padres
        se genera un número aleatorio en el intervalo [0,1]. Si este número
        es menor que un umbral dado (0.5 por defecto) el primer hijo hereda
        los codones correspondientes a ese kernel del primer padre. En caso
        contrario, hereda los del segundo padre. Análogamente se hace para
        el 2° hijo pero invirtiendo los genes a heredar.
        Sólo se heredan de los padres codones usados para decodificar el
        fenotipo, el resto se descarta para evitar "bloating". Del padre
        con el genotipo más largo ambos hijos heredan los kernels "extras"
        según el umbral dado (para reducir el "bloating")
        :param codones_por_kernel:
        :return:
        """

        long_padre1 = len(padres[0].get_genotipo())
        long_padre2 = len(padres[1].get_genotipo())

        # long_padre1 = padres[0].codones_usados // codones_por_kernel
        # long_padre2 = padres[1].codones_usados // codones_por_kernel
        long_vector_decision = max(long_padre1, long_padre2)
        genotipo_mas_corto = min(long_padre1, long_padre2)
        # Reordenación de los padres de acuerdo a la longitud de su genotipo usado
        if long_padre1 < long_padre2:
            padre1 = padres[0].get_genotipo()
            padre2 = padres[1].get_genotipo()
        else:
            padre1 = padres[1].get_genotipo()
            padre2 = padres[0].get_genotipo()


        vector_decision = np.random.rand(long_vector_decision)
        h1 = np.array([])
        h2 = np.array([])
        #print(vector_decision) # todo: quitar
        for i in range(long_vector_decision):
            if i < genotipo_mas_corto:
                if vector_decision[i] < umbral:
                    h1 = np.append(h1, padre1[codones_por_kernel * i
                                              :codones_por_kernel * (i+1)])
                    h2 = np.append(h2, padre2[codones_por_kernel * i
                                              :codones_por_kernel * (i+1)])
                else:
                    h1 = np.append(h1, padre2[codones_por_kernel * i
                                              :codones_por_kernel * (i+1)])
                    h2 = np.append(h2, padre1[codones_por_kernel * i
                                              :codones_por_kernel * (i+1)])
            else:
                if vector_decision[i] < umbral:
                    h1 = np.append(h1, padre2[codones_por_kernel * i
                                              :codones_por_kernel * (i + 1):])
                    h2 = np.append(h2, padre2[codones_por_kernel * i
                                              :codones_por_kernel * (i + 1):])

        hijo1 = Individuo(h1.astype(int))
        hijo2 = Individuo(h2.astype(int))

        return hijo1, hijo2



















































