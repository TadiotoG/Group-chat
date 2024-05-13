import socket
import threading
import csv
import pandas as pd

class Servidor:
    def __init__(self): # Se nao passar parametros cria novo servidor
        self.clientes = []
        self.salas = []

    def __init__(self, load_csv_name): # Se passar nome do csv, abre csv e inicializa servidor
        csv_base = pd.read_csv(load_csv_name)
        for i in range(csv_base["NOME"]):
            self.clients = csv_base['NOME'][i]

        # self.salas = ALGUMA COISA 

    @staticmethod
    def carrega_usuario():
        try:
            with open('UsuariosCadastrados.csv', 'r') as csvfile:
                print('Exite')
        except IOError:
            print ("Criando")
            with open('UsuariosCadastrados.csv', 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames= ['NOME','CHAVE PUBLICA'])
                writer.writeheader()
                writer.writerow({'NOME':'David','CHAVE PUBLICA':'123'})
                
        print("Entrou aqui")
        # Carregar usuários cadastrados de algum lugar
        usuarios_cadastrados = pd.read_csv('UsuariosCadastrados.csv', sep=',', encoding='latin-1')
        #nomes = usuarios_cadastrados['NOME']
        #usuarios_cadastrados = ['David', 'Lens', 'Tadioto']
        
        #print(nomes)
        return usuarios_cadastrados
  
    @staticmethod
    def registro_usuario(usuario):
        usuarios_cadastrados = Servidor.carrega_usuario()
        user = usuarios_cadastrados['NOME']
        for i in user:
            print(i)
            if usuario == i:
                return 'ERRO: Já existe um usuário com este nome.'
        
        with open('UsuariosCadastrados.csv', 'a', newline='') as csvfile:
            fieldnames = ['NOME', 'CHAVE PUBLICA']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'NOME': usuario, 'CHAVE PUBLICA': '123'})
            #usuarios_cadastrados = pd.read_csv('UsuariosCadastrados.csv', sep=',', encoding='latin-1')
        return 'Usuário registrado com sucesso.'

    @staticmethod
    def handle_client(client_socket, addr):
        print('Conexão recebida de', addr)
        # Envia uma mensagem de boas-vindas para o cliente
        client_socket.send(b'Obrigado por se conectar!')
        while True:
            msg = client_socket.recv(1024)
            if not msg: break
            print('Mensagem do cliente:', msg.decode())
            msg = msg.decode() # Aqui podemos fazer varias condicoes para diferentes comandos

            #Pequeno exemplo abaixo

            # if msg == "Create_sala"
            #   servidor.create_new_sala() 

            if msg.startswith("REGISTRO"):              
                nome_usuario = msg.split(" ")[1]
                resposta = Servidor.registro_usuario(nome_usuario)
                client_socket.send(resposta.encode())
        
        # Fecha a conexão com o cliente
        client_socket.close()
    
    def main():
        
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
            client_handler = threading.Thread(target=Servidor.handle_client, args=(client_socket, addr))
            client_handler.start()

if __name__ == "__main__":
    Servidor.main()
