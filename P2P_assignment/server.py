import socket
import threading
print("Starting server...")


HOST = '127.0.0.1'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []

def handle_client(client):
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            broadcast(msg, client)
        except:
            clients.remove(client)
            client.close()
            break

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message.encode('utf-8'))

print("Server is running...")
while True:
    client, addr = server.accept()
    print(f"Connected by {addr}")
    clients.append(client)
    thread = threading.Thread(target=handle_client, args=(client,))
    thread.start()

