#pip install pycryptodome
#pip install cryptography

import tkinter as tk
from tkinter import scrolledtext
import socket
import os
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256
import threading



#chave assimetrica
# Gera uma chave e um IV aleatórios
chaves = get_random_bytes(16)  # AES usa chaves de 16 bytes (128 bits)
print("Chave:", base64.b64encode(chaves).decode())
cifrador = AES.new(chaves, AES.MODE_ECB)
#print(f'Chave gerada: {key}')
#print(f'IV gerado: {iv}')

# Função para criptografar a mensagem
def encrypt_message(message):
     # Criptografar    
    texto_preenchido = pad(message.encode(), AES.block_size)
    texto_cifrado = cifrador.encrypt(texto_preenchido)
    texto_cifrado_codificado = b64encode(texto_cifrado).decode('utf-8')
    return texto_cifrado_codificado

# Função para descriptografar a mensagem
def decrypt_message(texto_cifrado):
    texto_decodificado = b64decode(texto_cifrado)
    texto_recuperado = unpad(cifrador.decrypt(texto_decodificado), AES.block_size)
    return texto_recuperado

"""/////////////////////////////////////////////////////////////////////INTERFACE GRÁFICA/////////////////////////////////////////////////////////////////////"""

import tkinter as tk
from tkinter import scrolledtext

class Main_Menu:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Interface")
        
        # Main frame
        main_frame = tk.Frame(root)
        main_frame.grid(padx=10, pady=10, sticky="nsew")

        # Configure row and column weights for main_frame
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)

        # Create the display area for messages
        self.chat_display = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=70, height=30)
        self.chat_display.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.chat_display.config(state=tk.DISABLED)

        # Frame for buttons
        self.button_frame = tk.Frame(main_frame)
        self.button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        # Create buttons        
        self.button_CRIAR_SALA = tk.Button(self.button_frame, text="CRIAR_SALA", width=20, command=self.criar_sala_message)
        self.button_CRIAR_SALA.pack(pady=5)

        self.button_ENTRAR_SALA = tk.Button(self.button_frame, text="ENTRAR_SALA", width=20, command=self.entrar_sala_message)
        self.button_ENTRAR_SALA.pack(pady=5)

        self.button_SAIR_SALA = tk.Button(self.button_frame, text="SAIR_SALA", width=20, command=self.sair_sala_message)
        self.button_SAIR_SALA.pack(pady=5)

        self.button_ENVIAR_MENSAGEM = tk.Button(self.button_frame, text="ENVIAR_MENSAGEM", width=20, command=self.enviar_mensagem_message)
        self.button_ENVIAR_MENSAGEM.pack(pady=5)

        self.button_FECHAR_SALA = tk.Button(self.button_frame, text="FECHAR_SALA", width=20, command=self.fechar_sala_message)
        self.button_FECHAR_SALA.pack(pady=5)

        self.button_BANIR_USUARIO = tk.Button(self.button_frame, text="BANIR_USUARIO", width=20, command=self.banir_usuario_message)
        self.button_BANIR_USUARIO.pack(pady=5)

        self.button_LISTAR_SALA = tk.Button(self.button_frame, text="LISTAR_SALAS", width=20, command=self.listar_sala_message)
        self.button_LISTAR_SALA.pack(pady=5)

        # Frame for text
        self.text_frame = tk.Frame(main_frame)
        self.text_frame.grid(row=0, column=2, padx=10, pady=10, sticky="n")

        self.message_entry_criar_sala_1 = tk.Entry(self.text_frame, width=30)
        self.message_entry_criar_sala_1.grid(row=0, column=0, padx=5, pady=8)

        self.message_entry_criar_sala_2 = tk.Entry(self.text_frame, width=30)
        self.message_entry_criar_sala_2.grid(row=0, column=1, padx=5, pady=8)

        self.message_entry_criar_sala_3 = tk.Entry(self.text_frame, width=30)
        self.message_entry_criar_sala_3.grid(row=0, column=2, padx=5, pady=8)

        self.message_entry_entrar_sala = tk.Entry(self.text_frame, width=30)
        self.message_entry_entrar_sala.grid(row=1, column=0, padx=5, pady=9)

        self.message_entry_entrar_sala_2 = tk.Entry(self.text_frame, width=30)
        self.message_entry_entrar_sala_2.grid(row=1, column=1, padx=5, pady=9)

        self.message_entry_sair_sala = tk.Entry(self.text_frame, width=30)
        self.message_entry_sair_sala.grid(row=2, column=0, padx=5, pady=9)

        self.message_entry_enviar_msg1 = tk.Entry(self.text_frame, width=30)
        self.message_entry_enviar_msg1.grid(row=3, column=0, padx=5, pady=8)
        
        self.message_entry_enviar_msg2 = tk.Entry(self.text_frame, width=50)
        self.message_entry_enviar_msg2.grid(row=3, column=1, padx=5, pady=8)

        self.message_entry_fechar_sala = tk.Entry(self.text_frame, width=30)
        self.message_entry_fechar_sala.grid(row=4, column=0, padx=5, pady=8)

        self.message_entry_banir_usuario = tk.Entry(self.text_frame, width=30)
        self.message_entry_banir_usuario.grid(row=5, column=0, padx=5, pady=8)

        self.message_entry_banir_usuario2 = tk.Entry(self.text_frame, width=30)
        self.message_entry_banir_usuario2.grid(row=5, column=1, padx=5, pady=8)

        # Bind the return key to send message
        self.root.bind('<Return>', self.send_message)

        # self.receive_msg()
        self.receive_thread = threading.Thread(target=self.receive_msg)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def criar_sala_message(self, event=None):
        public_or_private = self.message_entry_criar_sala_1.get()
        sala_name = self.message_entry_criar_sala_2.get()
        password = self.message_entry_criar_sala_3.get()

        if public_or_private.strip() and sala_name.strip():  # Check if the message is not empty
            if public_or_private.upper() == "PRIVADA":

                msg = "CRIAR_SALA " + public_or_private.upper() + " "  + sala_name
                
                hash_senha =  sha256(password.encode())
                mensagem_cliente = msg + " ["+str(hash_senha)+"("+password+")]"
                encrypted_message = encrypt_message(mensagem_cliente) 
                       
                client_socket.send(encrypted_message)

                #self.receive_msg()
                self.message_entry_criar_sala_1.delete(0, tk.END)
                self.message_entry_criar_sala_2.delete(0, tk.END)
                self.message_entry_criar_sala_3.delete(0, tk.END)

            elif public_or_private.upper() == "PUBLICA":
                msg = "CRIAR_SALA " + public_or_private.upper() + " "  + sala_name 

                encrypted_message = encrypt_message(msg)        
                client_socket.send(encrypted_message)

                #self.receive_msg()
                self.message_entry_criar_sala_1.delete(0, tk.END)
                self.message_entry_criar_sala_2.delete(0, tk.END)
                self.message_entry_criar_sala_3.delete(0, tk.END)

    def entrar_sala_message(self, event=None):
        sala_name = self.message_entry_entrar_sala.get()
        password = self.message_entry_entrar_sala_2.get()

        if sala_name.strip() and password.strip():  # Check if the message is not empty
            msg = "ENTRAR_SALA " + sala_name + " "  + password

            encrypted_message = encrypt_message(msg)        
            client_socket.send(encrypted_message)

            #self.receive_msg()
            self.message_entry_entrar_sala.delete(0, tk.END)
            self.message_entry_entrar_sala_2.delete(0, tk.END)

        else:
            msg = "ENTRAR_SALA " + sala_name

            encrypted_message = encrypt_message(msg)        
            client_socket.send(encrypted_message)

            #self.receive_msg()
            self.message_entry_entrar_sala.delete(0, tk.END)
            self.message_entry_entrar_sala_2.delete(0, tk.END)

    def sair_sala_message(self, event=None):
        sala_name = self.message_entry_sair_sala.get()

        if sala_name.strip():  # Check if the message is not empty
            msg = "SAIR_SALA " + sala_name

            encrypted_message = encrypt_message(msg)        
            client_socket.send(encrypted_message)

            # self.receive_msg()
            self.message_entry_sair_sala.delete(0, tk.END)

    def enviar_mensagem_message(self, event=None):
        sala_name = self.message_entry_enviar_msg1.get()
        mensagem_2_send = self.message_entry_enviar_msg2.get()

        if sala_name.strip():  # Check if the message is not empty
            msg = "ENVIAR_MENSAGEM " + sala_name + " " + mensagem_2_send

            encrypted_message = encrypt_message(msg)        
            client_socket.send(encrypted_message)

            # self.receive_msg()
            self.message_entry_enviar_msg1.delete(0, tk.END)
            self.message_entry_enviar_msg2.delete(0, tk.END)

    def fechar_sala_message(self, event=None):
        sala_name = self.message_entry_fechar_sala.get()

        if sala_name.strip():  # Check if the message is not empty
            msg = "FECHAR_SALA " + sala_name

            encrypted_message = encrypt_message(msg)        
            client_socket.send((encrypted_message))

            # self.receive_msg()
            self.message_entry_fechar_sala.delete(0, tk.END)

    def banir_usuario_message(self, event=None):
        sala_name = self.message_entry_banir_usuario.get()
        user_name = self.message_entry_banir_usuario2.get()
        if sala_name.strip():  # Check if the message is not empty
            msg = "BANIR_USUARIO " + sala_name + " " + user_name

            encrypted_message = encrypt_message(msg)        
            client_socket.send(encrypted_message)

            self.receive_msg()
            self.message_entry_banir_usuario.delete(0, tk.END)

    def listar_sala_message(self, event=None):
        msg = "LISTAR_SALAS"

        encrypted_message = encrypt_message(msg)        
        client_socket.send(encrypted_message)

        # self.receive_msg()
        
    def display_message(self, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.yview(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message.strip():  # Check if the message is not empty
            self.display_message("User" + message)
            self.message_entry.delete(0, tk.END)

    def receive_msg(self):
        while True:
            data = client_socket.recv(1024)
            if " " in data.decode():
                msg_servidor = data.decode()
                mensagem =  msg_servidor.split(" ")
                self.display_message(msg_servidor)

            else:
                msg = decrypt_message(data)
                msg_servidor = msg.decode()
                mensagem =  msg_servidor.split(" ")
                self.display_message(msg_servidor)
            # encrypted_message = client_socket.recv(1024)
            # decrypted_message = decrypt_message(key, iv, encrypted_message).decode()
            # self.display_message(decrypted_message)

            # except Exception as e:
            #     print(f"Erro ao receber mensagem: {e}")
            #     break   

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
#host = "192.168.56.1"
port = 12345

# Conecta ao servidor
client_socket.connect((host, port))

# Recebe dados do servidor
data = client_socket.recv(1024)
print('Mensagem do servidor:', data.decode())

autenticado = False

while(not autenticado):
     # Cria uma nova thread para lidar com a conexão

    msg = input('Envie um mensagem : ')
    mensagem_cliente = msg.split(" ")
    if (mensagem_cliente[0] ==  "REGISTRO"):
        client_socket.send(msg.encode())
    elif (mensagem_cliente[0] ==  "AUTENTICACAO"):
        print(msg.encode())
        client_socket.send(msg.encode())

    data = client_socket.recv(1024)
    #if " " in data.decode():
    try:
        msg_servidor = data.decode()       
        mensagem =  msg_servidor.split(" ")
        print("Mensagem Servidor : \n" , msg_servidor)

        #else:
    except UnicodeDecodeError:
        msg = decrypt_message(data)
        msg_servidor = msg.decode()       
        mensagem =  msg_servidor.split(" ")
        print("Mensagem Servidor : \n" , msg_servidor)
    
    if (mensagem[0] == 'CHAVE_PUBLICA' ):
        autenticado = True
        public_key = mensagem[1]
        public_key_bytes = b64decode(public_key)
        public_key = serialization.load_pem_public_key(
            public_key_bytes,
            backend=default_backend()
        )

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

def on_closing():
    client_socket.close()
    root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    chat_app = Main_Menu(root)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
