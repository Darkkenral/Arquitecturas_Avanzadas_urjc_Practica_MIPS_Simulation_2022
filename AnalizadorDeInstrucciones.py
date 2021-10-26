import Instruccion
import re


class AnalizadorDeInstrucciones():
    def __init__(self):
        self.setTipoInstruccion = {
            'r': ['add', 'sub', 'and', 'or', 'nor', 'slt','mul'],
            'i': ['addi', 'subi', 'ori',  'beq', 'bne', 'lw', 'sw', 'li'],
            'j': ['j']
        }

    def analizador(self, ruta):
        '''
        Lee y analiza linea por linea el fichero dado

        Parametros
        ----------
        ruta : [str]
            Ruta al fichero a analizar

        Devuelve
        -------
        [List]
            Lista de instrucciones ya analizadas y clasificadas
        '''
        with open(ruta) as r:
            dato = filter((lambda x: x != '\n'), r.readlines())
            instrucciones = [self.clasificar(elemento) for elemento in dato]
            return instrucciones

    def clasificar(self, s: str):
        '''
        Trozea el string y clasifica la instruccion. Creando su objeto correspondiente

        Parametros
        ----------
        s : str
            Linea de la instruccion

        Errores
        ------
        ValueError
            Falla cuando no consigue encontrar ningun op que haga match con la instruccion
        '''
        # En caso de que el formato de instrucciones sea otro que en el ejemplo y contenga comas
        s.replace(',', ' ')
        s = s.split()

        if not (s == []):
            op = s[0]
            if op in self.setTipoInstruccion['r']:
                return self.instruccion_R(s)
            elif op in self.setTipoInstruccion['i']:
                return self.instruccion_I(s)
            elif op in self.setTipoInstruccion['j']:
                return self.instruccion_J(s)
            if len(s)== 1:
                return self.instruccion_Etiqueta(s)

    def instruccion_R(self, linea):
        '''
        Crea una objeto que contiene una instruccion de tipo r apartir del string dado.

        Parametros
        ----------
        linea : [str]
            Cadena que contiene la instruccion que sera encapsulada

        Returns
        -------
        [TipoR]
            Objeto que encapsula una instruccion de tipo r
        '''

        return Instruccion.TipoR(op=linea[0], signals={"regRead": 1, "regWrite": 1, "aluop": 1}, reg_nombre_s=linea[2], reg_nombre_t=linea[3], reg_nombre_dest=linea[1])

    def instruccion_I(self, linea):
        '''
        Crea una objeto que contiene una instruccion de tipo i apartir del string dado.

        Parametros
        ----------
        linea : [str]
            Cadena que contiene la instruccion que sera encapsulada

        Returns
        -------
        [TipoR]
            Objeto que encapsula una instruccion de tipo i
        '''

        if (linea[0] == 'bne' or linea[0] == 'beq'):
            return Instruccion.TipoI(op=linea[0], signals={"regRead": 1, "aluop": 1}, reg_nombre_s=linea[1], reg_nombre_t=linea[2], inmediato=linea[3])

        if (linea[0] == "lw" or linea[0] == "sw"):

            '''
            Explicacion del regrex
            1er Grupo de captura (\d+)
                \d Busca un digito ( entre el [0-9])
                + busca el token anterior un numero ilimitado de veces posible, las que sean posibles
            2do Grupo de captura \((\$r\d+)\)
                \( Busca el caracter (
                \$ Busca el caracter $
                r Busca el caracter r \d Busca un digito ( entre el [0-9])
                + busca el token anterior un numero ilimitado de veces posible, las que sean posibles
                \) Busca el caracter )
            '''
            match = re.compile('(\d+)\((\$[a-z]\d+)\)').search(linea[2])

            valorInmediato = match.group(1)
            valorRegistro = match.group(2)
            if linea[0] == "lw":
                return Instruccion.TipoI(op=linea[0], signals={"regRead": 1, "regWrite": 1, "aluop": 1, "readMem": 1}, reg_nombre_s=linea[1], reg_nombre_t=valorRegistro, inmediato=valorInmediato)
            else:
                return Instruccion.TipoI(op=linea[0], signals={"regRead": 1, "aluop": 1, "writeMem": 1}, reg_nombre_s=linea[1], reg_nombre_t=valorRegistro, inmediato=valorInmediato)
        if (linea[0] == "li"):

            return Instruccion.TipoI(op=linea[0], signals={"regWrite": 1, "aluop": 1}, reg_nombre_s=linea[1], reg_nombre_t=None, inmediato=linea[2])
        return Instruccion.TipoI(op=linea[0], signals={"regRead": 1, "regWrite": 1, "aluop": 1}, reg_nombre_s=linea[1], reg_nombre_t=linea[2], inmediato=linea[3])

    def instruccion_J(self, linea):
        '''
        Crea una objeto que contiene una instruccion de tipo j apartir del string dado.

        Parametros 
        ----------
        linea : [str]
            Cadena que contiene la instruccion que sera encapsulada

        Returns
        -------
        [TipoR]
            Objeto que encapsula una instruccion de tipo j
        '''

        return Instruccion.TipoJ(op=linea[0], target=linea[1])

    def instruccion_Etiqueta(self, linea):
        return Instruccion.Etiqueta(nombre_etiqueta=linea[0])
