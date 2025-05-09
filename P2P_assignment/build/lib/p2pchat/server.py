import socket
import threading
import sqlite3
from datetime import datetime
import json

def main():
    print("Starting server...")

    # Set up SQLite database
    conn = sqlite3.connect('chat.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            message TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()

    HOST = '127.0.0.1'
    PORT = 48484

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    clients = []
    addresses = {}

    def handle_client(client):
        addr = addresses[client]

        cursor.execute("SELECT sender, message, timestamp FROM messages ORDER BY id DESC LIMIT 10")
        history = reversed(cursor.fetchall())
        for sender, msg, ts in history:
            data = {
                "type": "chat",
                "sender": sender,
                "message": msg,
                "timestamp": ts
            }
            client.send((json.dumps(data) + "\n").encode('utf-8'))

        while True:
            try:
                msg_raw = client.recv(1024).decode('utf-8')
                if not msg_raw:
                    break

                lines = msg_raw.strip().split('\n')
                for line in lines:
                    try:
                        msg_data = json.loads(line)
                    except:
                        continue

                    if msg_data["type"] == "command" and msg_data["message"] == "/online":
                        online_list = [str(addresses[c]) for c in clients]
                        data = {
                            "type": "notify",
                            "sender": "server",
                            "message": "Online users:\n" + "\n".join(online_list),
                            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        client.send((json.dumps(data) + "\n").encode('utf-8'))
                        continue

                    if msg_data["type"] == "chat":
                        cursor.execute("INSERT INTO messages (sender, message, timestamp) VALUES (?, ?, ?)",
                                       (msg_data["sender"], msg_data["message"], msg_data["timestamp"]))
                        conn.commit()

                    broadcast(json.dumps(msg_data), client)

            except:
                break

        clients.remove(client)
        offline_msg = {
            "type": "notify",
            "sender": "server",
            "message": f"(Off) {addr} left the chat.",
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        broadcast(json.dumps(offline_msg), client)
        del addresses[client]
        client.close()

    def broadcast(message, sender):
        print(f"[Broadcasting] {message}")
        for client in clients:
            if client != sender:
                try:
                    client.send((message + "\n").encode('utf-8'))
                except:
                    pass

    print("Server is running...")
    while True:
        client, addr = server.accept()
        print(f"Connected by {addr}")
        clients.append(client)
        addresses[client] = addr

        join_msg = {
            "type": "notify",
            "sender": "server",
            "message": f"(On) {addr} joined the chat.",
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        broadcast(json.dumps(join_msg), client)

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    main()
