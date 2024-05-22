import socket
import threading
import csv
import pandas as pd
import os
import base64
from Class_Sala import Sala
from cryptography.hazmat.primitives import serialization,hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

class Servidor:
    def __init__(self): # Se nao passar parametros cria novo servidor
        self.clientes = []
        self.salas = []
        self.usuarios_cadastrados = [] # Vai ter tudo
        self.usuarios_autenticados = []  # Vai ter somente os que estao em uso a parti que o servidor comeca a rodar
        self.codigo_usuarios = [] # Armazena a porta e o ip no mesmo indice que que o autenticado
        self.socket = [] # Guarda o socket de cada cliente conectado
        self.chave_simetrica = []
        self.controle_crip = False
    @staticmethod
    def carrega_usuario(self):
        try:
            with open('UsuariosCadastrados.csv', 'r') as csvfile:
                print("Carrregando Servidor ...")
        except IOError:
            print('Criando Servidor ...')
            print('Servidor Criado')            
            with open('UsuariosCadastrados.csv', 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames= ['NOME'])
                writer.writeheader()
                writer.writerow({'NOME':'David'})
                
        # Carregar usuários cadastrados de algum lugar
        self.usuarios_cadastrados = pd.read_csv('UsuariosCadastrados.csv', sep=',', encoding='latin-1')
        
        return self.usuarios_cadastrados
    
    # Função para criptografar a mensagem
    @staticmethod
    def encrypt_message(key, iv, message):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_message = base64.b64encode(cipher.encrypt(pad(message.encode(), AES.block_size)))
        return encrypted_message

    # Função para descriptografar a mensagem
    @staticmethod
    def decrypt_message(key, iv, encrypted_message):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_message = unpad(cipher.decrypt(base64.b64decode(encrypted_message)), AES.block_size)
        return decrypted_message    

    @staticmethod
    def obter_chave_publica_codificada(self):
        # Serializar a chave pública
        chave_publica_serializada = self.chave_publica.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        # Codificar em Base64 e retornar
        chave_publica_codificada = b64encode(chave_publica_serializada).decode('utf-8')
        return chave_publica_codificada
    
    @staticmethod
    def obter_chave_privada(self):
        # Serializar a chave privada
        chave_privada_serializada = self.chave_privada.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        # Codificar em Base64 e retornar
        #chave_privada_codificada = b64encode(chave_privada_serializada).decode('utf-8')
        return chave_privada_serializada


    @staticmethod
    def carrega_salas(self):
        try:
            with open('SalasCadastradas.csv', 'r') as csvfile:
                print("Carrregando Servidor ...")
        except IOError:
            print('Criando Servidor ...')
            print('Servidor Criado')            
            with open('SalasCadastradas.csv', 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames= ['NOME', 'CRIADOR', 'SENHA', 'USUARIOS'])
                writer.writeheader()
                
        # Carregar usuários cadastrados de algum lugar
        csv_salas = pd.read_csv('SalasCadastradas.csv')
        for i in range(len(csv_salas)):
            if str(csv_salas["SENHA"][i]) != "nan":
                new_sala = Sala(str(csv_salas["NOME"][i]), str(csv_salas["CRIADOR"][i]), str(csv_salas["SENHA"][i]))

            else:
                new_sala = Sala(str(csv_salas["NOME"][i]), str(csv_salas["CRIADOR"][i]))

            todos_usuarios = str(csv_salas["USUARIOS"][i])
            lista_todos_usuarios = todos_usuarios.split(" ") # Estava pegando o espaco final como um elemento
            del(lista_todos_usuarios[len(lista_todos_usuarios)-1]) # Retira o espaco final
            
            new_sala.load_system(lista_todos_usuarios)
            self.salas.append(new_sala)
        # new_sala = Sala(nome_da_sala, nome_usuario, senha)

    @staticmethod
    def autentifica_usuario(self, usuario, addr):
        user = self.usuarios_cadastrados['NOME']
        for nome in user:
            if usuario == nome:
                return True    
        return False

    @staticmethod
    def verifica_autenticidade(self, usuario):        
        for nome in self.usuarios_autenticados:
            if usuario == nome:
               return True
        return False
    
    @staticmethod
    def grava_autentifica_usuario(self, usuario, addr, chave): 
        user = self.usuarios_cadastrados['NOME']
        for nome in user:
            if usuario == nome:
                self.usuarios_autenticados.append(nome)
                self.codigo_usuarios.append(addr)
                self.chave_simetrica.append(chave)
                return True    
        return False
    
    @staticmethod
    def registro_usuario(self, usuario, addr):
        #usuarios_cadastrados = self.carrega_usuario(self)
        user = self.usuarios_cadastrados['NOME']
        for nome in user:
            if usuario == nome:
                return 'ERRO: Já existe um usuário com este nome.'
        
        with open('UsuariosCadastrados.csv', 'a', newline='') as csvfile:
            fieldnames = ['NOME']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'NOME': usuario})
            novo_usuario = pd.DataFrame({'NOME': [usuario]})
            self.usuarios_cadastrados = pd.concat([self.usuarios_cadastrados, novo_usuario],ignore_index=True)
            #self.usuarios_autenticados.append(usuario)
            #end = ' '.join((addr[0], str(addr[1]))) # COLOQUEI str(addr[1])
            #self.codigo_usuarios.append(end)
        #print(self.usuarios_autenticados[0])
        #print(addr[1])
        return 'REGISTRO_OK'
    
    @staticmethod
    def identifica_usuario(self,addr):
        #user = self.usuarios_cadastrados['NOME']        
        i = 0
        for end in self.codigo_usuarios:
            if end[0] == addr[0] and end[1] == addr [1]:
                print(self.usuarios_autenticados)
                return self.usuarios_autenticados[i]  
            i += 1

    @staticmethod
    def identifica_chave(self,addr):
        #user = self.usuarios_cadastrados['NOME']        
        i = 0
        for end in self.codigo_usuarios:
            if end[0] == addr[0] and end[1] == addr [1]:
                #print(self.usuarios_autenticados)
                return self.chave_simetrica[i]  
            i += 1
    @staticmethod
    def identifica_endereco(self,nome_buscado):   
        i = 0
        for nome in self.usuarios_autenticados:
            print("Nome : " , nome)
            print("Nome : " , nome_buscado)
            if nome == nome_buscado :
                print(self.codigo_usuarios[i])
                return self.codigo_usuarios[i]  
            i += 1
    
    @staticmethod
    def handle_client(self, client_socket, addr):
        print('Conexão recebida de', addr)
        # Envia uma mensagem de boas-vindas para o cliente
        client_socket.send(b'Obrigado por se conectar!')
        resposta = ""

        while True:
            msg = client_socket.recv(1024)
            if not msg: break
            #print('Mensagem do cliente:', msg.decode())
            #msg = msg.decode() 
            #msg = msg.decode(errors='ignore')  # Tentativa de decodificação ignorando erros
            if " " in msg.decode():
            #if msg:
            #if isinstance(msg, bytes):
              #try:
                #print("TESTE 0")
                self.controle_crip = False
                msg = msg.decode()                
                mensagem =  msg.split(" ")
                print('Mensagem do cliente:', msg)
                #except:
            else:
                self.controle_crip = True
                #print("TESTE")
                chave_simetrica = self.identifica_chave(self, addr)                
                #msg = b64decode(msg)
                #print(chave_simetrica)
                key = chave_simetrica[:32]
                iv = chave_simetrica[32:]
                #print("Chave " , key)
                #print("IV ", iv)
                msg = self.decrypt_message(key, iv, msg)
                msg = msg.decode()
                mensagem =  msg.split(" ")
                #print(mensagem)

            # REGISTRO
            if mensagem[0] ==  "REGISTRO":              
                nome_usuario = mensagem[1]
                resposta = self.registro_usuario(self, nome_usuario, addr)
            
            # AUTENTICACAO
            elif mensagem[0] ==  "AUTENTICACAO":              
                nome_usuario = mensagem[1]
                if(self.autentifica_usuario(self, nome_usuario, addr)):
                    resposta = "CHAVE_PUBLICA " + self.chave_publica_codificada       
            

            elif mensagem[0] == "CHAVE_SIMETRICA":
                
                chave_simetrica = b64decode(mensagem[1])
                #print(mensagem[1])
                chave_simetrica_decrypted = self.chave_privada.decrypt(
                    chave_simetrica,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                #print(chave_simetrica_decrypted)
                self.grava_autentifica_usuario(self, nome_usuario, addr, chave_simetrica_decrypted)
                
            # CRIAR SALA
            elif mensagem[0] == "CRIAR_SALA":
                privacidade = mensagem[1]
                nome_da_sala = mensagem[2]
                nome_usuario = self.identifica_usuario(self, addr)
                if self.verifica_autenticidade(self,nome_usuario):
                    if -1 != self.encontrar_sala(nome_da_sala):
                        resposta = "ERRO: Sala já existente!"

                    elif privacidade == "PRIVADA":
                        if len(mensagem) > 3:
                            senha = mensagem[3]
                            new_sala = Sala(nome_da_sala, nome_usuario, senha)
                            self.salas.append(new_sala)
                            self.salvar_salas_csv()
                            resposta = "CRIAR_SALA_OK"
                        else:
                            resposta = "ERRO : Ausencia de senha para sala PRIVADA"

                    else:
                        new_sala = Sala(nome_da_sala, nome_usuario)
                        self.salas.append(new_sala)
                        resposta = "CRIAR_SALA_OK"
                        self.salvar_salas_csv()
                else:
                    resposta = "ERRO : Para realizar essa operacao é necessario realizar a AUTENTICACAO primeiro !!! "
            # ENTRAR NA SALA
            elif mensagem[0] == "ENTRAR_SALA":
                nome_usuario = self.identifica_usuario(self, addr)
                nome_da_sala = mensagem[1]
                senha = ""
                if self.verifica_autenticidade(self,nome_usuario):
                    if len(mensagem) > 2:
                        senha = mensagem[2]

                    indice_sala = self.encontrar_sala(nome_da_sala)

                    if indice_sala == -1:
                        resposta = "ERRO: Sala não encontrada!"

                    else:
                        resposta = self.salas[indice_sala].add_new_client(nome_usuario, senha)
                        self.salvar_salas_csv()
                        usuarios = self.salas[indice_sala].list_clients()
                        usuarios_da_sala =  usuarios.split(', ')                       
                        for nome in usuarios_da_sala:
                            end_envio = self.identifica_endereco(self,nome)
                            if end_envio != None:
                                for i in range(len(self.socket)):
                                    end_socket = self.socket[i].getpeername()
                                    if end_envio[0] != addr[0] or end_envio[1] != addr[1]:
                                        if end_envio[0] == end_socket[0] and end_envio[1] == end_socket[1]:
                                            cliente = self.socket[i]
                                            conteudo = "ENTROU " + nome_da_sala + " " + nome_usuario
                                            cliente.send(conteudo.encode())

                else:
                    resposta = "ERRO : Para realizar essa operacao é necessario realizar a AUTENTICACAO primeiro !!! "
            
            # SAIR_SALA
            # Tadioto verificar na especificacao e ajeitar algumas saidas de acordo com oque foi pedido
            elif mensagem[0] == "SAIR_SALA":
                nome_usuario = self.identifica_usuario(self, addr)
                nome_da_sala = mensagem[1]
                indice_sala = self.encontrar_sala(nome_da_sala)
                if self.verifica_autenticidade(self,nome_usuario):
                    if indice_sala == -1:
                        resposta = "ERRO: Sala não encontrada!"

                    else:
                        resposta = self.salas[indice_sala].remove_client(nome_usuario, nome_usuario)
                        if len(self.salas[indice_sala].clients) < 1:
                            del(self.salas[indice_sala])
                            resposta = resposta + " E sala Fechada!"
                        self.salvar_salas_csv()
                else:
                    resposta = "ERRO : Para realizar essa operacao é necessario realizar a AUTENTICACAO primeiro !!! "

            # LISTAR_SALAS
            elif mensagem[0] == "LISTAR_SALAS": 
                #Funcao responsavel por verificar qual usuario solicitou a informação
                nome=self.identifica_usuario(self,addr)
                if self.verifica_autenticidade(self,nome):
                    resposta = "SALAS: "
                    for sala in self.salas:
                        resposta = resposta + sala.sala_name + ", "
                else:
                    resposta = "ERRO : Para realizar essa operacao é necessario realizar a AUTENTICACAO primeiro !!! "
            # BANIR_USUARIO
            elif mensagem[0] == "BANIR_USUARIO":
                nome_usuario = self.identifica_usuario(self, addr)
                nome_da_sala = mensagem[1]
                usuario_banido = mensagem[2]
                indice_sala = self.encontrar_sala(nome_da_sala)
                if self.verifica_autenticidade(self,nome_usuario):
                    if indice_sala == -1:
                        resposta = "ERRO: Sala não encontrada!"

                    else:
                        resposta = self.salas[indice_sala].remove_client(nome_usuario, usuario_banido) #BANIMENTO_OK
                        self.salvar_salas_csv()
                else:
                    resposta = "ERRO : Para realizar essa operacao é necessario realizar a AUTENTICACAO primeiro !!! "
            # SAIR DO SISTEMA
            elif mensagem[0] == "DESCONECTAR":
                print("Cliente ", self.identifica_usuario(self,addr), " desconectado")
                resposta = "Desconectado do servidor!"

            # LISTAR USUARIOS DE UMA SALA
            elif mensagem[0] == "LISTAR_USUARIOS":
                nome_da_sala = mensagem[1]
                indice_sala = self.encontrar_sala(nome_da_sala)

                if indice_sala == -1:
                    resposta = "ERRO: Sala não encontrada!"

                else:
                    resposta = self.salas[indice_sala].list_clients()

            # ENVIAR MENSAGEM 
            elif mensagem[0] == "ENVIAR_MENSAGEM" :
                nome_usuario = self.identifica_usuario(self, addr)
                if self.verifica_autenticidade(self,nome_usuario):
                    nome_da_sala = mensagem[1]
                    conteudo = mensagem[2]
                    if (len(mensagem)> 2):
                        mensagem = mensagem[3:]
                        for i in range(len(mensagem)):
                            conteudo = conteudo +" "+ mensagem[i] + "\n"
                    indice_sala = self.encontrar_sala(nome_da_sala)
                    if indice_sala == -1:
                        resposta = "ERRO: Sala não encontrada!"
                    else:
                        resposta = self.salas[indice_sala].list_clients()
                        usuarios_da_sala =  resposta.split(', ')
                        resposta = "Mensagem enviada"
                        for nome in usuarios_da_sala:
                            end_envio = self.identifica_endereco(self,nome)
                            if end_envio != None:
                                for i in range(len(self.socket)):
                                    end_socket = self.socket[i].getpeername()   
                                    #print(end_envio[0])
                                    #print(end_socket[0])
                                    #print(end_envio[1])
                                    #print(end_socket[1])
                                    if end_envio[0] != addr[0] or end_envio[1] != addr[1]:
                                        if end_envio[0] == end_socket[0] and end_envio[1] == end_socket[1]:
                                            cliente = self.socket[i]
                                            conteudo = "MENSAGEM " + nome_da_sala + " " + self.identifica_usuario(self,addr) + " " + conteudo
                                            cliente.send(conteudo.encode())
                                            #print(self.socket[i])
                else:
                    resposta = "ERRO : Para realizar essa operacao é necessario realizar a AUTENTICACAO primeiro !!! "

            # FECHA SALA
            elif mensagem[0] == "FECHAR_SALA":
                nome_usuario = self.identifica_usuario(self, addr)
                nome_da_sala = mensagem[1]
                indice_sala = self.encontrar_sala(nome_da_sala)
                if self.verifica_autenticidade(self,nome_usuario):
                    if indice_sala == -1:
                        resposta = "ERRO: Sala não encontrada!"

                    else:
                        if self.salas[indice_sala].admin != nome_usuario:
                            resposta = "ERRO: Voce nao tem permissao para fechar esta sala"
                    
                        else:
                            resposta = self.salas[indice_sala].list_clients()
                            usuarios_da_sala =  resposta.split(', ')
                            for nome in usuarios_da_sala:
                                end_envio = self.identifica_endereco(self,nome)
                                if end_envio != None:
                                    for i in range(len(self.socket)):
                                        end_socket = self.socket[i].getpeername()
                                        if end_envio[0] != addr[0] or end_envio[1] != addr[1]:
                                            if end_envio[0] == end_socket[0] and end_envio[1] == end_socket[1]:
                                                cliente = self.socket[i]
                                                conteudo = "Sala " + nome_da_sala + " fechada!"
                                                cliente.send(conteudo.encode())
                        
                            
                            self.salvar_salas_csv()
                            resposta = "FECHAR_SALA_OK"
                            usuarios = self.salas[indice_sala].list_clients()
                            usuarios_da_sala =  usuarios.split(', ')     
                            del(self.salas[indice_sala])                  
                            for nome in usuarios_da_sala:
                                end_envio = self.identifica_endereco(self,nome)
                                if end_envio != None:
                                    for i in range(len(self.socket)):
                                        end_socket = self.socket[i].getpeername()
                                        if end_envio[0] != addr[0] or end_envio[1] != addr[1]:
                                            if end_envio[0] == end_socket[0] and end_envio[1] == end_socket[1]:
                                                cliente = self.socket[i]
                                                conteudo = "SALA_FECHADA " + nome_da_sala
                                                cliente.send(conteudo.encode())
                            # Após o fechamento, nenhuma outra mensagem deve enviada pelo servidor naquela sala.
                else:
                    resposta = "ERRO : Para realizar essa operacao é necessario realizar a AUTENTICACAO primeiro !!! "
            
            #Caso o comando nao seja encontrado
            else:
                resposta = "ERRO : Comando Digitado é Invalido!"
            if (self.controle_crip):
                resposta_encripitada= self.encrypt_message(key, iv, resposta) 
                client_socket.send(resposta_encripitada)
            else:
                client_socket.send(resposta.encode())       
        # Fecha a conexão com o cliente
        client_socket.close()

    def encontrar_sala(self, nome_da_sala):
        for i in range(len(self.salas)):
            if self.salas[i].sala_name == nome_da_sala:
                return i
            
        return -1
    
    def salvar_salas_csv(self):
        with open("SalasCadastradas.csv", "w") as cria:
            cria.write("NOME,CRIADOR,SENHA,USUARIOS\n")

        with open("SalasCadastradas.csv", "a") as file:
            for sala in self.salas:
                todos_os_usuarios = ""
                for i in range(len(sala.clients)):
                    todos_os_usuarios = todos_os_usuarios + sala.clients[i] + " "
                file.write(sala.sala_name + "," + sala.admin + "," + sala.password + "," + todos_os_usuarios + "\n")

    
    def main(self):
        
        self.chave_privada = rsa.generate_private_key(
            public_exponent=65537,
            key_size=1024,
            backend=default_backend()
        )
        # Extrair a chave pública da chave privada
        self.chave_publica = self.chave_privada.public_key()
        
        self.chave_publica_codificada = self.obter_chave_publica_codificada(self)
       
        # Carrega a lista de usuarios que ja foram cadastrados no Sistema
        self.carrega_salas(self)
        self.usuarios_cadastrados = self.carrega_usuario(self)
        # Cria um objeto de socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Obtém o nome do host
        host = socket.gethostname()

        # Define a porta em que o servidor irá escutar
        port = 12345

        # Faz o bind do socket com o host e a porta
        server_socket.bind((host, port))

        # Começa a escutar por conexões
        server_socket.listen(500)
        print("Aguardando conexões...")

        while True:
            # Aceita a conexão
            client_socket, addr = server_socket.accept()
            cliente = client_socket            
            self.socket.append(cliente)            
            # Cria uma nova thread para lidar com a conexão
            client_handler = threading.Thread(target=self.handle_client, args=(self, client_socket, addr))
            client_handler.start()

if __name__ == "__main__":
    new_server = Servidor()
    new_server.main()