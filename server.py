from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


clients = {}
addresses = {}

HOST = ''
PORT = 5050
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


def broadcast(msg, nick=""):
    for sock in clients:
        sock.send(bytes(nick, "utf-8") + msg)


def handle_client(client):
    name = client.recv(BUFSIZ).decode('utf-8')
    print(name)
    welcome = f'Приветик {name}!'+' Если хочешь выйти, напиши {quit} и нажми [Enter]'
    client.send(bytes(welcome, 'utf8'))
    msg = f"{name} has joined the chat!"
    msg_left = f"{name} has left the chat!"
    client.send(bytes(msg, "utf-8"))
    broadcast(bytes(msg, "utf-8"))
    clients[client] = name
    print(clients)
    while True:
        try:
            msg = client.recv(BUFSIZ)
            if msg != bytes("{quit}", "utf-8"):
                broadcast(msg, name + ': ')
            elif msg == bytes("{quit}", "utf-8"):
                # broadcast("Has left the chat", name)
                client.close()
                # clients.pop(client)
        except:
            print(f"{clients[client]} disconnected")

            del clients[client]
            print(clients)
            break


def accept_incoming_connection():
    while True:
        client, client_address = SERVER.accept()
        print(f"{client_address} has connected.")
        client.send(bytes("Добро пожаловать в чат!" + " Впиши свой ник и нажми [Enter]", "utf-8"))
        addresses[client] = client_address
        Thread(target= handle_client, args=(client,)).start()


if __name__ == "__main__":
    SERVER.listen(8)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()