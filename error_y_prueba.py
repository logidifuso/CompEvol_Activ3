import interprete_gramatica
from Individuo import Individuo
import numpy as np



from math import sin

"""
cdef class Function:
    cpdef double evaluate(self, double x) except *:
        return 0

cdef class SinOfSquareFunction(Function):
    cpdef double evaluate(self, double x) except *:
        return sin(x ** 2)
"""

'''
class Function(object):
    def eval(self):
        return 9

class SinOfSquareFunction(Function):
    def evaluate(self):
        return x**2


print(SinOfSquareFunction())


import getopt, sys


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unhandled option"
    # ...

if __name__ == "__main__":
    main()

'''

especimen = Individuo()
print("\n\n", especimen)


genotipo = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
especimen = Individuo(genotipo, 6)
print("\n\n", especimen)

especimen = Individuo(longitud=6)
print("\n\n", especimen)
