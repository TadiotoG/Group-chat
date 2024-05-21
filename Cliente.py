#pip install pycryptodome
#pip install cryptography

import socket
import os
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

# Função para criptografar a mensagem
def encrypt_message(key, iv, message):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_message = base64.b64encode(cipher.encrypt(pad(message.encode(), AES.block_size)))
    return encrypted_message

# Função para descriptografar a mensagem
def decrypt_message(key, iv, encrypted_message):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(base64.b64decode(encrypted_message)), AES.block_size)
    return decrypted_message

# Cria um objeto de socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 12345

# Conecta ao servidor
client_socket.connect((host, port))

#chave assimetrica
# Gera uma chave e um IV aleatórios
key = os.urandom(32)
iv = os.urandom(16)
chaves = key + iv
print(f'Chave gerada: {key}')
print(f'IV gerado: {iv}')


# Recebe dados do servidor
data = client_socket.recv(1024)
print('Mensagem do servidor:', data.decode())

controle = 0
while(True):
     # Cria uma nova thread para lidar com a conexão
    msg = input('Envie um mensagem : ')
    mensagem_cliente = msg.split(" ")
    if (mensagem_cliente[0] ==  "REGISTRO"):
        client_socket.send(msg.encode())
    elif (mensagem_cliente[0] ==  "AUTENTICACAO"):
        client_socket.send(msg.encode())
    else :
        encrypted_message = encrypt_message(key, iv, msg)        
        client_socket.send(encrypted_message)

    data = client_socket.recv(1024)
    msg_servidor = data.decode()       
    print("Mensagem Servidor : \n" , msg_servidor)
    mensagem =  msg_servidor.split(" ")          
    
    if (mensagem[0] == 'CHAVE_PUBLICA' ):
        public_key = mensagem[1]
        public_key_bytes = b64decode(public_key)
        public_key = serialization.load_pem_public_key(
            public_key_bytes,
            backend=default_backend()
        )
        print(public_key)
        # Envia a chave para o servidor
        #client_socket.send(key)

        # Envia o IV para o servidor
        #client_socket.send(iv)
        
        
        texto_criptografado = public_key.encrypt(
            chaves,
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
