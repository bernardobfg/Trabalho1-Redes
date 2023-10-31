import tkinter as tk
from tkinter import scrolledtext
import socket
import threading
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--server', type=str, help='Servidor')
parser.add_argument('--port', type=int, help='Porta')

args = parser.parse_args()

server = args.server
port = args.port

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = ':D'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server, int(port)))

def send_msg():
    msg = entry.get()
    if msg:
        send(msg)
        entry.delete(0, tk.END)
        if msg == DISCONNECT_MESSAGE:
            root.quit()  # initiate main loop termination
            root.destroy()  # destroy the window after the main loop exits
            exit()

def receive():
    while True:
        try:
            msg = client.recv(2048).decode(FORMAT)
            root.after(1, lambda: chat_box.insert(tk.END, f"{msg}\n"))
        except ConnectionAbortedError:
            break

def send(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)

# Dark mode theme
dark_bg = "#282828"
dark_fg = "#FFFFFF"
dark_text = "#D3D3D3"

root = tk.Tk()
root.title("Tanaka App")
root.configure(bg=dark_bg)

chat_box = scrolledtext.ScrolledText(root, height=15, width=50, bg=dark_bg, fg=dark_text)
chat_box.pack(pady=10)

entry = tk.Entry(root, width=40, bg=dark_bg, fg=dark_text)
entry.pack(pady=10)

send_button = tk.Button(root, text="Enviar", command=send_msg, bg=dark_bg, fg=dark_text)
send_button.pack()

# Start a thread to receive messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

root.mainloop()
