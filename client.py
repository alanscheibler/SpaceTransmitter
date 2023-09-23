#client socket
import socket
import threading
import os

def sendFile(clientSocket, fileName):
    try:
        fileSize = os.path.getsize(fileName)
        clientSocket.send(fileName.encode())
        clientSocket.send(str(fileSize).encode())
        with open (fileName, 'rb') as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                clientSocket.send(data)
        print('Arquivo enviado: ', fileName)
    except FileNotFoundError:
        print('Arquivo não encontrado: ', fileName)

HOST_B = '127.0.0.1'
PORT_B = 443

clientSocketB = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
clientSocketB.connect((HOST_B, PORT_B))

receiveThread = threading.Thread(target=sendFile, args=(clientSocketB,))
receiveThread.start()

while True:
    message = input('Digite o nome do arquivo que deseja enviar ao computador A:\n')
    clientSocketB.sendall(message.encode())

clientSocketB.close()
