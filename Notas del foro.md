## Notas del foro

### Problema en convergencia

1. Papers:

   1. Los autores del paper han evaluado dos mecanismos de selección:  generacional y steady state. En el paper que te pongo a continuación  muestran la superioridad significativa de la aproximación steady state  ya que la generacional produce muchos individuos no válidos. Yo también  he tenido mejores resultados con ésta aproximación.

      Grammatical Evolution: A Steady State approach.

      http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.56.9196&rep=rep1&type=pdf

   2. El tema del crossover es muy importante y existen un montón de  técnicas para hacer crossovers en árboles. Nuevamente los autores del  paper han analizado varias técnicas y parece que el crossover de 1 punto  es de los más eficientes. En este caso el paper no está en abierto (si  lo quieres te lo paso).

      Crossover in Grammatical Evolution

      https://link.springer.com/article/10.1023/A:1021877127167

   3. Un detalle importante en el crossover de 1 punto es que si posterior  al cruce no tienes en cuenta el último codon que define el kernel, puede  ocurrir que en el cruce uno de los hijos sea igual que el padre ya que  si es un codon de kernel par hace que todo lo que has añadido a  continuación del kernel no se exprese. Yo al principio lo tenía así y  cuando lo modifiqué para tener en cuenta esta situación la diversidad y  la convergencia mejoró notablemente. Por otro lado el crossover tiene  que ser efectivo, es decir tiene que hacerse en una región del cromosoma  que se exprese (si se elige un punto en la zona no expresada, el  crossover no hace nada). Esto último lo cuentan en este capítulo:

      Introduction to 20 Years of Grammatical Evolution

      https://link.springer.com/chapter/10.1007%2F978-3-319-78717-6_1

2. cuidar es que el valor de probabilidad de mutación usado cuando se 
   trabaja a nivel de bits (representación binaria) no es directamente 
   comparable con el que debe usarse cuando se trabaja a nivel de enteros.

3. En principio, la selección por torneo debería ser suficiente y dar buenos resultados.

4. Con el parámetro que establece el valor máximo de longitud de cromosoma 
   debería ser suficiente para evitar el "efecto bloat", es decir, no 
   debería ser necesario aplicar un "pruning" explícito.

5. El valor de la probabilidad de mutación y de cruce puede resultar crítico

6. En relación a usar modelo generacional o de estado estacionario, puede 
   depender del tipo de problema a resolver. No necesariamente tiene que 
   ser uno de ellos universalmente válido. Eso sí, si se utiliza el modelo 
   generacional, es deseable acompañarlo de elitismo.

7. [Enrique] Lo que comentas de que la elección del punto de cruce puede determinar 
   la aparición o no de hijos idénticos a los padres (desde el punto de 
   vista sólo de la región expresable) es cierto. En cualquier caso, se 
   asume que la elección del punto de cruce es múltiplo del tamaño de 
   bloque. En este sentido, se podría asignar una cuenta en cada cromosoma 
   del número de bloques expresables que contiene y forzar a que el punto 
   de cruce esté dentro de este margen. También se puede mitigar el efecto 
   que comentas aumentando el valor de la probabilidad de cruce. Así, si la la longitud máxima elegida es grande y el número de kernels 
   necesarios (expresado en número de codones totales) para resolver un 
   problema determinado es mucho menor, el efecto que comentas es más 
   probable que aparezca (tal vez se debería entonces reducir la longitud 
   máxima).

8. [Enrique]  Con respecto a la mutación, conviene chequear que la mutación ha sido 
   efectiva también. En este caso también es importante que al mutar, 
   chequees que la expresión ha cambiado ya que debido al operador modulo 
   podemos mutar un codon y que la expresión sea la misma. Yo al principio 
   lo implementé y se me quedaba colgado porque los codones del grado en 
   los kernel no polinómicos no producen cambios. Lo tengo pendiente de 
   cambiar y de momento sin este chequeo funciona bien, pero sería más 
   efectivo chequearlo 

   > cierto, pero eso se puede mitigar aumentando el valor de la probabilidad de mutación.

   

8.  La generación de la población inicial. Si la haces random, como lo  estas haciendo, tienes 50% de modelos con un kernel, 25% con dos  kernels, 12.5% con tres kernels, y bajando... Esto sesga enormemente la  población inicial. En este paper lo cuentan:

   GE, explosive grammars and the lasting legacy of bad initialisation

   https://ieeexplore.ieee.org/document/5586336/

   Un método que genera una distribución más o menos uniforme es el *ramped*-*half-and-half.* Yo  he usado este método reusando el código de los autores, pero sería  facil generarlo a mano controlando los codones de generación de kernel  para que sean impares hasta cierta longitud (conforme a la gramática  propuesta los pares no expresan más codones, y los impares permiten  expresar más kernels). Pruebalo y nos cuentas.

9. De Enrique:

   1. (1) No es estrictamente necesario trabajar a nivel de bits, es decir,  podrías trabajar directamente a nivel de codones (enteros de 8 bits).  La única diferencia es la aplicación del operador de mutación (mutar  bits o mutar enteros) y la probabilidad de mutación asignada (no es lo  mismo la frecuencia de mutación si se trabaja a nivel de bits que si se  trabaja a nivel de enteros).

      (2) Mi recomendación es que apliques torneo para la **selección de padres**.

      (3) Yo empezaría probando el cruce por 1 punto.

      (4) El número de individuos lo veo excesivo. Yo utilizaría  poblaciones de tamaño del orden de 10^3 (1000, 2000, 3000...). Todo  depende de la capacidad de cómputo que tengas en tu sistema.  Evidentemente, a mayor tamaño de población, mayor coste computacional  tendrá cada simulación.

      (5) El ajuste de la probabilidad de cruce y de mutación puede ser  importante. Por tanto, yo analizaría cómo depende el algoritmo de estos  valores.

      > **probabilidad de cruce** me refiero a que, dados dos padres, se extrae un 
      > número al azar comprendido entre 1 y 0; si dicho valor es menor o igual 
      > que la probabilidad de cruce, entonces se cruzan y se obtienen los hijos
      > correspondientes. En otro caso, los dos hijos se obtienen como 
      > clonación de los dos padres. De forma similar, la probabilidad de 
      > mutación marca cuándo mutar o no cada uno de los hijos obtenidos.

      (6) El valorar si el número de kernels obtenido en los fenotipos son  suficientes o no dependerá de si aproximan bien o no la función  estudiada.

      (7) A mayor cantidad de wrapping, más complejo será la búsqueda. Dado  que un mismo codón podría desempeñar tantas funciones como indique el  número de wrapping máximo. En principio, yo lo pondría como máximo a 2.

      > * Respecto al método de inicialización, utilizando como motor de búsqueda un AG, se podría perfectamente usar cualquier método de inicialización aleatorio utilizado con AGs, con la única particularidad aquí de que los cromosomas a generar no están 
      >   limitados a un tamaño fijo. Por otro lado, el método **"ramped** 
      >   **half-and-half"** es utilizado normalmente en PG, pero no quita que pueda 
      >   ser adaptado para poder usarse también con el AG que sirve de motor de 
      >   búsqueda de GE. Sin embargo, **no hay garantiza** que dicho método tenga que
      >   **ser el mejor método de inicialización** en el contexto de GE, como sí 
      >   ocurre normalmente en el contexto de PG. 
      >
      > * por mi experiencia con GE, yo no inicializaría cromosomas al valor de 
      >   longitud máxima. Como mucho, a la mitad de la longitud máxima. Ya se 
      >   encargará el algoritmo de ir aumentando el tamaño si es necesario. Este 
      >   es mi consejo, salvo que hayas leído en la literatura alguna ventaja 
      >   para hacerlo tal y como lo haces.
      >
      >   > ​	*he observado el decaimiento progresivo de la longitud  media de los cromosomas de la población durante algunas ejecuciones,*
      >
      > > Mio*: Aparte de ramped half-and-half podría limitar los exponentes a valores bajos para evitar que los individuos generados inicialx. se me vayan al quinto conio! -->  
      > >
      > > Dibujar las funciones a representar y ver que valores de exponentes son razonables!!

- [ ] Implementa probabilidad de cruze
- [ ] Implemente ramped half-and-half
- [ ] Ajusta probabilidad de mutación de bit a entero (entero debería ser x8 p.e. si 8-bits por codón)
- [ ] Lee de nuevo las notas