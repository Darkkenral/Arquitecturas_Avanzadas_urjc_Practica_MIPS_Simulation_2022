
import sys
from AnalizadorDeInstrucciones import *
from MipsSimulator import *

analizador = AnalizadorDeInstrucciones()
#PARSEAMOS EL ARCHIVO DE INSTRUCCIONES  Y SE LA DAMOS A LA SIMULACION
MipsSimulator = Segmentacionsimulacion(analizador.analizador(sys.argv[1]))
# ASIGNAMOS LA SALIDA ESTANDAR AL FICHERO DEBUG
filename = sys.argv[2] if len(sys.argv) > 2 else "debug.txt"
f = open(filename, 'w')
sys.stdout = f
#EJECUTAMOS LA SIMULACION 
MipsSimulator.run()
