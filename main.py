import os
from functions import cls, registerSonda, registerData, sendKey, clientSocket, generateSignature
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
import socket
import subprocess


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
              global choseServer
              choseServer = input('Deseja fazer a conexão com local host (1) ou com outro computador(2)?')

              if choseServer == '1':
                     mainPath = os.getcwd()
                     serverPath = os.path.join(mainPath,'server')
                     server = "server.py"
                     cmd = f'start cmd.exe /K "cd /D {serverPath} && python {server}"'
                     subprocess.Popen(cmd, shell=True)

                     input('Apente enter para continuar após uma janela do cmd se abra:')
                     HOST = '127.0.0.1'
                     PORT = 443
                     clientSocket(HOST, PORT)
                     input('Após o envio da chave, você pode fechar a janela do cmd aberta para prosseguir.(enter)')

              elif choseServer == '2':
                     HOST = input('Insira o IP da maquina que estará execuntando o socket server:\n')
                     PORT = int(input('Insira a porta configurada no socket serer:\n'))
                     input('Aguarde a outra maquina configurar executar o socket server e aperte enter')
                     clientSocket(HOST, PORT)
                     

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
       
       elif options == '7':
              cls()
              runnig = False
       else:
              print('Insira uma opção valida!\nPressione enter para continuar.')
              return
       
input('-*-*-       Bem-vindo ao Space Transmiter!       -*-*-\n\n       Pressione enter para continuar.\n')

while runnig:
       cls()
       menuOptions()

       
       
              

