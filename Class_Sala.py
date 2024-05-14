class Sala:

    def __init__(self, sala_name, creator, password = ""):
        self.sala_name = sala_name
        self.admin = creator
        self.password = password
        self.clients = []

    def add_new_client(self, new_client, passw = ""):
        if self.password == passw:
            self.clients.append(new_client)
            return "Entrou em " + self.sala_name

        else:
            return "Nao foi possivel adicionar novo membro!"
        
    def load_system(self, list_of_clients):
        self.clients = list_of_clients

    def remove_client(self, requester, client2remove):
        if self.admin == requester or requester == client2remove:
            for i in range(self.clients):
                if self.clients[i] == client2remove:
                    del(self.clients[i])
                    return "Membro Removido!"

    def receive_message(self, sender, message):
        if sender in self.clients:
            self.send_message_to_clients(message)

        else:
            print("Voce nao pode enviar mensagens para este grupo!")

    def send_message_to_clients(self, message):
        print(message)
        pass

    def list_clients(self):
        all_clients = ""
        for client in self.clients:
            all_clients = all_clients + client.name + ", "
        return all_clients
