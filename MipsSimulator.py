from Instruccion import *
import collections


class Segmentacionsimulacion(object):
    operaciones = {'add': '+', 'addi': '+', 'sub': '-', 'subi': '-',
                   'and': '&', 'andi': '&', 'or': '|', 'ori': '|', 'mul': '*'}

    def __init__(self, listaInstrucciones):
        self.contador_instrucciones = 0
        self.ciclos = 0
        self.listaPeligros = []
        self.__terminado = False
        self.ramificado = False
        self.aparcado = False
        self.registros = {}

        self.segmentacion = [None for x in range(0, 5)]

        self.segmentacion[0] = FetchStage(Instruccion_vacia(), self)
        self.segmentacion[1] = WriteStage(Instruccion_vacia(), self)
        self.segmentacion[2] = ReadStage(Instruccion_vacia(), self)
        self.segmentacion[3] = ExecStage(Instruccion_vacia(), self)
        self.segmentacion[4] = DataStage(Instruccion_vacia(), self)

        # Generacion de la memoria de los registros
        self.registros['$zero'] = 0
        self.registros['$at'] = 0
        self.registros['$gp'] = 0
        self.registros['$sp'] = 0
        self.registros['$fp'] = 0
        self.registros['$ra'] = 0
        for x in range(0, 2):
            self.registros['$v' + str(x)] = 0
        for x in range(0, 4):
            self.registros['$a' + str(x)] = 0
        for x in range(0, 10):
            self.registros['$t' + str(x)] = 0
        for x in range(0, 2):
            self.registros['$k' + str(x)] = 0

        # memoria principal
        self.memoria_principal = dict([(x*4, 0) for x in range(4, 0xffc)])

        # contador_de_programa
        self.contador_de_programa = 0x1000
        self.listaInstrucciones = listaInstrucciones
        # busco cuales seran las posiciones de las etiquetas en memoria y las guardo
        y = 0
        etiquetas = {}
        for instr in self.listaInstrucciones:
            if type(instr) == Etiqueta:
                etiquetas[instr.nombre_etiqueta] = 0x1000 + y
            y += 4
        y = 0

        # si hay un salto busco su posicion en la lista de etiquetas
        for instr in self.listaInstrucciones:

            if type(instr) == TipoJ:
                instr.target = etiquetas[instr.target]

            if type(instr) == TipoI:
                if (instr.op == 'bne' or instr.op == 'beq' or instr.op == 'blt' or instr.op == 'bgt'):
                    instr.inmediato = etiquetas[instr.inmediato]
            self.memoria_principal[0x1000 + y] = instr
            y += 4

    def step(self):
        self.ciclos += 1
        # Pone las instrucciones en su siguiente estado
        # Dado que el segmentacion inicia vacio el primer ciclo inicia vacio
        # FetchStage selecciona la instruccion, por eso no recibe ninguna

        self.segmentacion[1] = WriteStage(self.segmentacion[4].instr, self)
        if self.aparcado:
            self.segmentacion[4] = DataStage(Instruccion_vacia(), self)
            self.aparcado = False
        else:
            self.segmentacion[4] = DataStage(self.segmentacion[3].instr, self)
            self.segmentacion[3] = ExecStage(self.segmentacion[2].instr, self)
            self.segmentacion[2] = ReadStage(self.segmentacion[0].instr, self)
            self.segmentacion[0] = FetchStage(Instruccion_vacia(), self)

        # Avanzamos en la segmentacion en cada uno de los pasos.
        for pi in self.segmentacion:
            pi.advance()
        # Una vez se ha completado el ciclo eliinamos el registro conflictivo de
        # la lista de peligros

        if hasattr(self.segmentacion[1].instr, 'regWrite'):
            if not(self.listaPeligros == []):
                self.listaPeligros.pop(0)

        self.checkTerminado()

        # si hemos aparcado la instruccion o es un salto no queremos cargar una nueva instruccion al ciclo
        if self.aparcado or self.ramificado:
            self.contador_de_programa -= 4
            self.ramificado = False

    def checkTerminado(self):
        """ Comprueba si queda alguna instruccion por ejecutarse """
        self.__terminado = True
        for pi in self.segmentacion:
            if pi.instr.__class__.__name__ != Instruccion_vacia.__name__:
                self.__terminado = False
        if   self.__terminado:
            print("######################## Terminado ###########################")

    def run(self):
        """Ejecuta la simulacion, hasta que la señal done se activa"""
        self.printColeccionInstrucciones()
        while not self.__terminado:
            self.step()
            self.debug()

    def getForwardVal(self, regnombre):
        """ Realiza el forwarding basandose en el nombre del registro
            Si el valor no esta listo, devuelve el token "NULL"
        """
        print("<Realizando Forwarding> : ",regnombre)
        if (self.segmentacion[4].instr is not Instruccion_vacia
                and self.segmentacion[4].instr.value is not None
                and self.segmentacion[4].instr.reg_nombre_dest == regnombre):
            return self.segmentacion[4].instr.value
        elif (self.segmentacion[1] is not Instruccion_vacia
                and self.segmentacion[1].instr.reg_nombre_dest == regnombre):
            return self.segmentacion[1].instr.value
        else:
            return "NULL"

    ### ESTADO DE LA SIMULACION ###
    def debug(self):
        print("######################## debug ###########################")

        self.printRegistros()
        print("\n<contador_de_programa>", self.contador_de_programa)
        self.printsegmentacion()
        print("<Hazard List> : ", self.listaPeligros)

    def printsegmentacion(self):
        print("\n<segmentacion>")
        print(str(self.segmentacion[0]))
        print(str(self.segmentacion[2]))
        print(str(self.segmentacion[3]))
        print(str(self.segmentacion[4]))
        print(str(self.segmentacion[1]))

    def printRegistros(self):
        # """
        print("\n<Register File>")
        s = []
        for k, v in self.registros.items():
            s = s+["\t", str(k), " : ", str(v)]
        aux = ''.join(s)
        print(aux)

    def printColeccionInstrucciones(self):
        print("<Coleccion de instrucciones>")
        for index, item in (self.memoria_principal.items()):
            if item != 0:
                print(index, ": ", str(item))


# objeto generico del estado


class segmentacionStage():
    def __init__(self, instruccion, simulacion):
        self.instr = instruccion
        self.simulacion = simulacion

    def advance(self):
        pass

    def __str__(self):
        return str(self.simulacion) + ':\t' + str(self.instr)

# objeto fetch estado


class FetchStage(segmentacionStage):

    def __init__(self, instruccion, simulacion):
        super().__init__(instruccion, simulacion)

    def advance(self):
        """
        Escoje la siguiente instruccion basandose en el contador_de_programa
        """
        if self.simulacion.contador_de_programa < (len(self.simulacion.listaInstrucciones) * 4 + 0x1000):
            self.simulacion.contador_instrucciones += 1
            self.instr = self.simulacion.memoria_principal[self.simulacion.contador_de_programa]
        else:
            self.instr is Instruccion_vacia
        self.simulacion.contador_de_programa += 4

    def __str__(self):
        return 'FetchStage \t' + ':\t' + str(self.instr)


class ReadStage(segmentacionStage):

    def __init__(self, instruccion, simulacion):
        super().__init__(instruccion, simulacion)

    def advance(self):
        """
        Lee el dato de los registros utilizados en la instruccion
        """
        if self.instr.__class__.__name__ != Instruccion_vacia.__name__:
            if self.instr.__class__.__name__ != Etiqueta.__name__:
                if self.instr.op == 'j':
                    self.simulacion.contador_de_programa = self.instr.target
                    # Pone el resto de instrucciones del pipeline a instruccion vacia en caso de salto
                    print("-------BURBUJA DE SALTO INCONDICIONAL-------")
                    self.simulacion.segmentacion[0] = FetchStage(
                        Instruccion_vacia(), self)

                elif (self.instr.regRead):
                    self.instr.reg_value_s = self.simulacion.registros[self.instr.reg_nombre_s]
                    if (hasattr(self.instr, 'inmediato')):
                        # son de tipo I
                        if self.instr.op == 'beq' or self.instr.op == 'bne' or self.instr.op == 'blt' or self.instr.op == 'bgt':
                            self.instr.reg_value_s = self.simulacion.registros[self.instr.reg_nombre_s]
                            self.instr.reg_value_t = self.simulacion.registros[self.instr.reg_nombre_t]
                        if self.instr.op == 'lw' or self.instr.op == 'sw':
                            self.instr.reg_value_t = self.simulacion.registros[self.instr.reg_nombre_t]
                            self.instr.reg_value_s = self.simulacion.registros[self.instr.reg_nombre_s]
                        if self.instr.op == 'addi' or self.instr.op == 'subi' or self.instr.op == 'ori':
                            self.instr.reg_value_t = self.simulacion.registros[self.instr.reg_nombre_t]
                    elif hasattr(self.instr, 'reg_nombre_t'):
                        self.instr.reg_value_t = self.simulacion.registros[self.instr.reg_nombre_t]

    def __str__(self):
        return 'ReadStage ' + ':\t' + str(self.instr)


class ExecStage(segmentacionStage):

    def __init__(self, instruccion, simulacion):
        super().__init__(instruccion, simulacion)

    def advance(self):
        """
        Ejecuta la operacion en funcion de su campo op, se utilizan las coleccion de operaciones 
        """

        if self.instr.__class__.__name__ != Instruccion_vacia.__name__:
            if self.instr.__class__.__name__ != Etiqueta.__name__:
                  if self.instr.__class__.__name__ != TipoJ.__name__:
                    if self.instr.aluop:
                        # Si tenemos un posible peligro en el registro s o en el t
                        # cogemos el valor foward
                       
                        if self.instr.reg_nombre_s in self.simulacion.listaPeligros:
                            print("<Hay un posible peligro> : ")
                            forwardVal = self.simulacion.getForwardVal(
                                self.instr.reg_nombre_s)
                            if forwardVal != "NULL":
                                self.instr.reg_value_s = forwardVal
                            else:
                                self.simulacion.aparcado = True
                                return
                        if self.instr.reg_nombre_t in self.simulacion.listaPeligros:
                            forwardVal = self.simulacion.getForwardVal(
                                self.instr.reg_nombre_t)
                            if forwardVal != "NULL":
                                self.instr.reg_value_t = forwardVal
                            else:
                                self.simulacion.aparcado = True
                                return

                        # Annadimos el registro de destino a la lista de peligros.
                        if hasattr(self.instr, 'regWrite'):
                            if self.instr.regWrite:
                                if self.instr.__class__.__name__ == 'TipoI':
                                    self.simulacion.listaPeligros.append(
                                        self.instr.reg_nombre_s)
                                else:
                                    self.simulacion.listaPeligros.append(
                                        self.instr.reg_nombre_dest)

                        if self.instr.op == 'lw':
                            self.instr.reg_value_s = self.simulacion.memoria_principal[
                                int(self.instr.reg_value_t)+int(self.instr.inmediato)+0x1000]
                        elif self.instr.op == 'li':
                            self.instr.value = self.instr.inmediato
                            self.simulacion.registros[self.instr.reg_nombre_s] = self.instr.inmediato
                        elif self.instr.op == 'sw':
                            self.instr.reg_value_t = self.simulacion.memoria_principal[
                                int(self.instr.reg_value_s)+int(self.instr.inmediato)+0x1000]
                        elif self.instr.op == 'bne':
                            if int(self.instr.reg_value_s) != int(self.instr.reg_value_t):
                                # Colocamos el contador de programa a la etiqueta
                                self.simulacion.contador_de_programa = self.instr.inmediato
                                # Ponemos el resto de instrucciones del segmentacion a Instruccion_vacias
                                print("-------BURBUJA DE SALTO CONDICIONAL-------")
                                self.simulacion.segmentacion[0] = FetchStage(
                                    Instruccion_vacia(), self)
                                self.simulacion.segmentacion[2] = ReadStage(
                                    Instruccion_vacia(), self)
                                # activamos la señal de salto
                                self.simulacion.branched = True
                        elif self.instr.op == 'blt':
                            if int(self.instr.reg_value_s) < int(self.instr.reg_value_t):
                                # Colocamos el contador de programa a la etiqueta
                                self.simulacion.contador_de_programa = self.instr.inmediato
                                # Ponemos el resto de instrucciones del segmentacion a Instruccion_vacias
                                print("-------BURBUJA DE SALTO CONDICIONAL-------")
                                self.simulacion.segmentacion[0] = FetchStage(
                                    Instruccion_vacia(), self)
                                self.simulacion.segmentacion[2] = ReadStage(
                                    Instruccion_vacia(), self)
                                # activamos la señal de salto
                                self.simulacion.branched = True
                        elif self.instr.op == 'bgt':
                            if int(self.instr.reg_value_s) > int(self.instr.reg_value_t):
                                # Colocamos el contador de programa a la etiqueta
                                self.simulacion.contador_de_programa = self.instr.inmediato
                                # Ponemos el resto de instrucciones del segmentacion a Instruccion_vacias
                                print("-------BURBUJA DE SALTO CONDICIONAL-------")
                                self.simulacion.segmentacion[0] = FetchStage(
                                    Instruccion_vacia(), self)
                                self.simulacion.segmentacion[2] = ReadStage(
                                    Instruccion_vacia(), self)
                                # activamos la señal de salto
                                self.simulacion.branched = True
                        elif self.instr.op == 'beq':
                            if int(self.instr.reg_value_s) == int(self.instr.reg_value_t):
                                # Colocamos el contador de programa a la etiqueta
                                self.simulacion.contador_de_programa = self.instr.inmediato
                                # Ponemos el resto de instrucciones del segmentacion a Instruccion_vacias
                                print("-------BURBUJA DE SALTO CONDICIONAL-------")
                                self.simulacion.segmentacion[0] = FetchStage(
                                    Instruccion_vacia(), self)
                                self.simulacion.segmentacion[2] = ReadStage(
                                    Instruccion_vacia(), self)
                                self.simulacion.branched = True
                        else:

                            if (self.instr.op == 'slt'):
                                val = 1 if self.instr.reg_value_s < self.instr.reg_value_t else 0
                                self.instr.value = val
                                self.simulacion.registros[self.instr.reg_nombre_dest] = val
                            elif (self.instr.op == 'nor'):
                                self.instr.value = (
                                    self.instr.reg_value_s | self.instr.reg_value_t)
                                self.simulacion.registros[self.instr.reg_nombre_dest] = self.instr.value
                            elif self.instr.op == 'addi':
                                self.instr.reg_value_s = int(
                                    self.instr.reg_value_t) + int(self.instr.inmediato)
                            elif self.instr.op == 'subi':
                                self.instr.reg_value_s = int(
                                    self.instr.reg_value_t) - self.instr.inmediato
                            elif self.instr.op == 'ori':
                                self.instr.reg_value_s = int(
                                    self.instr.reg_value_t) or int(self.instr.inmediato)
                            else:

                                if self.instr is None:
                                    self.instr.value = eval("%d %s %d" %
                                                            (int(self.instr.reg_value_s),
                                                            self.simulacion.operaciones[self.instr.op],
                                                            int(self.instr.reg_value_t)))

    def __str__(self):
        return 'ExecStage ' + ':\t' + str(self.instr)


class DataStage(segmentacionStage):

    def __init__(self, instruccion, simulacion):
        super().__init__(instruccion, simulacion)

    def advance(self):
        """
        Si tenemos que leer de memoria , escribe primero
        y despues lee de memoria principal
        """

        if self.instr.__class__.__name__ != Instruccion_vacia.__name__:
            if self.instr.__class__.__name__ != Etiqueta.__name__:
                if self.instr.__class__.__name__ != TipoJ.__name__:
                    if self.instr.writeMem:
                        self.simulacion.memoria_principal[self.instr.reg_value_t] = self.instr.reg_value_s
                    elif self.instr.readMem:
                        self.instr.value = self.simulacion.memoria_principal[self.instr.reg_value_s]

    def __str__(self):
        return 'DataStage  ' + ':\t' + str(self.instr)


class WriteStage(segmentacionStage):

    def __init__(self, instruccion, simulacion):
        super().__init__(instruccion, simulacion)

    def advance(self):
        """
        Escribimos en la memoria de registros 
        """

        if self.instr.__class__.__name__ != Instruccion_vacia.__name__:
            if self.instr.__class__.__name__ != Etiqueta.__name__:
                if self.instr.__class__.__name__ != TipoJ.__name__:    
                    if self.instr.regWrite:
                        if hasattr(self.instr, 'reg_nombre_dest'):
                            self.simulacion.registros[self.instr.reg_nombre_dest] = self.instr.value
                        if hasattr(self.instr, 'reg_nombre_s'):
                            self.simulacion.registros[self.instr.reg_nombre_s] = self.instr.reg_value_s
    def __str__(self):
        return 'WriteStage ' + ':\t' + str(self.instr)
