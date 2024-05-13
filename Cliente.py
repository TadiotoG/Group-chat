from Class_Sala import Sala

class Cliente:
    def __init__(self, client_name, key):
        self.name = client_name
        self.public_key = key

    def send_message(message):
        print(message)

    def create_sala(self):
        pass

    def remove_client(self, client_name):
        pass

    def enter_in_sala(self, sala_code):
        pass

    def request_list(self):
        pass

new_client = Cliente("Gabriel", 123)
client_2 = Cliente("Davi", 222)
sala_test = Sala("MinhaSala", new_client)
sala_test.add_new_client(new_client = client_2)
sala_test.list_clients()