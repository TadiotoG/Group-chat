import socket

# Cria um objeto de socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Obtém o nome do host do servidor
host = socket.gethostname()

# Define a porta em que o servidor está escutando
port = 12345

# Conecta ao servidor
client_socket.connect((host, port))

# Recebe dados do servidor
data = client_socket.recv(1024)
print('Mensagem do servidor:', data.decode())
for i in range(5):
    msg = input('Envie um mensagem : ')
    client_socket.send(msg.encode())
    data = client_socket.recv(1024)
    print('Mensagem do servidor:', data.decode())

client_socket.close()
