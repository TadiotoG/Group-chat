Autores:    David Antonio Brocardo; 
            Leonardo Bednarczuk Balan de Oliveira; 
            Gabriel Tadioto de Oliveira.

Oque é necessario para rodar :
    - Caso não tenha Python instalado, execute o seguinte comando no PowerShell:
        winget install Python.Python.3
    - Para verificar versão:
        python --version

    -  Execute os comandos abaixo para instalar as bibliotecas necessárias
        pip install pycryptodome
        pip install cryptography   

Para rodar o Servidor, em um terminal localizado no diretório raiz do projeto, execute o comando:

	 python .\Servidor.py

Para rodar o Cliente, voce terá duas opções 
    - 1° Via terminal
            No diretório raiz do projeto, execute o comando:
	            python .\Cliente_com_Interface.py
    
    - 2° Via Executável no Windows:
            Execute o arquivo executável do cliente localizado no seguinte caminho:
                ...\Group-chat\Executavel\dist\Cliente_com_Interface.exe
	
O servidor e o cliente estão previamente configurados para rodar no IP da própria máquina (localhost) na porta 8080. 
Caso deseje alterar essas configurações, siga as instruções abaixo:

    - Alterar a Porta do Servidor:
        No arquivo Servidor.py, vá até a linha 572 e modifique a porta para o valor desejado
         - port = ColocarAquiPortaDesejada

    - Alterar IP e Porta do Cliente:

        Via Executável: 
            Informe o IP e a porta desejados. Para o IP local e porta 8080, basta digitar '0'.
        
        Via Terminal:
            No arquivo Cliente_com_Interface.py, vá até a linha 296 e modifique o IP e a porta para os valores desejados:
                host = "ColocarAquiIPDesejado"
                port = ColocarAquiPortaDesejada 
         