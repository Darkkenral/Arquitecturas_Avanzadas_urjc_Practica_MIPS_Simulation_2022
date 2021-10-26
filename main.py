
import sys
from AnalizadorDeInstrucciones import *
from MipsSimulator import *

analizador = AnalizadorDeInstrucciones()
MipsSimulator = Segmentacionsimulacion(analizador.analizador(sys.argv[1]))
    
filename = sys.argv[2] if len(sys.argv) > 2 else "debug.txt"
f = open(filename, 'w')
sys.stdout = f
MipsSimulator.run()
