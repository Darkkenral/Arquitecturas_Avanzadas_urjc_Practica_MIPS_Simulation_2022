from _typeshed import Self
from typing import Dict


class Instruccion():
    def __init__(self, op, signals):
        self.op = op
        self.signal_controls = {'aluop': None,
                                'regRead': None,
                                'regWrite': None,
                                'readMem': None,
                                'writeMem': None}
        if not signals=={}:
            for signal in signals.keys():
                signal_controls[signal] = signals[signal]

    @property
    def op(self):
        """ Devuelve el codigo de operacion"""
        return self.op

    @property
    def aluop(self):
        '''
            Obtiene la sennal de control que decide una operacion de la alu

            Devuelve
            -------
            Int
                Bit de la señal
        '''
        return self.signal_controls['aluop']

    @property
    def regRead(self):
        '''
            Obtiene la sennal de control que decide si leer o no en un registro

            Devuelve
            -------
            Int
                Bit de la señal
        '''
        return self.signal_controls['regRead']

    @property
    def regWrite(self):
        '''
            Obtiene la sennal de control que decide si escribir o no en un registro

            Devuelve
            -------
            Int
                Bit de la señal
        '''
        return self.signal_controls['regWrite']

    @property
    def readMem(self):
        '''
             Obtiene la sennal de control que decide si leer o no de la memoria principal

             Devuelve
             -------
             Int
                 Bit de la señal
         '''
        return self.signal_controls['readMem']

    @property
    def writeMem(self):
        '''
            Obtiene la sennal de control que decide si escribir o no de la memoria principal

            Devuelve
            -------
            Int
                Bit de la señal
        '''
        return self.signal_controls['writeMem']

    @property
    def __str__(self):
        s = str(self.op)+"\t"
        return s


class TipoR(Instruccion):
    

    def __init__(self, op, signals: Dict, reg_nombre_s, reg_nombre_t, reg_nombre_dest):
        super().__init__(op, signals)
        self.reg_value_s = None
        self.reg_value_t = None
        self.value = None
        self.reg_nombre_s = reg_nombre_s
        self.reg_nombre_t = reg_nombre_t
        self.reg_nombre_dest = reg_nombre_dest

    @property
    def reg_nombre_s(self):
        return self.reg_nombre_s

    @property
    def reg_nombre_t(self):
        return self.reg_nombre_t

    @property
    def reg_nombre_dest(self):
        return self.reg_nombre_dest

    @property
    def __str__(self):
        '''
        Funcion que genera un string apartir del los campos del objeto

        Devuelve
        -------
        str
        '''
        s = str(self.op) + str(self.reg_nombre_dest) + " " + \
            str(self.reg_nombre_s) + str(self.reg_nombre_t)
        return s


class TipoI(Instruccion):

    def __init__(self, op, signals: Dict, reg_nombre_s, reg_nombre_t, inmediato):
        super().__init__(op, signals)
        self.reg_value_s = None
        self.reg_value_t = None
        self.reg_nombre_s = reg_nombre_s
        self.reg_nombre_t = reg_nombre_t
        self.inmediato = inmediato

    @property
    def reg_nombre_s(self):
        return self.reg_nombre_s

    @property
    def reg_nombre_t(self):
        return self.reg_nombre_t

    @property
    def inmediato(self):
        return self.inmediato

    @property
    def __str__(self):
        '''
        Funcion que genera un string apartir del los campos del objeto

        Devuelve
        -------
        str
        '''
        s = str(self.op) + " " + str(self.reg_nombre_s) + " " + \
            str(self.reg_nombre_t) + " " + str(self.inmediato)+"\n "
        return s


class TipoJ(Instruccion):

    def __init__(self, op, signals: Dict, desplazamiento):
        super().__init__(op, signals)
        self.desplazamiento = desplazamiento

    @property
    def desplazamiento(self):
        return self.desplazamiento

    @property
    def __str__(self):
        '''
        Funcion que genera un string apartir del los campos del objeto

        Devuelve
        -------
        str
        '''
        s = str(self.op) + " " + str(self.desplazamiento) + "\n "

        return s
