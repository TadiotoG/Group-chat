import socket
import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


# Cria um objeto de socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Aqui deve adicionar o IP do servidor
host = socket.gethostname()

# Define a porta em que o servidor está escutando
port = 12345

# Conecta ao servidor
client_socket.connect((host, port))
#chave assimetrica
key = os.urandom(32)
#Vetor de inicializacao
iv = os.urandom(16)
# Escolha o backend padrão
backend = default_backend()


# Criando o objeto que criptografa AES com a chave gerada 
aes = algorithms.AES(key)
cbc = modes.CBC(iv)
cipher =  Cipher (aes, cbc, backend=backend)
chave_Simetrica= cipher.encryptor()
print(cipher)
# Recebe dados do servidor
data = client_socket.recv(1024)
print('Mensagem do servidor:', data.decode())

controle = 0
while(True):
     # Cria uma nova thread para lidar com a conexão
    msg = input('Envie um mensagem : ')
    client_socket.send(msg.encode())
    data = client_socket.recv(1024)
    msg_servidor = data.decode()       
    print("Mensagem Servidor :" , msg_servidor)
    mensagem =  msg_servidor.split(" ")          
    
    if (mensagem[0] == 'CHAVE_PUBLICA' ):
        public_key = mensagem[1]
        public_key_bytes = b64decode(public_key)
        public_key = serialization.load_pem_public_key(
            public_key_bytes,
            backend=default_backend()
        )
        # Finalize a operação de criptografia para obter a chave simétrica criptografada
        texto_para_ser_criptografado = chave_Simetrica.finalize()
        #texto_para_ser_criptografado = cipher 
        # Cifrar a chave simétrica com a chave pública
        print(texto_para_ser_criptografado)
        texto_criptografado = public_key.encrypt(
            texto_para_ser_criptografado,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        texto_criptografado_codificado = b64encode(texto_criptografado).decode('utf-8')
        
        msg = "CHAVE_SIMETRICA " + texto_criptografado_codificado
        client_socket.send(msg.encode())

        controle = 1
    #elif (controle == 1):
    #   data = client_socket.recv(1024)
    #    print(data.decode())
     #   block_size = 16 
     #   n = len(b_MSG)
     #   spaces_add = block_size -n  % block_size 
    #    new_b_MSG = bytearray(MSG + ' ' * spaces_add,encoding="utf8")
    #    texto_criptografado = chave_Simetrica.update(new_b_MSG) + chave_Simetrica.finalize()
    
    #else:
     #   print('erro')


    if msg == "DESCONECTAR":
        break

client_socket.close()
