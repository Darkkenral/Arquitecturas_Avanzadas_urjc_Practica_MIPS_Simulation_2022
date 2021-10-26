

class Instruccion():

    def __init__(self, op, signals):
        self.op = op
        self.signal_contr = {'aluop': None,
                             'regRead': None,
                             'regWrite': None,
                             'readMem': None,
                             'writeMem': None}
        if not signals == {}:
            for signal in signals.keys():
                self.signal_contr[signal] = signals[signal]

    def aluop(self):

        return self.controls['aluop']

    def regRead(self):

        return self.controls['regRead']

    def regWrite(self):

        return self.controls['regWrite']

    def readMem(self):

        return self.controls['readMem']

    def writeMem(self):

        return self.controls['writeMem']


class TipoR(Instruccion):

    def __init__(self, op, signals, reg_nombre_s, reg_nombre_t, reg_nombre_dest):
        super().__init__(op, signals)
        self.reg_value_s = None
        self.reg_value_t = None
        self.value = None
        self.reg_nombre_s = reg_nombre_s
        self.reg_nombre_t = reg_nombre_t
        self.reg_nombre_dest = reg_nombre_dest

    def __str__(self):
        '''
        Funcion que genera un string apartir del los campos del objeto

        Devuelve
        -------
        str
        '''
        s = str(self.op) + " " + str(self.reg_nombre_dest) + " " + \
            str(self.reg_nombre_s) + " " + str(self.reg_nombre_t)
        return s


class TipoI(Instruccion):

    def __init__(self, op, signals, reg_nombre_s, reg_nombre_t, inmediato):
        super().__init__(op, signals)
        self.reg_value_s = None
        self.reg_value_t = None
        self.reg_nombre_s = reg_nombre_s
        self.reg_nombre_t = reg_nombre_t
        self.inmediato = inmediato

    def __str__(self):
        '''
        Funcion que genera un string apartir del los campos del objeto

        Devuelve
        -------
        str
        '''
        s = str(self.op) + " " + str(self.reg_nombre_s) + " " + \
            str(self.reg_nombre_t) + " " + str(self.inmediato)
        return s


class TipoJ(Instruccion):

    def __init__(self, op, target):
        super().__init__(op, {})
        self.target = target

    def __str__(self):
        '''
        Funcion que genera un string apartir del los campos del objeto

        Devuelve
        -------
        str
        '''
        s = str(self.op) + " " + str(self.target) 

        return s


class Etiqueta(Instruccion):

    def __init__(self, nombre_etiqueta):
        super().__init__("Etiqueta", {})
        self.nombre_etiqueta = nombre_etiqueta[:-1]

    def __str__(self):
        '''
        Funcion que genera un string apartir del los campos del objeto

        Devuelve
        -------
        str
        '''
        s = str(self.op) + " " + str(self.nombre_etiqueta) 
        return s


class Instruccion_vacia(Instruccion):
    def __init__(self):
        super().__init__("Vacia", {})

    def __str__(self):
        '''
        Funcion que genera un string apartir del los campos del objeto

        Devuelve
        -------
        str
        '''
        s = str(self.op)

        return s
