import socket
import threading
import os
import time

PORTA = 20003
SERVER = 'localhost'
ADDR = (SERVER, PORTA)
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT = ':D'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Lista para armazenar todas as conexões
conexoes = []

def handler(conn, addr):
    print(f'[NOVA CONEXÃO]: {addr} se conectou!')

    conectado = True
    # Adiciona a nova conexão à lista
    conexoes.append(conn)
    
    while conectado:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT:
                conectado = False

            print(f'[{time.ctime()}][{addr}]: {msg}')
            
            # Envia a mensagem para todos os clientes
            for conexao in conexoes:
                conexao.send(f'[{time.ctime()}][{addr}]: {msg}'.encode(FORMAT))

    # Remove a conexão da lista após desconectar
    conexoes.remove(conn)
    conn.close()

def start():
    server.listen()
    print(f'O servidor está no endereço {SERVER}')
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handler, args=(conn, addr))
        thread.start()
        print(f'Conexões ativas: {threading.active_count() - 1}')

print('Iniciando o servidor ...')
print('--------------------------')
start()
