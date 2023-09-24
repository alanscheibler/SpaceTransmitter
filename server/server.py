import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 443

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen()


print('Aguardando conexões...')

def handleClient(clientSocket):
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
                    'Tipo do redistro: ', fileType) 
            
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
                registerData = clientSocket.recv(4096)
                if registerData:
                    with open(os.path.join(sondaFolder,f'{registerName}.txt'), 'wb') as regFile: 
                        regFile.write(registerData)
                    print('Arquivo de registro recebido e salvo com sucesso!')
                
            elif fileType == 'SIGNATURE':
                signatureData = clientSocket.recv(4096)
                if signatureData:
                    with open(os.path.join(sondaFolder,f'{registerName}.signature.txt'), 'wb') as sigFile: 
                        sigFile.write(signatureData)
                    print('Arquivo de assinatura recebido e salvo com sucesso!')
                    
        except socket.timeout:
            print('Tempo limite atingido. Fechando conexão')
            break

while True:
    clientSocket, clientAddress = serverSocket.accept()
    print('Conexão estabelecida com: ', clientAddress)
    clientHandler = threading.Thread(target=handleClient, args=(clientSocket,))
    clientHandler.start()

        