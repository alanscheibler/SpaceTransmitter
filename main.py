import os
from functions import cls, registerSonda, registerData
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

runnig = True
cls()

def menuOptions():
       global options
       options = input('-*-*-       Space Transmiter       -*-*-'+
                     '\n\n-Menu:'+
                     '\n    1 - Cadastrar Sonda e Gerar Par de Chaves.'+
                     '\n    2 - Enviar Chave da Sonda.'+
                     '\n    3 - Coletar dados da sonda.'+
                     '\n    4 - Gerar Assinatura dos dados Coletados.'+
                     '\n    5 - Enviar para a Terra os dados.'
                     '\n    6 - Sair.\n')
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
              print('Menu:\n    2 - Enviar Chave da Sonda.')

       elif options == '3':
              cls()
              print('Menu:\n    3 - Coletar dados da sonda.\n')
              registerData()

       elif options == '4':
              cls()
              print('Menu:\n    4 - Gerar Assinatura dos dados Coletados.')

       elif options == '5':
              cls()
              print('Menu:\n    5 - Enviar para a Terra os dados.' )
       
       elif options == '6':
              cls()
              runnig = False
       else:
              print('Insira uma opção valida!\nPressione enter para continuar.')
              return
       
input('-*-*-       Bem-vindo ao Space Transmiter!       -*-*-\n\n       Pressione enter para continuar.\n')

while runnig:
       cls()
       menuOptions()

       
              

