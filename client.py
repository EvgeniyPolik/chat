import socket
import threading

class ServerClient:
    def SendMessage(self):
        while True:
            user_input = input('Ваше сообщение: \n')
            if user_input != 'q':
                message = f'{self.nickname}: {user_input}'
                self.client.send(message.encode('ascii', errors='xmlcharrefreplace'))
            else:
                break


    def ResiveMessage(self):
        while True:
            try:
                message = self.client.recv(1024).decode('ascii', errors='xmlcharrefreplace')
                if message == '$WHO_ARE_YOU?':
                    self.client.send(self.nickname.encode('ascii', errors='xmlcharrefreplace'))
                else:
                    print(message)
            except:
                print('We are have a same errors, exiting...')
                self.client.close()
                break

    def __init__(self):
        self.server_addr = input('Input server address: ')
        self.server_port = int(input('Input server port: '))
        self.nickname = input('Choose your nickname: ')
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server_addr, self.server_port))
        self.receive_service = threading.Thread(target=self.ResiveMessage)
        self.send_service = threading.Thread(target=self.SendMessage)

    def Working(self):
        self.send_service.start()
        self.receive_service.start()


chat_client = ServerClient()
chat_client.Working()