import socket
import threading

class ServerUser:  # class UserInfo
    def __init__(self, socket_id, nickname, address):
        self.socket_id = socket_id
        self.nickname = nickname
        self.address = address

class ChatServer:  #Server class
    def __init__(self, ip_address, server_port):
        self.server_ip = ip_address
        self.port = server_port
        self.users = []

    def Start(self):  # Wait connection
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.server_ip, self.port))
        server.listen()
        while True:
            new_client, client_address = server.accept()
            new_client.send('$WHO_ARE_YOU?'.encode('ascii', errors='xmlcharrefreplace'))
            client_nick = new_client.recv(1024).decode('ascii', errors='xmlcharrefreplace')
            new_user = ServerUser(new_client, client_nick, client_address)
            self.SendMessageToAll(f'{new_user.nickname} came here!')
            self.users.append(new_user)
            new_user.socket_id.send('Welcome to our server!'.encode('ascii', errors='xmlcharrefreplace'))
            print(f'We are have new user: {new_user.nickname}')
            new_thread = threading.Thread(target=self.UserDialog, args=(new_user,))
            new_thread.start()

    def SendMessageToAll(self, message = '', sender = None): # Send message all users
        for user in self.users:
            if sender and user != sender:
                user.socket_id.send(f"{user.nickname}: {message}".encode('ascii', errors='xmlcharrefreplace'))
            if sender is None and message != '':
                user.socket_id.send(f"{'SERVER: '}: {message}".encode('ascii', errors='xmlcharrefreplace'))


    def UserDialog(self, new_user):  # Wait new message from user
        while True:
            try:
                message = new_user.socket_id.recv(1024)
                self.SendMessageToAll(message, new_user.socket_id)
            except:
                index = self.users.index(new_user)
                self.users.remove(new_user)
                new_user.socket_id.close()
                self.SendMessageToAll(f'{new_user.nickname} left')
                break


ip = input('Введите ip: ')
prt = input('Введите порт: ')
s = ChatServer(ip, int(prt))
print("Server is statrting...")
s.Start() # Start server