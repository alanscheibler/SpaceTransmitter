
# SpaceTransmitter
O projeto foi desenvolvido para o processo avaliativo da diciplina de CyberSecurity do curso de Ciências da Computação - Atitus 2023/02. O objetivo do projeto é realizar um sistema de registro de dados em arquivos, criptografá-los, gerar assinatura conforme sua respectiva sonda, e dar a possibilidade enviar para um socket server, seja ele local host ou executado por outra maquina.

## Funcionalidades
- Criação de sondas e das respectivas chaves privadas e públicas;
- Ver lista de sondas cadastradas;
- Enviar a chave da sonda para um socket server (local host ou externo);
- Coletar dados da sonda (gera um arquivo de registro .txt encriptado conforme uma chave inserida pelo usuário);
- Gerar assinatura do registro(gera um arquivo .txt contendo a assinatura do registro conforme a sonda em que foi registrado);
- Ver lista de registros da sonda;
- Enviar os arquivos registro para um socket server (envia o arquivo de registro juntamente da assinatura e realiza a verificação por parte do server);
-  
## Como executar
Antes de executar o arquivo você deve instalar as seguintes bibliotecas: rsa e pycryptodome
```
pip install rsa
```
```
pip install pycryptodome
```
Para executar você deve navegar através do prompt de comano até a pasta do projeto e executar o arquivo "main.py".

- Para executar, navegue até a pasta do projeto pelo prompt de comando e digite:

```
py main.py
```
OBS: 
- Sempre que terminar o envio dos dados via local host lembre-se de fechar o prompt de comando que foi aberto para não atrapalhar algum próximo envio que venha na seuquência.
- Quando tentar realizar o envio dos arquivos para outra maquina, o outro usuário deve navegar até a pasta "server", localizada dentro da pasta do projeto e executar o arquivo "Server Socket.py" e certificar-se de inserir corretamente o ip da maquina.
```
py ServerSocket.py
```


## Autor
-**Aluno:** Alan Marcelo Scheibler

-**RA:** 1130556
