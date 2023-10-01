import socket
import threading
import os
import rsa
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

def cls():
       os.system("cls")



def verifySignature(sondaName, registerName):
    signaturePath = os.path.join(sondaName, f'{registerName}.signature.txt')
    registerPath = os.path.join(sondaName, f'{registerName}.txt')
    publicKeyPath = os.path.join(sondaName, f'{sondaName}.public.pem')

    with open(publicKeyPath, 'rb') as publicKeyFile:
        publicKeyData = publicKeyFile.read()
        publicKey = rsa.PublicKey.load_pkcs1(publicKeyData)
    with open(registerPath, 'rb') as registerFile:
        registerData = registerFile.read()
    with open(signaturePath, 'rb') as signatureFile:
        signatureData = signatureFile.read()

    try:
        rsa.verify(registerData, signatureData, publicKey)
        print('Assinatura verificada com sucesso pelo servidor!')
        verifyM = ('Assinatura verificada com sucesso!')
        clientSocket.sendall(verifyM.encode())
        return True
    except Exception as e:
        print('Falha na verificação da assinatura: ', str(e))
        verifyM = ('Assinatura verificada com sucesso pelo servidor!')
        clientSocket.sendall(verifyM.encode())
        return False
    
verify = 0
def receiveFile(clientSocket):
    global verify
    while True:
        try:       
            clientSocket.settimeout(60)
            message = clientSocket.recv(1024).decode()

            data = message.split('#')
            sondaName = data[0]
            registerName = data[1]
            fileType = data[2]

            print('Nome da sonda: ',sondaName,'\n')
            if registerName == '':
                print('Tipo do redistro: ', fileType)
            else:
                print('Nome do registro: ', registerName,'\n'
                    'Tipo do registro: ', fileType) 
            
            sondaFolder = os.path.join(sondaName)
            if not os.path.exists(sondaFolder):
                        os.makedirs(sondaFolder)
                        sondaListFile = os.path.join('sonda_list.txt')
                        with open(sondaListFile, 'a') as listFile:
                            listFile.write(f'-{sondaName}\n')

            if fileType == 'KEY':
                publicKeyData = clientSocket.recv(4096)
                if publicKeyData:
                    publicKeyFile = os.path.join(sondaFolder, f'{sondaName}.public.pem')

                with open(publicKeyFile, 'wb') as file:
                    file.write(publicKeyData)
                print(f'Chave pública da sonda {sondaName} recebida e salva com sucesso')
            
            elif fileType == 'REGISTER':
                verify = verify + 1
                registerData = clientSocket.recv(4096)
                if registerData:
                    with open(os.path.join(sondaFolder,f'{registerName}.txt'), 'wb') as regFile: 
                        regFile.write(registerData)

                registerList = os.path.join(sondaFolder,"register_list.txt")
                if os.path.exists(registerList):
                        with open(registerList, 'a') as listFile:
                                listFile.write(f'{registerName}\n')
                else:
                        with open(registerList, 'w') as listFile:
                                listFile.write(f'{registerName}\n')
                    
                
            elif fileType == 'SIGNATURE':
                verify = verify + 1
                signatureData = clientSocket.recv(4096)
                if signatureData:
                    with open(os.path.join(sondaFolder,f'{registerName}.signature.txt'), 'wb') as sigFile: 
                        sigFile.write(signatureData)

            if verify == 2:
                verify == 0       
                verifySignature(sondaName, registerName)
                 
        except socket.timeout:
            print('Tempo limite atingido. Fechando conexão')
            break
running = True
while running == True:
    cls()
    options = input('-*-*-       Space Transmiter       -*-*-'+
                    '\n-*-*-    server socket    -*-*-'
                     '\n\nMenu:'+
                     '\n    1 - Executar server.'+
                     '\n    2 - Ver lista de sondas cadastradas.'+
                     '\n    3 - Sair.\n')
    
    if options == '1':
        cls()
        print('Menu:\n    1 - Executar server.')
        choseServer = input('Deseja rodar o server para local host(1) ou deseja conectar-se com uma maquina externa(2)?')
        if choseServer == '1':
            HOST = '127.0.0.1'
            PORT = 443

        elif choseServer == '2':
            HOST = input('Insira o ip da sua maquina:\n')

            PORT = int(input('Insira a porta que desjea realizar a conexão:\n'))
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((HOST, PORT))
        serverSocket.listen()

        print('Aguardando conexões...')     
        clientSocket, clientAddress = serverSocket.accept()
        print('Conexão estabelecida com: ', clientAddress)
        clientHandler = threading.Thread(target=receiveFile, args=(clientSocket,))
        clientHandler.start()

    elif options == '2':
        cls()
        print('Menu:\n    2 - Ver lista de sondas cadastradas.')
        sondaFile = 'sonda_list.txt'
        sondaList = []

        if os.path.exists(sondaFile):
                with open(sondaFile, 'r') as sondaFile:
                    sondaList = sondaFile.read().splitlines()
                    for index, sonda in enumerate(sondaList, start=1):
                            input(f'\n{index} - {sonda}.\n(enter)')
                            
                
        elif sondaList == [] or not os.path.exists(sondaFile) :
                input('\nAinda não existem sondas cadastradas. (enter)')

    
    elif options == '3':
        cls()
        running = False
        
    else:
        input('Insira uma opção valida!\nPressione enter para continuar.')
            
        

    