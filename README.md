
# SpaceTransmitter
O projeto foi desenvolvido para o processo avaliativo da diciplina de CyberSecurity do curso de Ciências da Computação - Atitus 2023/02. O objetivo do projeto é realizar um sistema de registro de dados em arquivos, criptografá-los, gerar assinatura conforme sua respectiva sonda, e dar a possibilidade enviar para um socket server, seja ele local host ou executado por outra maquina.

## Funcionalidades
- Registro de sondas (cria uma pasta dedicada para os quivos da sonda assim como suas respectivas chaves);
- Ver lista de sondas cadastradas(mostra todas as sondas registradas);
- Enviar a chave da sonda para um socket server (local host ou externo);
- Coletar dados da sonda (gera um arquivo de registro .txt encriptado conforme uma chave inserida pelo usuário);
- Gerar assinatura do registro (gera um arquivo contendo a assinatura dos registros conforme a sonda em que foi realizado);
- Ver lista de registros da sonda (mostra todos os arquivos de registro cadastrados em uma sonda específica);
- Enviar os arquivos para a Terra (envia o arquivo de registro juntamente da assinatura e realiza a verificação por parte do server para confirmar que os arquivos não foram interceptados e alterados);
-   
## Como executar
Antes de executar o arquivo você deve instalar as seguintes dependencias: rsa e pycryptodome.
```
pip install rsa
```
```
pip install pycryptodome
```
Para executar você deve navegar através do prompt de comando até a pasta do projeto e executar o arquivo "main.py".

- Para executar, navegue até a pasta do projeto pelo prompt de comando e digite:

```
py main.py
```
OBS: 
- Sempre que terminar o envio dos dados via local host lembre-se de fechar o prompt de comando que foi aberto para não atrapalhar algum próximo envio que venha na sequência.
- Quando tentar realizar o envio dos arquivos para outra maquina, o outro usuário que rodará o server socket deve navegar até a pasta "server", localizada dentro da pasta do projeto e executar o arquivo "Server Socket.py" e certificar-se de inserir corretamente o ip da maquina assim como a porta e informar os dados para o momento do envio.
```
py ServerSocket.py
```


## Autor
-**Aluno:** Alan Marcelo Scheibler

-**RA:** 1130556
