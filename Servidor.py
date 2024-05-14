import socket
import threading
import csv
import pandas as pd
from Class_Sala import Sala

class Servidor:
    def __init__(self): # Se nao passar parametros cria novo servidor
        self.clientes = []
        self.salas = []
        self.usuarios_cadastrados = [] # Vai ter tudo
        self.usuarios_autenticados = []  # Vai ter somente os que estao em uso a parti que o servidor comeca a rodar
        self.codigo_usuarios = [] # Armazena a porta e o ip no mesmo indice que que o autenticado
        self.socket = [] # possivel gambiarra funcional
    @staticmethod
    def carrega_usuario(self):
        try:
            with open('UsuariosCadastrados.csv', 'r') as csvfile:
                print("Carrregando Servidor ...")
        except IOError:
            print('Criando Servidor ...')
            print('Servidor Criado')            
            with open('UsuariosCadastrados.csv', 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames= ['NOME','CHAVE PUBLICA'])
                writer.writeheader()
                writer.writerow({'NOME':'David','CHAVE PUBLICA':'123'})
                
        # Carregar usuários cadastrados de algum lugar
        usuarios_cadastrados = pd.read_csv('UsuariosCadastrados.csv', sep=',', encoding='latin-1')
        
        return usuarios_cadastrados
    
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
            new_sala.load_system(todos_usuarios.split(" "))
            self.salas.append(new_sala)
        # new_sala = Sala(nome_da_sala, nome_usuario, senha)

    @staticmethod
    def autentifica_usuario(self, usuario, addr):
        user = self.usuarios_cadastrados['NOME']
        for nome in user:
            if usuario == nome:
                self.usuarios_autenticados.append(usuario)
                self.codigo_usuarios.append(addr)
                return 'Usuário autentificado com sucesso.'    
        return 'ERRO: Não existe um usuário com este nome.'
        
    @staticmethod
    def registro_usuario(self, usuario, addr):
        #usuarios_cadastrados = self.carrega_usuario(self)
        user = self.usuarios_cadastrados['NOME']
        for nome in user:
            if usuario == nome:
                return 'ERRO: Já existe um usuário com este nome.'
        
        with open('UsuariosCadastrados.csv', 'a', newline='') as csvfile:
            fieldnames = ['NOME', 'CHAVE PUBLICA']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'NOME': usuario, 'CHAVE PUBLICA': '123'})
            novo_usuario = pd.DataFrame({'NOME': [usuario], 'CHAVE PUBLICA': ['123']})
            self.usuarios_cadastrados = pd.concat([self.usuarios_cadastrados, novo_usuario],ignore_index=True)
            self.usuarios_autenticados.append(usuario)
            end = ' '.join((addr[0], str(addr[1]))) # COLOQUEI str(addr[1])
            self.codigo_usuarios.append(end)
        #print(self.usuarios_autenticados[0])
        #print(addr[1])
        return 'Usuário registrado com sucesso.'
    
    @staticmethod
    def identifica_usuario(self,addr):
        user = self.usuarios_cadastrados['NOME']        
        i = 0
        for end in self.codigo_usuarios:
            if end[0] == addr[0] and end[1] == addr [1]:
                
                return self.usuarios_autenticados[i]  
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
            print('Mensagem do cliente:', msg.decode())
            msg = msg.decode()       
            mensagem =  msg.split(" ")
            # REGISTRO
            if mensagem[0] ==  "REGISTRO":              
                nome_usuario = mensagem[1]
                resposta = self.registro_usuario(self, nome_usuario, addr)
            
            # AUTENTICACAO
            elif mensagem[0] ==  "AUTENTICACAO":              
                nome_usuario = mensagem[1]
                resposta = self.autentifica_usuario(self, nome_usuario, addr)
                # AQUI TERA QUE PASSAR A CHAVE PUBLICA DO SERVIDOR PARA O USUARIO
                # Fazer isso posteriomente

            # CRIAR SALA
            elif mensagem[0] == "CRIAR_SALA":
                privacidade = mensagem[1]
                nome_da_sala = mensagem[2]
                nome_usuario = self.identifica_usuario(self, addr)
                if privacidade == "PRIVADA":
                    if len(mensagem) > 3:
                        senha = mensagem[3]
                        new_sala = Sala(nome_da_sala, nome_usuario, senha)
                        self.salas.append(new_sala)
                        resposta = "Sala criada!"
                    else:
                        resposta = "ERRO : Ausencia de senha para sala PRIVADA"

                else:
                    new_sala = Sala(nome_da_sala, nome_usuario)
                    self.salas.append(new_sala)
                    resposta = "Sala criada!"

            # ENTRAR NA SALA
            elif mensagem[0] == "ENTRAR_SALA":
                nome_usuario = self.identifica_usuario(self, addr)
                nome_da_sala = mensagem[1]
                senha = ""
                if len(mensagem) > 2:
                    senha = mensagem[2]

                indice_sala = self.encontrar_sala(nome_da_sala)

                if indice_sala == -1:
                    resposta = "Sala não encontrada!"

                else:
                    resposta = self.salas[indice_sala].add_new_client(nome_usuario, senha)

            # SAIR_SALA
            elif mensagem[0] == "SAIR_SALA":
                nome_usuario = self.identifica_usuario(self, addr)
                nome_da_sala = mensagem[1]
                indice_sala = self.encontrar_sala(nome_da_sala)

                if indice_sala == -1:
                    resposta = "Sala não encontrada!"

                else:
                    resposta = self.salas[indice_sala].remove_client(nome_usuario, nome_usuario)

            # LISTAR_SALAS
            elif mensagem[0] == "LISTAR_SALAS": 
                #Funcao responsavel por verificar qual usuario solicitou a informação
                nome=self.identifica_usuario(self,addr)
                resposta = "Lista de salas: "
                for sala in self.salas:
                    resposta = resposta + sala.sala_name + ", "

            # BANIR_USUARIO
            elif mensagem[0] == "BANIR_USUARIO":
                nome_usuario = self.identifica_usuario(self, addr)
                nome_da_sala = mensagem[1]
                usuario_banido = mensagem[2]
                indice_sala = self.encontrar_sala(nome_da_sala)

                if indice_sala == -1:
                    resposta = "Sala não encontrada!"

                else:
                    resposta = self.salas[indice_sala].remove_client(nome_usuario, usuario_banido)

            # SAIR DO SISTEMA
            elif mensagem[0] == "DESCONECTAR":
                print("Cliente ", self.identifica_usuario(self,addr), " desconectado")
                resposta = "Desconectado do servidor!"

            # LISTAR USUARIOS DE UMA SALA
            elif mensagem[0] == "LISTAR_USUARIOS":
                nome_da_sala = mensagem[1]
                indice_sala = self.encontrar_sala(nome_da_sala)

                if indice_sala == -1:
                    resposta = "Sala não encontrada!"

                else:
                    resposta = self.salas[indice_sala].list_clients()

            # ENVIAR MENSAGEM 
            elif mensagem[0] == "ENVIAR_MENSAGEM" :
                nome_da_sala = mensagem[1]
                conteudo = mensagem[2]
                if (len(mensagem)> 2):
                    mensagem = mensagem[3:]
                    for i in range(len(mensagem)):
                        conteudo = conteudo +" "+ mensagem[i]
                indice_sala = self.encontrar_sala(nome_da_sala)
                if indice_sala == -1:
                    resposta = "Sala não encontrada!"
                else:
                    resposta = self.salas[indice_sala].list_clients()
                    usuarios_da_sala =  resposta.split(', ')
                    resposta = "Mensagem enviada"
                    for nome in usuarios_da_sala:
                        end_envio = self.identifica_endereco(self,nome)
                        if end_envio != None:
                            for i in range(len(self.socket)):
                                end_socket = self.socket[i].getpeername()   
                                print(end_envio[0])
                                print(end_socket[0])
                                print(end_envio[1])
                                print(end_socket[1])
                                if end_envio[0] != addr[0] or end_envio[1] != addr[1]:
                                    if end_envio[0] == end_socket[0] and end_envio[1] == end_socket[1]:
                                        cliente = self.socket[i]
                                        conteudo = "Mensagem do grupo " + nome_da_sala + " de " + self.identifica_usuario(self,addr) + " : " + conteudo
                                        cliente.send(conteudo.encode())
                                        print(self.socket[i])
                                        



            # FECHA SALA

            else:
                resposta = "Comando Invalido!"
            resposta = 'Mensagem do servidor: ' + resposta
            client_socket.send(resposta.encode())
            self.salvar_salas_csv()
                    
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