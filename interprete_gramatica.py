import re


class Gramatica(object):

    NT = "NT"   # Conjunto de no-terminales
    T = "T"     # Conjunto de terminales

    def __init__(self, archivo_gramatica):
        self.reglas = {}
        self.no_terminales, self.terminales = set(), set()
        self.regla_inicio = None

        self.lee_archivo_gramatica(archivo_gramatica)

    def lee_archivo_gramatica(self, nombre_archivo):
        """Lee el archivo de gramática usado """
        patron_no_terminales = "(<.+?>)"    # Sirve para identificar si el archivo de gramática es
        separador_reglas = "::="            # sintácticamente correcto. Busca lo que sea que este
        separador_opciones = "|"            # entre corchetes

        # Lectura del archivo de gramática
        for line in open(nombre_archivo, 'r'):
            if not line.startswith("#") and line.strip() != "":
                # Reglas de separación. Todas las opciones de una regla hand de estar en la misma línea
                if line.find(separador_reglas):
                    regla, opciones = line.split(separador_reglas)
                    regla = regla.strip()
                    if not re.search(patron_no_terminales, regla):    # Si
                        raise ValueError("Error en el archivo de gramática:", regla)
                    self.no_terminales.add(regla)
                    if self.regla_inicio is None:       # La primera línea de la gramática debe ser <expr>
                        self.regla_inicio = (regla, self.NT)
                        # TODO: Decide si dejas la regla de inicio como None o la cambias
                    # Busca los terminales
                    opciones_tmp = []
                    for opcion in [opcion.strip()
                                   for opcion in opciones.split(separador_opciones)]:
                        opcion_tmp = []
                        if not re.search(patron_no_terminales, opcion):
                            self.terminales.add(opcion)
                            opcion_tmp.append((opcion, self.T))
                        else:
                            # Match non terminal or terminal pattern
                            # TODO does this handle quoted NT symbols?
                            for valor in re.findall("<.+?>|[^<>]*", opcion):
                                if valor != '':
                                    if not re.search(patron_no_terminales, valor):
                                        simbolo = (valor, self.T)
                                        self.terminales.add(valor)
                                    else:
                                        simbolo = (valor, self.NT)
                                    opcion_tmp.append(simbolo)
                        opciones_tmp.append(opcion_tmp)
                    # Crear regla de producción
                    if regla not in self.reglas:
                        self.reglas[regla] = opciones_tmp
                    else:
                        raise ValueError("Regla repetida:!", regla)
                else:
                    raise ValueError("Cada regla debe estar en una misma línea")

    def __str__(self):
        return "Conjunto de terminales:\n%s \n\n" \
               "Conjunto de no terminales:\n%s \n\n" \
               "Conjunto de reglas:\n%s \n\n" \
               "Regla de inicio:\n%s" % (self.terminales, self.no_terminales,
                                         self.reglas, self.regla_inicio)

    def generate(self, _input, max_wraps=2):
        """Map input via rules to salida. Returns salida and codones_usados"""
        codones_usados = 0
        wraps = 0
        salida = []
        opciones_de_produccion = []
        #print(self.reglas)

        simbolos_no_asignados = [self.regla_inicio]
        while (wraps < max_wraps) and (len(simbolos_no_asignados) > 0):
            # Wrap: La siguiente condición comprueba si se vuelven a reutilizar codones
            if codones_usados == 15:
                print("cuidao!")
 #           if codones_usados % len(_input) == 0 and codones_usados > 0 and len(opciones_de_produccion) > 1:
 #               wraps += 1
            # Asignar una producción (obtener el valor de un símbolo)
            simbolo_actual = simbolos_no_asignados.pop(0)
            # Si no es un no-terminal se fija el valor correspondiente
            #if simbolos_no_asignados[0][1] != self.NT:
             #   print(simbolos_no_asignados)
              #  while simbolos_no_asignados[0][1] != self.NT:
               #     simbolo_actual = simbolos_no_asignados.pop(0)
                #    salida.append(simbolo_actual[0])

            if simbolo_actual[1] != self.NT:
                #while  simbolo_actual[1] != self.NT:
                salida.append(simbolo_actual[0])
              #      simbolo_actual = simbolos_no_asignados.pop(0)
            # Si pertenece al conjunto no-terminal hay que escoger la opción de producción
            else:
                #simbolo_actual = simbolos_no_asignados.pop(0)
                opciones_de_produccion = self.reglas[simbolo_actual[0]]
                # Seleccionar una opción de producción
                produccion_actual = _input[codones_usados % len(_input)] % len(opciones_de_produccion)
                # Y se usa el codón si había más de una opción para escoger
                if len(opciones_de_produccion) > 1:
                    codones_usados += 1
                if codones_usados % len(_input) == 0 and codones_usados > 0 and len(opciones_de_produccion) > 1:
                    wraps += 1
                # Derviation order is left to right(depth-first)
                simbolos_no_asignados = opciones_de_produccion[produccion_actual] + simbolos_no_asignados

        # Not completly expanded
        if len(simbolos_no_asignados) > 0:
            return None, codones_usados

        salida = "".join(salida)

        """ Create correct python syntax.
        We use {: and :} as special open and close brackets, because
        it's not possible to specify indentation correctly in a BNF
        grammar without this type of scheme."""

        indent_level = 0
        tmp = salida[:]
        i = 0
        while i < len(tmp):
            tok = tmp[i:i + 2]
            if tok == "{:":
                indent_level += 1
            elif tok == ":}":
                indent_level -= 1
            tabstr = "\n" + "  " * indent_level
            if tok == "{:" or tok == ":}":
                tmp = tmp.replace(tok, tabstr, 1)
            i += 1
        # Strip superfluous blank lines.
        salida = "\n".join([line for line in tmp.split("\n")
                            if line.strip() != ""])

        return salida, codones_usados

