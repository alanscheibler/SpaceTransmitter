import os
from Crypto.PublicKey import RSA

invalidCharacters = ("/",":","*","?","<",">","|","\ "," ")

def cls():
       os.system("cls")

def registerSonda():
       global sondaName 

       sondaName = input('Insira o nome da sonda:\n')
       sondaName = ''.join(char if char not in invalidCharacters else '_' for char in sondaName)
       folderPath = os.path.join(os.getcwd(), sondaName)

       sondaPrivate = os.path.join(folderPath, f'{sondaName}.private.pem')
       sondaPublic = os.path.join(folderPath, f'{sondaName}.public.pem')
       

       if os.path.exists(folderPath):
              input(f'A sonda {sondaName} já foi registrada, registre sua sonda com um novo nome. Pressione enter para continuar')
       else:
              os.mkdir(folderPath)
              key = RSA.generate(1024)
              privateGen = key.export_key()
              publicGen = key.publickey().export_key()
              
              with open(sondaPrivate, 'wb') as privateFile:
                     privateFile.write(privateGen)
                     privateKeyPem = open(sondaPrivate, 'rb').read()
                     privateKeyPem = b'\n'.join([privateKeyPem[i:i+64] for i in range (0, len(privateKeyPem),64)])

              with open(sondaPublic, 'wb') as publicFile:
                     publicFile.write(publicGen)
                     publicKeyPem = open(sondaPublic,'rb').read()
                     publicKeyPem = b'\n'.join([publicKeyPem[i:i+64] for i in range(0, len(publicKeyPem), 64)])
              
              input("Sonda registrada com sucesso! (enter)")

              sondaFile = "sonda_list.txt"
              if os.path.exists(sondaFile):
                     with open(sondaFile, 'a') as listFile:
                            listFile.write(f'- {sondaName}\n')
              else:
                     with open(sondaFile, 'w') as listFile:
                            listFile.write(f'{sondaName}\n')


def registerData():
       local = input('Insira o local do registro:\n')
       local = ''.join(char if char not in invalidCharacters else '_' for char in local)
       data = input('Insira a data do registro:\n')
       data = ''.join(char if char not in invalidCharacters else '_' for char in data)
       temperatura = input('Insira a Temperatura:\n')
       radiacaoAlfa = input('Insira a Radiacao Alfa:\n')
       radiacaoBeta = input('Insira a Radiacao Beta:\n')
       radiacaoGama = input('Insira a Radiacao Gama:\n')
       sonda = input('Insira o nome da sonda onde os dados serão registrados:\n')
       registerPath = os.path.join(os.getcwd(), sonda)

       if not os.path.exists(registerPath):
              cls()
              print('Menu:\n    3 - Coletar dados da sonda.\n')
              input(f'A sonda {sonda} ainda não foi registrada, realize o registro dela para prosseguir. (enter)')
              registerSonda()

       registerPath = os.path.join(os.getcwd(), sonda)
       register = os.path.join(registerPath, f'{local}_{data}.txt')
       with open(register, 'w') as registerFile:
                            registerFile.write(f'Sonda: {sonda}\n\nLocal: {local}\n\nData :{data}\n\nTemperatura: {temperatura}\n\nRadiação Alfa: {radiacaoAlfa}\n\nRadiação Beta: {radiacaoBeta}\n\nRadiação Gama: {radiacaoGama}')
                            registerTxt = open(register, 'r').read()
                            registerTxt ='\n'.join([register[i:i+64] for i in range (0, len(register),64)])