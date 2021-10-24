from Instruccion import *
import collections


class SegmentacionSimulator(object):
    operations = {'add': '+', 'addi': '+', 'sub': '-', 'subi': '-',
                  'and': '&', 'andi': '&', 'or': '|', 'ori': '|','mul':'*'}

    def __init__(self, listaInstrucciones):
        self.contador_instrucciones = 0
        self.ciclos = 0
        self.lsitaPeligros = []
        self.__terminado = False
        self.ramificado = False
        self.aparcado = False
        self.registros={}

        self.segmentacion = [None for x in range(0, 5)]

        self.segmentacion[0] = FetchStage(Instruccion_vacia, self)
        self.segmentacion[1] = WriteStage(Instruccion_vacia, self)
        self.segmentacion[2] = ReadStage(Instruccion_vacia, self)
        self.segmentacion[3] = ExecStage(Instruccion_vacia, self)
        self.segmentacion[4] = DataStage(Instruccion_vacia, self)

        # Generacion de la memoria de los registros
        self.registros['$zero']=0
        self.registros['$at']=0
        self.registros['$gp']=0
        self.registros['$sp']=0
        self.registros['$fp']=0
        self.registros['$ra']=0
        for x in range(1):
            self.registros['$v'+ str(x)]= 0
        for x in range(3):
                self.registros['$a'+ str(x)]= 0
        for x in range(9):
                self.registros['$t'+ str(x)]= 0
        for x in range(1):
                self.registros['$k'+ str(x)]= 0

        # memoria principal
        self.mainmemory = dict([(x*4, 0) for x in range(4,0xffc)])

        # contador_de_programa to state where in the Instruccion collection
        # we are. to find correct spot in mainmemory add 0x100
        self.contador_de_programa = 0x1000

        # the list of Instruccion objects passed into the simulator,
        # most likely created by parsing text
        self.listaInstrucciones = listaInstrucciones

        # populate main memory with our text of the Instruccions
        # starting at 0x100
        y = 0
        for instr in self.listaInstrucciones:
            etiquetas={}
            # lista de etiquetas.= nombre : posicion en memoria.
            # if j o jr  campo target etiqueta
            if type(instr)==Etiqueta:
                etiquetas[instr.nombre_etiqueta]=0x1000 + y
            if type(instr)==TipoJ:
                for search in range(self.listaInstrucciones.index(instr), self.listaInstrucciones.__len__):
                    self.listaInstrucciones.inde
                etiquetas[instr.target]
            self.mainmemory[0x1000 + y] = instr
            y += 4

    def step(self):
        self.ciclos += 1
        # shift the Instruccions to the next logical place
        # technically we do the Fetch Instruccion here, which is why
        # FetchStage.advance() does nothing

        # MUST KEEP THIS ORDER
        self.segmentacion[1] = WriteStage(self.segmentacion[4].instr, self)
        if self.aparcado:
            self.segmentacion[4] = DataStage(Instruccion_vacia, self)
            self.aparcado = False
        else:
            self.segmentacion[4] = DataStage(self.segmentacion[3].instr, self)
            self.segmentacion[3] = ExecStage(self.segmentacion[2].instr, self)
            self.segmentacion[2] = ReadStage(self.segmentacion[0].instr, self)
            self.segmentacion[0] = FetchStage(None, self)

        # call advance on each Instruccion in the segmentacion
        for pi in self.segmentacion:
            pi.advance()
        # now that everything is done, remove the register from
        # the hazard list
        if (self.segmentacion[1].instr.regWrite):
            self.lsitaPeligros.pop(0)

        self.checkDone()

        # if we aparcadoed our ramificado we didn't want to load a new
        # so keep the program counter where it is
        if self.aparcado or self.ramificado:
            self.contador_de_programa -= 4
            self.ramificado = False

    def checkDone(self):
        """ Check if we are done and set __terminado variable """
        self.__terminado = True
        for pi in self.segmentacion:
            if pi.instr is not Instruccion_vacia:
                self.__terminado = False

    def run(self):
        """ Run the simulator, call step until we are done """
        while not self.__terminado:
            self.step()
            self.debug()

    def getForwardVal(self, regName):
        """ Forward the proper value based on the given register name
            If the value is not ready, return "GAH" 
        """
        if (self.segmentacion[4] is not Instruccion_vacia
                and self.segmentacion[4].instr.result is not None
                and self.segmentacion[4].instr.dest == regName):
            return self.segmentacion[4].instr.result
        elif (self.segmentacion[1] is not Instruccion_vacia
                and self.segmentacion[1].instr.dest == regName):
            return self.segmentacion[1].instr.result
        else:  # this value used to be False, but python treats False and 0 the same
            return "GAH"

    ### DEBUGGING INFORMATION PRINTING ###
    def debug(self):
        print ("######################## debug ###########################")
        self.printStageCollection()
        self.printRegFile()
        print ("\n<contador_de_programa>", self.contador_de_programa)
        self.printsegmentacion()
        print ("<CPI> : ", float(self.ciclos) / float(self.contador_instrucciones))
        print ("<Hazard List> : ", self.lsitaPeligros)

    def printsegmentacion(self):
        print ("\n<segmentacion>")
        print (repr(self.segmentacion[0]))
        print (repr(self.segmentacion[2]))
        print (repr(self.segmentacion[3]))
        print (repr(self.segmentacion[4]))
        print (repr(self.segmentacion[1]))

    def printRegFile(self):
        # """
        print ("\n<Register File>")
        for k, v in sorted(self.registros.iteritems()):
            if len(k) != 3:
                print( k, " : ", v,)
            else:
                print ("\n", k, " : ", v,)

    def printStageCollection(self):
        print ("<Instruccion Collection>")
        for index, item in sorted(self.mainmemory.iteritems()):
            if item != 0:
                print (index, ": ", str(item))


class segmentacionStage(object):
    def __init__(self, Instruccion, simulator):
        self.instr = Instruccion
        self.simulator = simulator

    def advance(self):
        pass

    def __repr__(self):
        return str(self) + ':\t' + str(self.instr)


class FetchStage(segmentacionStage):
    pass


class ReadStage(segmentacionStage):
    pass


class ExecStage(segmentacionStage):
    pass


class DataStage(segmentacionStage):
    pass


class WriteStage(segmentacionStage):
    pass
