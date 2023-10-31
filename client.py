import socket
import threading

HEADER = 64
PORT = 5559
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = ':D'
SERVER = '54.90.229.62'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

def receive():
    while True:
        msg = client.recv(2048).decode(FORMAT)
        print("\n", msg, "\n")

# Inicia uma thread separada para receber mensagens do servidor
receive_thread = threading.Thread(target=receive)
receive_thread.start()

while True:
    entry = input('')
    send_thread = threading.Thread(target=send, args=(entry,))
    send_thread.start()
