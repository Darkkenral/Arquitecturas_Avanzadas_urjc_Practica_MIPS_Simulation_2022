def main(ruta:str):
    with open(ruta, 'r') as fichero:
        for linea in fichero:
            parseInstruction();
