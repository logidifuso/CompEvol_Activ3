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
    resul = f(x)
    return resul

def calcula_fitness(individuo, U, K0, K1, x_referencia, y_referencia, m):
    y = evaluar_fenotipo(individuo, x_referencia)
    suma = 0
    for i in range(m):
        if abs(y[i]-y_referencia[i]) <= U:
            sumando = K0 * abs(y[i]-y_referencia[i])
        else:
            sumando = K1 * abs(y[i]-y_referencia[i])
        suma += sumando
    return suma

def mapeo_y_fitness(individuo):
    # 1) Mapear genotipo a fenotipo y asignarlo al individuo -> generate -> set_fenotipo
    fenotipo, codones_usados = bnf_grammar.generate(hijos[i].get_genotipo())
    _indiv.set_fenotipo(fenotipo)
    # 2) evaluar y apuntar el fitness al individuo --> calcula_fitness
    fitness_indiv = calcula_fitness(_indiv, U=0.1, K0=0.1, K1=1,
                                    x_referencia, y_referencia, m=41)
    _indiv.set_fitness(fitness_indiv)

    poblacion[i].set_fitness(seleccion_func)
    poblacion[i + 1].set_fitness(seleccion_func)
    i += 2

def seleccion_sus(poblacion):
    """
    Selección de padres usando el algoritmo estocástico universal (SUS)
    :param poblacion:
    :return:
    """
    seleccion_padres = 0
    tamano_poblacion = len(poblacion)
    # En nuestro caso lamdda = al tamanno de la población,
    # pero dejo la variable para posibles futuros experimentos
    lambda_padres = tamano_poblacion
    indice = 0
    r = np.random.uniform(0, 1/lambda_padres)
    lista_padres = []

    while seleccion_padres < lambda_padres:
        while r <= poblacion[indice].get_prob_padre_acumulada():
            lista_padres.append(poblacion[indice])
            r = r + 1/lambda_padres
            seleccion_padres += 1
        indice += 1
    return lista_padres

def seleccion_torneo(poblacion):
    # TODO: Implementar la selección por torneo. Referencia ponyge2
    aux = poblacion
    return aux

def paso_generacional(poblacion):

    elite = min(poblacion).get_fitness()
    tamano_poblacion = len(poblacion)
    # 1) Busqueda y selección
    # TODO: Implemento solo SUS de momento. Opciones: if para elegir o \
    # varias funciones paso_generacional

    # 1.a) Asignación de las probabilidades de seleccion
    poblacion.sort()
    pos = 0
    acum = 0

    for elem in poblacion:
        elem.set_prob_lin(pos, s, tamano_poblacion)
        acum += elem.get_prob_padre()
        elem.set_prob_padre_acumulada(acum)
        pos += 1

    # 1.b) Selección de padres
    lista_padres = seleccion_sus(poblacion)
    # 2) Cruzes y mutaciones
    # TODO: De momento solo con cruze de 1punto fijo!!
    shuffle(lista_padres)  # Barajamos los padres --> cruze aleatorio
    elite = max(poblacion)  # Reservo el mejor de la población por si debemos aplicar elitismo
    hijos = []  # Reseteo de la población - aplicamos relevo generacional

    i = 0
    while i < (tamano_poblacion - 1):
        padres = [lista_padres[i], lista_padres[i+1]]
        hijo1, hijo2 = Individuo.crossover_1pt_fijo(padres, codones_por_kernel=15)
        hijos.append(Individuo(hijo1))
        hijos.append(Individuo(hijo2))
        # 3) Mutaciones
        hijos[i].muta_en_kernel(prob_mutacion, codones_por_kernel=15)
        hijos[i+1].muta_en_kernel(prob_mutacion, codones_por_kernel=15)
        # 4) Mapeo y evaluación del fitness de los hijos
        mapeo_y_fitness(hijos[i])
        mapeo_y_fitness(hijos[i + 1])
        i +=2

    mejor_hijo = max(hijos)

    if elite > mejor_hijo:
        peor_hijo = min(poblacion)
        poblacion.remove(peor_hijo)
        poblacion.append(elite)

    return hijos

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



GRAMMAR_FILE = 'gramatica_nucleos.bnf'
# Read grammar
bnf_grammar = interprete_gramatica.Gramatica(GRAMMAR_FILE)
print(bnf_grammar)

# Genoma para testear las funciones en la clase Gramatica
genoma_prueba = [1, 0, 1, 2, 1, 3, 5, 6, 1, 9, 8, 9, 1, 2, 0, 3, \
                 1, 3, 3, 0, 1, 8, 8, 1, 1, 7, 7, 1, 2, 1, 4, 0, \
                 6, 6, 0, 2, 3, 3, 1, 8, 2, 2, 0, 1, 1]
fenotipo, codones_usados = bnf_grammar.generate(genoma_prueba)


#print("El número de codones usados ha sido: ", codones_usados)
print("El fenotipo que ha quedado tras decodificar es:\n", fenotipo)

exec(fenotipo, globals())
# Rango de x a evaluar (vectorización de la evaluación de los puntos)
x = np.arange(-1, 1, 0.5)
print("Puntos de evaluación:", x)
evaluacion = f(x)
print("El resultado de la evaluación ha sido:\n", evaluacion)

'''
x_referencia = [-1.  -0.5  0.   0.5]#
y_referencia 

def calcula_fitness(individuo, U, K0, K1, x_referencia, y_referencia, m):
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