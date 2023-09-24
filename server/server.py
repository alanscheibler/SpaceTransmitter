import socket
import threading
import os
import rsa

HOST = '127.0.0.1'
PORT = 443

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen()


print('Aguardando conexões...')

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
        print('Assinatura verificada com sucesso!')
        return True
    except Exception as e:
        print('Falha na verificação da assinatura: ', str(e))
        return False
    
verify = 0
def handleClient(clientSocket):
    global verify
    while True:
        try:       
            clientSocket.settimeout(60)
            message = clientSocket.recv(1024).decode()
            print(verify)

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
                print(verify)
                registerData = clientSocket.recv(4096)
                if registerData:
                    with open(os.path.join(sondaFolder,f'{registerName}.txt'), 'wb') as regFile: 
                        regFile.write(registerData)
                    
                
            elif fileType == 'SIGNATURE':
                verify = verify + 1
                print(verify)
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

while True:
    clientSocket, clientAddress = serverSocket.accept()
    print('Conexão estabelecida com: ', clientAddress)
    clientHandler = threading.Thread(target=handleClient, args=(clientSocket,))
    clientHandler.start()

        