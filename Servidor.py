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
    def autentifica_usuario(self, usuario,addr):
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
            end = ' '.join([addr[0], addr[1]])
            self.codigo_usuarios.append(end)
        #print(self.usuarios_autenticados[0])
        #print(addr[1])
        return 'Usuário registrado com sucesso.'
    
    @staticmethod
    def indetifica_usuario(self,addr):
        user = self.usuarios_cadastrados['NOME']        
        i = 0
        for end in self.codigo_usuarios:
            if end[0] == addr[0]:
                if end[1] == addr [1]:
                    #print(self.usuarios_autenticados[i])
                    return self.usuarios_autenticados[i]  
            i += 1
    
    @staticmethod
    def handle_client(self, client_socket, addr):
        print('Conexão recebida de', addr)
        # Envia uma mensagem de boas-vindas para o cliente
        client_socket.send(b'Obrigado por se conectar!')
        while True:
            msg = client_socket.recv(1024)
            if not msg: break
            print('Mensagem do cliente:', msg.decode())
            msg = msg.decode()       
            mensagem =  msg.split(" ")       
            # REGISTRO
            if mensagem[0] ==  "REGISTRO":              
                nome_usuario = mensagem[1]
                resposta = self.registro_usuario(self, nome_usuario,addr)
                client_socket.send(resposta.encode())
            
             # AUTENTICACAO
            if mensagem[0] ==  "AUTENTICACAO":              
                nome_usuario = mensagem[1]
                resposta = self.autentifica_usuario(self, nome_usuario,addr)
                # AQUI TERA QUE PASSAR A CHAVE PUBLICA DO SERVIDOR PARA O USUARIO
                # Fazer isso posteriomente
                client_socket.send(resposta.encode())

            # CRIAR SALA
            if mensagem[0] == "CRIAR_SALA":   
                privacidade = mensagem[1]
                nome_da_sala = mensagem[2]
                if privacidade == "PRIVADA":
                    if len(mensagem) > 3:
                        senha = mensagem[3]
                        new_sala = Sala(nome_da_sala, addr, senha)
                        self.salas.append(new_sala)
                        print(senha)
                    else:
                        client_socket.send(b'ERRO : Ausencia de senha para sala PRIVADA')

                else:
                    new_sala = Sala(nome_da_sala, addr)
                    self.salas.append(new_sala)

            # ENTRAR NA SALA
            if mensagem[0] == "ENTRAR_SALA":
                pass

            # LISTAR_SALAS
            if mensagem[0] == "LISTAR_SALAS": 
                #Funcao responsavel por verificar qual usuario solicitou a informação
                nome=self.indetifica_usuario(self,addr)
                indice_sala = self.encontrar_sala(nome)
                self.salas[indice_sala].list_clients()

            # SAIR_SALA

            # BANIR_USUARIO
        # Fecha a conexão com o cliente
        client_socket.close()

    def encontrar_sala(self, nome_da_sala):
        for i in range(self.salas):
            if self.salas[i] == nome_da_sala:
                return i
    
    def main(self):
        # Carrega a lista de usuarios que ja foram cadastrados no Sistema
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

            # Cria uma nova thread para lidar com a conexão
            client_handler = threading.Thread(target=self.handle_client, args=(self, client_socket, addr))
            client_handler.start()

if __name__ == "__main__":
    new_server = Servidor()
    new_server.main()