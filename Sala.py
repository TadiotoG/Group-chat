class Sala:
    def __init__(self, sala_name, creator):
        self.sala_name = sala_name
        self.admin = creator
        self.clients = []

    def add_new_client(self, requester, new_client):
        if self.admin == requester:
            self.clients.append(new_client)
            print("Cliente Adicionado!")

        else:
            print("Nao foi possivel adicionar novo membro!")

    def remove_client(self, requester, client2remove):
        if self.admin == requester:
            for i in range(self.clients):
                if self.clients[i] == client2remove:
                    pass

    def receive_message(self, sender, message):
        if sender in self.clients:
            self.send_message_to_clients(message)

        else:
            print("Voce nao pode enviar mensagens para este grupo!")

    def send_message_to_clients(message):
        pass