from Instruccion import *
import collections


class PipelineSimulator(object):
    operations = {'add': '+', 'addi': '+', 'sub': '-', 'subi': '-',
                  'and': '&', 'andi': '&', 'or': '|', 'ori': '|'}

    def __init__(self, instrCollection):
        self.instrCount = 0
        self.cycles = 0
        self.hazardList = []
        self.__done = False
        self.branched = False
        self.stall = False

        self.pipeline = [None for x in range(0, 5)]

        self.pipeline[0] = FetchStage(Instruccion_vacia, self)
        self.pipeline[1] = WriteStage(Instruccion_vacia, self)
        self.pipeline[2] = ReadStage(Instruccion_vacia, self)
        self.pipeline[3] = ExecStage(Instruccion_vacia, self)
        self.pipeline[4] = DataStage(Instruccion_vacia, self)

        # Generacion de la memoria de los registros
        self.registers = dict([("$r%s" % x, 0) for x in range(32)])

        # memoria principal
        # and continuing to 0xffc
        self.mainmemory = dict([(x*4, 0) for x in range(0xffc/4)])

        # programCounter to state where in the Instruccion collection
        # we are. to find correct spot in mainmemory add 0x100
        self.programCounter = 0x1000

        # the list of Instruccion objects passed into the simulator,
        # most likely created by parsing text
        self.instrCollection = instrCollection

        # populate main memory with our text of the Instruccions
        # starting at 0x100
        y = 0
        for instr in self.instrCollection:
            # lista de etiquetas.= nombre : posicion en memoria.
            # if j o jr  campo target etiqueta
            self.mainmemory[0x1000 + y] = instr
            y += 4

    def step(self):
        self.cycles += 1
        # shift the Instruccions to the next logical place
        # technically we do the Fetch Instruccion here, which is why
        # FetchStage.advance() does nothing

        # MUST KEEP THIS ORDER
        self.pipeline[1] = WriteStage(self.pipeline[4].instr, self)
        if self.stall:
            self.pipeline[4] = DataStage(Instruccion_vacia, self)
            self.stall = False
        else:
            self.pipeline[4] = DataStage(self.pipeline[3].instr, self)
            self.pipeline[3] = ExecStage(self.pipeline[2].instr, self)
            self.pipeline[2] = ReadStage(self.pipeline[0].instr, self)
            self.pipeline[0] = FetchStage(None, self)

        # call advance on each Instruccion in the pipeline
        for pi in self.pipeline:
            pi.advance()
        # now that everything is done, remove the register from
        # the hazard list
        if (self.pipeline[1].instr.regWrite):
            self.hazardList.pop(0)

        self.checkDone()

        # if we stalled our branched we didn't want to load a new
        # so keep the program counter where it is
        if self.stall or self.branched:
            self.programCounter -= 4
            self.branched = False

    def checkDone(self):
        """ Check if we are done and set __done variable """
        self.__done = True
        for pi in self.pipeline:
            if pi.instr is not Instruccion_vacia:
                self.__done = False

    def run(self):
        """ Run the simulator, call step until we are done """
        while not self.__done:
            self.step()
            self.debug()

    def getForwardVal(self, regName):
        """ Forward the proper value based on the given register name
            If the value is not ready, return "GAH" 
        """
        if (self.pipeline[4] is not Instruccion_vacia
                and self.pipeline[4].instr.result is not None
                and self.pipeline[4].instr.dest == regName):
            return self.pipeline[4].instr.result
        elif (self.pipeline[1] is not Instruccion_vacia
                and self.pipeline[1].instr.dest == regName):
            return self.pipeline[1].instr.result
        else:  # this value used to be False, but python treats False and 0 the same
            return "GAH"

    ### DEBUGGING INFORMATION PRINTING ###
    def debug(self):
        print ("######################## debug ###########################")
        self.printStageCollection()
        self.printRegFile()
        print ("\n<ProgramCounter>", self.programCounter)
        self.printPipeline()
        print ("<CPI> : ", float(self.cycles) / float(self.instrCount))
        print ("<Hazard List> : ", self.hazardList)

    def printPipeline(self):
        print ("\n<Pipeline>")
        print (repr(self.pipeline[0]))
        print (repr(self.pipeline[2]))
        print (repr(self.pipeline[3]))
        print (repr(self.pipeline[4]))
        print (repr(self.pipeline[1]))

    def printRegFile(self):
        # """
        print ("\n<Register File>")
        for k, v in sorted(self.registers.iteritems()):
            if len(k) != 3:
                print( k, " : ", v,)
            else:
                print ("\n", k, " : ", v,)

    def printStageCollection(self):
        print ("<Instruccion Collection>")
        for index, item in sorted(self.mainmemory.iteritems()):
            if item != 0:
                print (index, ": ", str(item))


class PipelineStage(object):
    def __init__(self, Instruccion, simulator):
        self.instr = Instruccion
        self.simulator = simulator

    def advance(self):
        pass

    def __repr__(self):
        return str(self) + ':\t' + str(self.instr)


class FetchStage(PipelineStage):
    pass


class ReadStage(PipelineStage):
    pass


class ExecStage(PipelineStage):
    pass


class DataStage(PipelineStage):
    pass


class WriteStage(PipelineStage):
    pass
