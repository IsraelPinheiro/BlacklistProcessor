import os
import re
import sys
from configparser import ConfigParser
from datetime import datetime

class PhoneProcessor(object):
    def __init__(self):
        self.DDDs = [11,12,13,14,15,16,17,18,19,21,22,24,27,28,31,32,33,34,35,37,38,41,42,43,44,45,46,47,48,49,51,53,54,55,61,62,63,64,65,66,67,68,69,71,73,74,75,77,79,81,82,83,84,85,86,87,88,89,91,92,93,94,95,96,97,98,99]
        self.InputFiles = list()
        
        self.ProcessingStartTime = datetime.now()

        config = ConfigParser()
        config.read("config.ini")
        self.logProcessedPhones = config.getboolean('logs','logProcessedPhones',fallback=False) 
        self.logProcessedFiles = config.getboolean('logs','logProcessedFiles',fallback=True)
        self.removeDuplicates = config.getboolean('logs','removeDuplicates',fallback=False)

        self.initialize()
        self.banner()
        self.menu()

    def initialize(self):
        if not os.path.isdir("./Input"):
            os.makedirs("./Input")
        if not os.path.isdir("./Output"):
            os.makedirs("./Output")
        if not os.path.isdir("./Logs"):
            os.makedirs("./Logs")
        if not os.path.isfile("./Logs/ProcessedFiles.csv"):
            with open("./Logs/ProcessedFiles.csv", "a") as ProcessedFiles:
                ProcessedFiles.write("Processing Start,File,Elapsed Time")
        if not os.path.isfile("./Logs/ProcessedPhones.csv"):
            with open("./Logs/ProcessedPhones.csv", "a") as ProcessedPhones:
                ProcessedPhones.write("Phone,Processed At,OriginFile")

        self.InputFiles = self.listInputFiles()

        if len(self.InputFiles)<1:
            sys.exit("Nenhum arquivo de input localizado, o sistema será finalizado")
        
    def listInputFiles(self):
        files = os.listdir("./Input")
        return files

    def cleanString(self, StringToClean):
        StringToClean = re.sub('\D', '', StringToClean)
        if StringToClean[0] == "0":
            StringToClean = StringToClean[1:]
        return StringToClean

    def validatePhone(self, PhoneToValidate):
        if len(PhoneToValidate)<10 or len(PhoneToValidate)>11:
            return False

        if int(PhoneToValidate[:2]) not in self.DDDs:
            return False
        
        if self.removeDuplicates:
            return False

        return True

    def logPhone(self, InputFile, PhoneToOutput):
        with open("./Logs/ProcessedPhones.csv", "a") as ProcessedFiles:
            ProcessedFiles.write(f"\n{PhoneToOutput},{datetime.now()},{InputFile}")

    def logFileProcessing(self, InputFile):
        with open("./Logs/ProcessedFiles.csv", "a") as ProcessedFiles:
            ProcessedFiles.write(f"\n{InputFile},{self.ProcessingStartTime},{(datetime.now()-self.ProcessingStartTime).total_seconds()}")
    
    def outputPhone(self, InputFile, PhoneToOutput):
        if self.logProcessedPhones:
            self.logPhone(InputFile, PhoneToOutput)
        with open(f"./Output/{InputFile}_DDD{PhoneToOutput[:2]}.txt", "a") as ProcessedFiles:
            ProcessedFiles.write(f"{PhoneToOutput}\n")
    
    def processAllFiles(self):
        for f in self.InputFiles:
            self.processFile(f)

    def processFile(self, FileToProcess):
        processed = 0
        valid = 0
        unique = 0

        self.ProcessingStartTime = datetime.now()
        print(f"Iniciando processamento do arquivo {FileToProcess}")
        with open(f"./Input/{FileToProcess}") as f:
            for line in f:
                processed+=1
                line = self.cleanString(line)
                if self.validatePhone(line):
                    valid+=1
                    self.outputPhone(FileToProcess, line)
            if self.logProcessedFiles:
                self.logFileProcessing(FileToProcess)
        print("\033[92m")
        print(f"Arquivo {FileToProcess} processado com sucesso!")
        print(f"{processed} Números processados")
        print(f"{valid} Números válidos")
        if self.removeDuplicates:
            print(f"{unique} Números únicos")
        print("\033[0m")

    def banner(self):
        print("\033[93m")
        print(r"=================================================================================================")
        print(r"||                                                                                             ||")
        print(r"||  __________.__                           _________      .__  .__  __    __                  ||")
        print(r"||  \______   \  |__   ____   ____   ____  /   _____/_____ |  | |__|/  |__/  |_  ___________   ||")
        print(r"||   |     ___/  |  \ /  _ \ /    \_/ __ \ \_____  \\____ \|  | |  \   __\   __\/ __ \_  __ \  ||")
        print(r"||   |    |   |   Y  (  <_> )   |  \  ___/ /        \  |_> >  |_|  ||  |  |  | \  ___/|  | \/  ||")
        print(r"||   |____|   |___|  /\____/|___|  /\___  >_______  /   __/|____/__||__|  |__|  \___  >__|     ||")
        print(r"||                 \/            \/     \/        \/|__|                            \/         ||")
        print(r"||                                                                                             ||")
        print(r"||                                          v0.8 Beta                                          ||")
        print(r"||                              ©Copyright 2020 Israel R Pinheiro                              ||")
        print(r"||                                                                                             ||")
        print(r"=================================================================================================")
        print("\033[0m")

    def menu(self):
        print("1 - Listar Arquivos disponíveis para processamento")
        print("2 - Processar Arquivo")
        print("3 - Processar todos os arquivos disponíveis")
        print("4 - Atualizar lista de arquivos")
        print("5 - Sobre")
        print("6 - Sair")
        x = input("Escolha uma das opções:")

        if x=="1":
            print("\n")
            for f in self.InputFiles:
                print(f"+ {f}")
            print("\n")
            self.menu()
        elif x=="2":
            c=0
            print("\n")
            for f in self.InputFiles:
                c +=1
                print(f"{c} - {f}")
            print(f"{c+1} - Cancelar")
            print("\n")
            x = input("Escolha uma das opções:")

            if int(x)>0 and int(x)<len(self.InputFiles)+1:
                if int(x) == len(self.InputFiles)+1:
                    self.menu()
                else:
                    self.processFile(self.InputFiles[int(x)-1])
                    self.menu()
            else:
                print("Opção inválida")
                self.menu()

        elif x=="3":
            self.processAllFiles()
            print("Todos os arquivos foram processados\n")
            self.menu()
        elif x=="4":
            self.InputFiles = self.listInputFiles()
            print("Listagem de arquivos atualizada\n")
            self.menu()
        elif x=="5":
            print("\nSobre!")
            self.menu()
        elif x=="6":
            print("\nSaindo...")
            exit()
        else:
            print("Opção Inválida\n")
            self.menu()

if __name__ == "__main__":
    PP = PhoneProcessor()
