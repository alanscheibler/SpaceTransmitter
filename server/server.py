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
    message = clientSocket.recv(1024).decode()
    print('Mensagem recebida:\n', message)
    
    publicKeyData = clientSocket.recv(4096)
    
    if publicKeyData:
        sondaName = message.split()[-1]
        sondaFolder = os.path.join(sondaName)

        if not os.path.exists(sondaFolder):
            os.makedirs(sondaFolder)

        publicKeyFile = os.path.join(sondaFolder, f'{sondaName}.public.pem')

        with open(publicKeyFile, 'wb') as file:
            file.write(publicKeyData)
        print(f'Chave pública da sonda {sondaName} receboda e salva com sucesso')
    else:
        print('Nenhum dado recebido')
    
    sondaListFile = os.path.join('sonda_list.txt')
    with open(sondaListFile, 'a') as listFile:
        listFile.write(f'-{sondaName}\n')

    clientSocket.close()

while True:
    clientSocket, clientAddress = serverSocket.accept()
    print('Conexão estabelecida com: ', clientAddress)
    clientHandler = threading.Thread(target=handleClient, args=(clientSocket,))
    clientHandler.start()

        