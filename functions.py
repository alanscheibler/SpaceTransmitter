import os
import rsa
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import subprocess
import time
import datetime

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
                            listFile.write(f' {sondaName}\n')
              else:
                     with open(sondaFile, 'w') as listFile:
                            listFile.write(f'{sondaName}\n')


def registerData():
       while True:
              local = input('Insira o local do registro:\n')
              local = ''.join(char if char not in invalidCharacters else '.' for char in local)
              if local.strip():
                     break
              else:
                     print('O local não pode estar vazio. Por favor, insira um valor válido.')

       now = datetime.datetime.now()
       data = now.strftime("%d.%m") 
       temperatura = input('Insira a Temperatura:\n')
       radiacaoAlfa = input('Insira a Radiação Alfa:\n')
       radiacaoBeta = input('Insira a Radiação Beta:\n')
       radiacaoGama = input('Insira a Radiação Gama:\n')
       while True:
              sonda = input('Insira o nome da sonda onde os dados serão registrados:\n')
              sonda = ''.join(char if char not in invalidCharacters else '.' for char in sonda)
              if sonda.strip():
                     break
              else:
                     print('O nome da sonda não pode estar vazio, insira um nome válido.')

       registerPath = os.path.join(os.getcwd(), sonda)

       if not os.path.exists(registerPath):
              print('Menu:\n    3 - Coletar dados da sonda.\n')
              input(f'A sonda {sonda} ainda não foi registrada, realize o registro dela para prosseguir. (enter)')
              return

       registerPath = os.path.join(os.getcwd(), sonda)
       registerName = f'{local}.{data}.txt'
       register = os.path.join(registerPath, registerName)
       with open(register, 'w') as registerFile:
              registerFile.write(f'Sonda: {sonda}\n\nLocal: {local}\n\nData :{data}\n\nTemperatura: {temperatura}\n\nRadiacao Alfa: {radiacaoAlfa}\n\nRadiacao Beta: {radiacaoBeta}\n\nRadiacao Gama: {radiacaoGama}')

       registerList = os.path.join(registerPath,"register_list.txt")
       if os.path.exists(registerList):
              with open(registerList, 'a') as listFile:
                     listFile.write(f'{registerName}\n')
       else:
              with open(registerList, 'w') as listFile:
                     listFile.write(f'{registerName}\n')

       key = input('Insira a chave de criptografia do arquivo:\n')
       if len(key) < 16:
              key = key.ljust(16)
       elif len(key) > 16:
              key = key[:16]

       keyAES = key.encode('utf-8')
       cipher = AES.new(keyAES, AES.MODE_EAX)

       with open(register, 'rb') as file:
              plaintext = file.read()  
       cipherText, tag = cipher.encrypt_and_digest(plaintext)

       with open(register, 'wb') as encryptedFile:
              encryptedFile.write(cipherText)

       #Decifra o texto
       #     key = input('Insira a chave de criptografia do arquivo:\n')
       #     if len(key) < 16:
       #        key = key.ljust(16)
       #     elif len(key) > 16:
       #         key = key[:16]
       #     keyAES = key.encode('utf-8')
       #cipher = AES.new(keyAES, AES.MODE_EAX)
       #cipherText, tag = cipher.encrypt_and_digest(plaintext)    
       #decipher = AES.new(keyAES, AES.MODE_EAX, nonce=cipher.nonce)
       #decryptedData = decipher.decrypt_and_verify(cipherText, tag)
       
       input(f'Dados coletados e criptografados com sucesso! (enter)\n')

       
       

def sendKey(clientSocket, sondaName):
       publicKeyFile = os.path.join(os.getcwd(), sondaName, f'{sondaName}.public.pem')

       if os.path.exists(publicKeyFile):
              
              message = f'{sondaName}##KEY'
              clientSocket.sendall(message.encode())

              with open(publicKeyFile,'rb') as file:
                     fileData = file.read()
                     clientSocket.sendall(fileData)
                     input(f'Chave pública da sonda {sondaName} enviada com sucesso.(enter)')
       else:
              input(f'Chave pública da sonda {sondaName} não encontrada.(enter)')

def sendRegister(clientSocket, sondaName, registerName):
       registerFile = os.path.join(os.getcwd(), sondaName, f'{registerName}.txt')
       registerSignature = os.path.join(os.getcwd(), sondaName, f'{registerName}.signature.txt')
       if not os.path.exists(registerSignature):
              input('Assinatura não encontrada.(enter)')
              generateSignature()
       if os.path.exists(registerFile):
              
              registerM = f'{sondaName}#{registerName}#REGISTER'
              clientSocket.sendall(registerM.encode())
              with open(registerFile,'rb') as file:
                     fileData = file.read()
                     clientSocket.sendall(fileData)
                     input(f'Registro "{registerName}" enviado com sucesso.(enter)')
       else:
              input(f'{registerName} não encontrado.(enter)')

       time.sleep(1)

       if os.path.exists(registerSignature):
              signatureM = f'{sondaName}#{registerName}#SIGNATURE'
              clientSocket.sendall(signatureM.encode())
              with open(registerSignature,'rb') as file:
                     registerSignatureData = file.read()
                     clientSocket.sendall(registerSignatureData)

       verifyM = clientSocket.recv(1024).decode()
       input(f'{verifyM}(enter)') 


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
