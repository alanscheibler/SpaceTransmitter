import os
from functions import cls
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

cls()      

input('-*-*-       Bem-vindo ao Space Transmiter!       -*-*-\n\n       Pressione qualquer tecla para continuar.\n')
cls()

options = input('-*-*-       Space Transmiter       -*-*-'+
       '\n\n-Menu:'+
       '\n    1 - Cadastrar Sonda e Gerar Par de Chaves.'+
       '\n    2 - Enviar Chave da Sonda.'+
       '\n    3 - Coletar dados da sonda.'+
       '\n    4 - Gerar Assinatura dos dados Coletados.'+
       '\n    5 - Enviar para a Terra os dados.\n')
def registerSonda():
              
       sondaName = input('Insira o nome da sonda:\n')
       sondaPrivate = sondaName.replace(" ", "_") + '.private.pem'
       sondaPublic = sondaName.replace(" ", "_") + '.public.pem'
       try:
              #substituir por verificação de nome da sona
              #caso uma sonda já possua esse nome retornar mensagem de erro e solicitar novamente
              #caso seja um nome novo, criar uma pasta com o nome e da sonda e passar a criação das chaves para essa pasta
              privateKeyPem = open(sondaPublic, 'rb').read()
              publicKeyPem = open(sondaPublic, 'rb').read()
       except:
              key = RSA.generate(1024)
              privateGen = key.export_key()

              with open(sondaPrivate, 'wb') as privateFile:
                     privateFile.write(privateGen)
              privateKeyPem = open(sondaPrivate, 'rb').read()
              privateKeyPem = b'\n'.join([privateKeyPem[i:i+64] for i in range (0, len(privateKeyPem),64)])

              publicGen = key.publickey().export_key()
              with open(sondaPublic, 'wb') as publicFile:
                     publicFile.write(publicGen)
              publicKeyPem = open(sondaPublic,'rb').read()
              publicKeyPem = b'\n'.join([publicKeyPem[i:i+64] for i in range(0, len(publicKeyPem), 64)])


try:
       if options == '1':
              registerSonda()
       elif options == '2':
              print()
       elif options == '3':
              print()
       elif options == '4':
              print()
       elif options == '5':
              print()
except:
       print('Insira uma opção valida!')

