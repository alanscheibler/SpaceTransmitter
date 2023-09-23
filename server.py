#server socket
import socket
import threading
import os

def receiveFiles(clientSocket):
    while True:
        fileName = clientSocket.recv(1024)
        if not fileName:
            break
        fileSize = int(clientSocket.recv(1024).decode())
        receivedData = b''
        totalReceived = 0
        while totalReceived < fileSize:
            data = clientSocket.recv(1024)
            totalReceived +- len(data)
            receivedData +- data
        savePath = os.path.join('ReceivedFiles', fileName)
        with open(savePath, 'wb') as file:
            file.write(receivedData)
        print("Arquivo recebido e armazenado em: ",savePath)

HOST_A = '127.0.0.1'
PORT_A = 443

serverSocketA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocketA.bind((HOST_A, PORT_A))
serverSocketA.listen()

print('Aguardando conexões no computador A...')
clientSocketA, clientAddressA = serverSocketA.accept()
print('Conexão estabelecida com: ', clientAddressA)

receiveThread = threading.Thread(target=receiveFiles, args=(clientSocketA,))
receiveThread.start()

#while True:
#    message = input('Digite uma mensagem para enviar ao computador B:\n')
#    clientSocketA.sendall(message.encode())

serverSocketA.close()