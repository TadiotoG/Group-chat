import socket
import threading

def handle_client(client_socket, addr):
    print('Conexão recebida de', addr)
    # Envia uma mensagem de boas-vindas para o cliente
    client_socket.send(b'Obrigado por se conectar!')
    while True:
            msg = client_socket.recv(1024)
            if not msg: break
            print('Mensagem do cliente:', msg.decode())

   

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
    server_socket.listen(5)
    print("Aguardando conexões...")

    while True:
        # Aceita a conexão
        client_socket, addr = server_socket.accept()

        # Cria uma nova thread para lidar com a conexão
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    main()
