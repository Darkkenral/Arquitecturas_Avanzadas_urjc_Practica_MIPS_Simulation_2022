



class Instruccion():
  

    def __init__(self, op, signals):
        self.op = op
        self.signal_contr = {'aluop': None,
                    'regRead': None,
                    'regWrite': None,
                    'readMem': None,
                    'writeMem': None}
        if not signals=={}:
            for signal in signals.keys():
               self.signal_contr[signal] = signals[signal]

 


class TipoR(Instruccion):
    

    def __init__(self, op, signals, reg_nombre_s, reg_nombre_t, reg_nombre_dest):
        super().__init__(op, signals)
        self.reg_value_s = None
        self.reg_value_t = None
        self.value = None
        self.reg_nombre_s = reg_nombre_s
        self.reg_nombre_t = reg_nombre_t
        self.reg_nombre_dest = reg_nombre_dest

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

    def __init__(self, op, signals, reg_nombre_s, reg_nombre_t, inmediato):
        super().__init__(op, signals)
        self.reg_value_s = None
        self.reg_value_t = None
        self.reg_nombre_s = reg_nombre_s
        self.reg_nombre_t = reg_nombre_t
        self.inmediato = inmediato


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

    def __init__(self, op ,target):
        super().__init__(op, {})
        self.target = target

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
class Etiqueta(Instruccion):
    
    def __init__(self, nombre_etiqueta):
        super().__init__("Etiqueta", {})
        self.nombre_etiqueta=nombre_etiqueta[:-1]
class Instruccion_vacia(Instruccion):
    pass
