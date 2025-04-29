import socket
import threading
import json
from datetime import datetime

HOST = '127.0.0.1'
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    buffer = ""
    while True:
        try:
            data = client.recv(1024).decode('utf-8')
            if not data:
                break
            buffer += data
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                try:
                    msg_data = json.loads(line)
                    print(f"\n[{msg_data['timestamp']}] {msg_data['sender']}: {msg_data['message']}")
                except:
                    print(f"\n[Error decoding]: {line}")
        except:
            print("Disconnected from server.")
            client.close()
            break

def send():
    while True:
        msg = input()
        message_data = {
            "type": "command" if msg.startswith('/') else "chat",
            "sender": str(client.getsockname()),
            "message": msg,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        client.send((json.dumps(message_data) + "\n").encode('utf-8'))

receive_thread = threading.Thread(target=receive)
send_thread = threading.Thread(target=send)

receive_thread.start()
send_thread.start()
