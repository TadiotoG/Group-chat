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
        self.chat_display = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=100, height=30)
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

        self.button_FECHAR_SALA = tk.Button(self.button_frame, text="FECHAR_SALA", width=20, command=self.fechar_sala_message)
        self.button_FECHAR_SALA.pack(pady=5)

        self.button_BANIR_USUARIO = tk.Button(self.button_frame, text="BANIR_USUARIO", width=20, command=self.banir_usuario_message)
        self.button_BANIR_USUARIO.pack(pady=5)

        self.button_LISTAR_SALA = tk.Button(self.button_frame, text="LISTAR_SALA", width=20, command=self.listar_sala_message)
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

        self.message_entry_fechar_sala = tk.Entry(self.text_frame, width=30)
        self.message_entry_fechar_sala.grid(row=3, column=0, padx=5, pady=8)

        self.message_entry_banir_usuario = tk.Entry(self.text_frame, width=30)
        self.message_entry_banir_usuario.grid(row=4, column=0, padx=5, pady=8)

        # Bind the return key to send message
        self.root.bind('<Return>', self.send_message)

    def criar_sala_message(self, event=None):
        public_or_private = self.message_entry_criar_sala_1.get()
        sala_name = self.message_entry_criar_sala_2.get()
        password = self.message_entry_criar_sala_3.get()

        if public_or_private.strip() and sala_name.strip():  # Check if the message is not empty
            if public_or_private.upper() == "PRIVADA":
                msg = "CRIAR_SALA " + public_or_private.upper() + " "  + sala_name + " " + password
                self.display_message(msg)
                self.message_entry_criar_sala_1.delete(0, tk.END)
                self.message_entry_criar_sala_2.delete(0, tk.END)
                self.message_entry_criar_sala_3.delete(0, tk.END)

            elif public_or_private.upper() == "PUBLICA":
                msg = "CRIAR_SALA " + public_or_private.upper() + " "  + sala_name
                self.display_message(msg)
                self.message_entry_criar_sala_1.delete(0, tk.END)
                self.message_entry_criar_sala_2.delete(0, tk.END)
                self.message_entry_criar_sala_3.delete(0, tk.END)

    def entrar_sala_message(self, event=None):
        sala_name = self.message_entry_entrar_sala.get()
        password = self.message_entry_entrar_sala_2.get()

        if sala_name.strip() and password.strip():  # Check if the message is not empty
            msg = "ENTRAR_SALA " + sala_name + " "  + password
            self.display_message(msg)
            self.message_entry_entrar_sala.delete(0, tk.END)
            self.message_entry_entrar_sala_2.delete(0, tk.END)

        else:
            msg = "ENTRAR_SALA " + sala_name
            self.display_message(msg)
            self.message_entry_entrar_sala.delete(0, tk.END)
            self.message_entry_entrar_sala_2.delete(0, tk.END)

    def sair_sala_message(self, event=None):
        sala_name = self.message_entry_sair_sala.get()

        if sala_name.strip():  # Check if the message is not empty
            msg = "SAIR_SALA " + sala_name
            self.display_message(msg)
            self.message_entry_sair_sala.delete(0, tk.END)

    def fechar_sala_message(self, event=None):
        sala_name = self.message_entry_fechar_sala.get()

        if sala_name.strip():  # Check if the message is not empty
            msg = "FECHAR_SALA " + sala_name
            self.display_message(msg)
            self.message_entry_fechar_sala.delete(0, tk.END)

    def banir_usuario_message(self, event=None):
        sala_name = self.message_entry_banir_usuario.get()

        if sala_name.strip():  # Check if the message is not empty
            msg = "BANIR_USUARIO " + sala_name
            self.display_message(msg)
            self.message_entry_banir_usuario.delete(0, tk.END)

    def listar_sala_message(self, event=None):
        msg = "LISTAR_SALA"
        self.display_message(msg)
        
    def display_message(self, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.yview(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message.strip():  # Check if the message is not empty
            self.display_message("User", message)
            self.message_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    chat_app = Main_Menu(root)
    root.mainloop()
