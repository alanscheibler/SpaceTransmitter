import os
import rsa
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import subprocess
import time

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
              input(f'A sonda {sondaName} já foi registrada, registre sua sonda com um novo nome. (enter)')
       else:
              os.mkdir(folderPath)
              (pubKey, privKey) = rsa.newkeys(2048)
              with open(sondaPrivate, 'wb') as privateFile:
                     privateFile.write(privKey.save_pkcs1('PEM'))

              with open(sondaPublic, 'wb') as publicFile:
                     publicFile.write(pubKey.save_pkcs1('PEM'))

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
       registerName = f'{local}_{data}.txt'
       register = os.path.join(registerPath, registerName)
       with open(register, 'w') as registerFile:
                            registerFile.write(f'Sonda: {sonda}\n\nLocal: {local}\n\nData :{data}\n\nTemperatura: {temperatura}\n\nRadiação Alfa: {radiacaoAlfa}\n\nRadiação Beta: {radiacaoBeta}\n\nRadiação Gama: {radiacaoGama}')

       registerList = os.path.join(registerPath,"register_list.txt")
       if os.path.exists(registerList):
              with open(registerList, 'a') as listFile:
                     listFile.write(f'{registerName}\n')
       else:
              with open(registerList, 'w') as listFile:
                     listFile.write(f'{registerName}\n')

       key = input('Insira a chave para criptografia do arquivo:\n')
       key_aes = PBKDF2(key.encode(), salt=os.urandom(8), dkLen=32, count=1000000)

       cipher = AES.new(key_aes, AES.MODE_EAX)
       plainRegister = open(register, 'rb').read()
       cipherRegister, tag = cipher.encrypt_and_digest(plainRegister)

       with open(register,'wb') as registerFile:
               registerFile.write(cipher.nonce)
               registerFile.write(cipherRegister)
       
       input(f'Dados coletados e criptografados com sucesso! (enter)\n')

       
       #decipher = AES.new(key, AES.MODE_EAX, nonce=cipher.nonce)
       #decryptedData = decipher.decrypy_and_verify(cipherRegister, tag)

def sendKey(clientSocket, sondaName):
       publicKeyFile = os.path.join(os.getcwd(), sondaName, f'{sondaName}.public.pem')

       if os.path.exists(publicKeyFile):
              
              message = f'{sondaName}##KEY'
              clientSocket.sendall(message.encode())

              with open(publicKeyFile,'rb') as file:
                     fileData = file.read()
                     clientSocket.sendall(fileData)
                     print(f'Chave pública da sonda {sondaName} enviada com sucesso.')
       else:
              print(f'Chave pública da sonda {sondaName} não encontrada')

def sendRegister(clientSocket, sondaName, registerName):
       registerFile = os.path.join(os.getcwd(), sondaName, f'{registerName}.txt')
       if os.path.exists(registerFile):
              
              registerM = f'{sondaName}#{registerName}#REGISTER'
              clientSocket.sendall(registerM.encode())
              with open(registerFile,'rb') as file:
                     fileData = file.read()
                     clientSocket.sendall(fileData)
                     print(f'Registro "{registerName}" enviado com sucesso.')
       else:
              print(f'{registerName} não encontrado')

       time.sleep(1)

       registerSignature = os.path.join(os.getcwd(), sondaName, f'{registerName}.signature.txt')
       if os.path.exists(registerSignature):
              signatureM = f'{sondaName}#{registerName}#SIGNATURE'
              clientSocket.sendall(signatureM.encode())
              with open(registerSignature,'rb') as file:
                     registerSignatureData = file.read()
                     clientSocket.sendall(registerSignatureData)


def generateSignature():
       sonda = input('Digite o nome da sonda a qual deseja criar a assinatura dos dados:\n')
       register = input('Digite o nome do registro que deseja gerar a assinatura:\n')
       registerFile = os.path.join(os.getcwd(), sonda, f'{register}.txt')
       keyFile = os.path.join(os.getcwd(), sonda, f'{sonda}.private.pem')
       signaturePath = os.path.join(os.getcwd(), sonda, f'{register}.signature.txt')
       with open(keyFile, 'rb') as keyFile:
              privateKeyData = keyFile.read()
              privateKey = rsa.PrivateKey.load_pkcs1(privateKeyData)

       try:
              with open(registerFile, 'rb') as sign:
                     fileSing = sign.read()
              signature = rsa.sign(fileSing, privateKey, 'SHA-256')

              with open(signaturePath, 'wb') as signatureFile:
                     signatureFile.write(signature)
              input('Assinatura gerada com sucesso.(enter)')
       
       except FileNotFoundError:
               input(f'O arquive {register} não foi encontrado')

def serverSocket():
       mainPath = os.getcwd()
       serverPath = os.path.join(mainPath,'server')
       server = "server.py"
       cmd = f'start cmd.exe /K "cd /D {serverPath} && python {server}"'
       subprocess.Popen(cmd, shell=True)

       input('Apente enter para continuar após uma janela do cmd se abra:')
