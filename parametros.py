# Diccionario con los parámetros usados

params = {
    'TAMANO_POBLACION': 5000,
    'LONG_MAX_GENOTIPO': 240,
    'MAX_WRAPS': 2,
    'MAX_VAL_CODON': 256,

    'MIN_LONG_FENOTIPO_INICIAL': 1,
    'MAX_LONG_FENOTIPO_INICIAL': 8,

    'U': 0.1,
    'K0': 1,
    'K1': 10,

    'S': 1.8,

    'ARCHIVO_GRAMATICA': 'gramatica_nucleos.bnf',
    'PROBLEMA_TIPO': 'Problema1',

    'p_mutacion': 0.05,  # todo: decidir si es una constante o se usa en algo memético
    'OPCION_SELECCION': 'Torneo',
    'TAMANO_TORNEO': 2,

    'NUM_EJECUCIONES': 1,
    'MAX_GENERACIONES': 80
}
