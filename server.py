import socket
import threading

host = '0.0.0.0'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients[:]:
        try:
            client.send(message)
        except:
            clients.remove(client)
            client.close()

def kick_user(name):
    if name in nicknames:
        idx = nicknames.index(name)
        client = clients[idx]
        client.send("You were kicked by admin.".encode('ascii'))
        client.close()
        clients.pop(idx)
        nicknames.pop(idx)
        broadcast(f"{name} was kicked.".encode('ascii'))

def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                break

            text = msg.decode('ascii')

            if text.startswith("KICK"):
                if nicknames[clients.index(client)] == 'admin':
                    kick_user(text[5:].strip())
                else:
                    client.send("Admin only.".encode('ascii'))

            elif text.startswith("BAN"):
                if nicknames[clients.index(client)] == 'admin':
                    name = text[4:].strip()
                    kick_user(name)
                    with open("bans.txt", "a") as f:
                        f.write(name + "\n")
                else:
                    client.send("Admin only.".encode('ascii'))
            else:
                broadcast(msg)

        except:
            break

    if client in clients:
        idx = clients.index(client)
        name = nicknames[idx]
        clients.pop(idx)
        nicknames.pop(idx)
        broadcast(f"{name} left.".encode('ascii'))
        client.close()

def receive():
    while True:
        client, addr = server.accept()
        print(f"Connected: {addr}")

        client.send("NICK".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        if nickname == 'admin':
            client.send("PASS".encode('ascii'))
            if client.recv(1024).decode('ascii') != "password":
                client.send("GOAWAY".encode('ascii'))
                client.close()
                continue

        nicknames.append(nickname)
        clients.append(client)

        broadcast(f"{nickname} joined!".encode('ascii'))
        threading.Thread(target=handle, args=(client,), daemon=True).start()

print("Server running...")
receive()
