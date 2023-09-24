import os
from functions import *
import socket
import time
runnig = True
cls()

def menuOptions():
       global options
       options = input('-*-*-       Space Transmiter       -*-*-'+
                     '\n\n-Menu:'+
                     '\n    1 - Cadastrar Sonda e Gerar Par de Chaves.'+
                     '\n    2 - Ver lista de sondas cadastradas.'+
                     '\n    3 - Enviar Chave da Sonda.'+
                     '\n    4 - Coletar dados da sonda.'+
                     '\n    5 - Gerar Assinatura dos dados Coletados.'+
                     '\n    6 - Enviar para a Terra os dados.'
                     '\n    7 - Sair.\n')
       menu()
def menu():
       global runnig
       global options

       if options == '1':
              cls()
              print('-*-*-       Space Transmiter       -*-*-'+
              '\n\n-Menu: '+
              '      \n    1 - Cadastrar Sonda e Gerar Par de Chaves.\n')
              registerSonda()

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
              print('Menu:\n    3 - Enviar Chave da Sonda.')
              choseServer()
              

       elif options == '4':
              cls()
              print('Menu:\n    4 - Coletar dados da sonda.\n')
              registerData()

       elif options == '5':
              cls()
              print('Menu:\n    5 - Gerar Assinatura dos dados Coletados.')
              generateSignature()

       elif options == '6':
              cls()
              print('Menu:\n    6 - Enviar para a Terra os dados.' )
              choseServer()
       
       elif options == '7':
              cls()
              runnig = False
       else:
              print('Insira uma opção valida!\nPressione enter para continuar.')
              return
       
def clientSocket(HOST, PORT):
       global options
       clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       clientSocket.connect((HOST, PORT)) 
       while True:
              if options == '3':
                     sondaName = input('Digite o nome da sonda da qual deseja compartilhar a chave pública ("0" para sair:)\n')

                     if sondaName == '0':
                            break
                     sendKey(clientSocket, sondaName)
       
              if options == '6':
                     sondaName = input('Digite o nome da sonda da qual deseja compartilhar os registros. ("0" para sair:)\n')
                     registerName = input('Digite o nome do registro que deseja compartilhar o servidor. ("0" para sair:)\n')
                     if sondaName == '0' or registerName == '0':
                            break
                     sendRegister(clientSocket, sondaName, registerName)   

       clientSocket.close()

def choseServer():
       global options
       choseServer = input('Deseja fazer a conexão com local host (1) ou com outro computador(2)?')

       if options == '3':
              if choseServer == '1':
                     serverSocket()
                     HOST = '127.0.0.1'
                     PORT = 443
                     clientSocket(HOST, PORT)
                     input('Após o envio da chave, você pode fechar a janela do cmd aberta para prosseguir.(enter)')

              elif choseServer == '2':
                     HOST = input('Insira o IP da maquina que estará execuntando o socket server:\n')
                     PORT = int(input('Insira a porta configurada no socket serer:\n'))
                     input('Aguarde a outra maquina configurar executar o socket server e aperte enter')
                     clientSocket(HOST, PORT)

       elif options == '6':
              if choseServer == '1':
                     serverSocket()
                     HOST = '127.0.0.1'
                     PORT = 443
                     clientSocket(HOST, PORT)
                     input('Após o envio do registro, você pode fechar a janela do cmd aberta para prosseguir ou fazer outro envio.(enter)')

              elif choseServer == '2':
                     HOST = input('Insira o IP da maquina que estará execuntando o socket server:\n')
                     PORT = int(input('Insira a porta configurada no socket serer:\n'))
                     input('Aguarde a outra maquina configurar executar o socket server e aperte enter')
                     clientSocket(HOST, PORT)


       
input('-*-*-       Bem-vindo ao Space Transmiter!       -*-*-\n\n       Pressione enter para continuar.\n')



while runnig:
       cls()
       menuOptions()

       
       
              

