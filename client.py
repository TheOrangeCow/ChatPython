import socket
import threading
import time
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('216.24.57.251', 55555))
#client.connect(("chatbackend-4efu.onrender.com", 55555))


nickname = input("Nickname: ")

if nickname == 'admin':
    password = input("Password: ")

def receive():
    while True:
        try:
            msg = client.recv(1024).decode('ascii')
            if msg == 'NICK':
                client.send(nickname.encode('ascii'))
            elif msg == 'PASS':
                client.send(password.encode('ascii'))
            elif msg == 'GOAWAY':
                print("Wrong password")
                client.close()
                break
            else:
                print(msg)
        except:
            client.close()
            break

def write():
    while True:
        text = input()
        if text.startswith('/kick'):
            client.send(f"KICK {text[6:]}".encode('ascii'))
        elif text.startswith('/ban'):
            client.send(f"BAN {text[5:]}".encode('ascii'))
        else:
            timestamp = time.strftime("%H:%M:%S")
            client.send(f"{nickname} ({timestamp}): {text}".encode('ascii'))

threading.Thread(target=receive, daemon=True).start()
write()
