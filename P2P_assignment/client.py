import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            print(f"\n{msg}")
        except:
            print("Disconnected from server.")
            client.close()
            break

def send():
    while True:
        msg = input()
        client.send(msg.encode('utf-8'))

receive_thread = threading.Thread(target=receive)
send_thread = threading.Thread(target=send)

receive_thread.start()
send_thread.start()
