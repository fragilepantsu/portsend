import sys
import socket
import threading
import time

class RawClient:
    def __init__(self, ip, port, listen_port):
        self.ip = ip
        self.port = port
        self.listen_port = listen_port
        self.is_sending = False
        self.stop_listening = threading.Event()
        self.buffer_size = 1024 

    def listen_on_port(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            try:
                server_socket.bind(('0.0.0.0', self.listen_port))
                server_socket.listen()
                print(f"Listening for incoming connections on port {self.listen_port}...")

                while not self.stop_listening.is_set():
                    server_socket.settimeout(1) 
                    try:
                        connection, client_address = server_socket.accept()
                        with connection:
                            data = b'' 
                            while True:
                                chunk = connection.recv(self.buffer_size)
                                if not chunk:
                                    break
                                data += chunk  
                                
                                if len(data) > 65536: 
                                    print("[ERROR] Data size exceeds limit. Disconnecting.")
                                    break
                                
                                try:
                                    decoded_data = data.decode('utf-8', errors='ignore') 
                                    print(f"\n[RECEIVED] From {client_address[0]}:{client_address[1]}: {decoded_data}")
                                except UnicodeDecodeError as e:
                                    print(f"[ERROR] Decoding data: {e}")
                    except socket.timeout:
                        continue

            except Exception as e:
                print(f"[ERROR] While listening: {e}")

    def send_raw_message(self):
        while True:
            message = input("> ")

            if message.lower() == 'exit':
                print("[CLOSING] Connection...")
                self.stop_listening.set()
                break

            
            self.is_sending = True
            self.stop_listening.set()
            print(f"[STATUS] Switching to sending mode...")

            time.sleep(0.5)

            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(5)  
                    s.connect((self.ip, self.port))
                    print(f"[CONNECTED] to {self.ip}:{self.port} from local port {s.getsockname()[1]}.")
                    s.sendall(message.encode('utf-8'))
                    print(f"[SENT] {message}")
            except socket.timeout:
                print("[ERROR] Connection timed out.")
            except Exception as e:
                print(f"[ERROR] While sending: {e}")


            print(f"[STATUS] Switching back to listening mode...")
            self.is_sending = False
            self.stop_listening.clear()
            time.sleep(1)

def main():
    if len(sys.argv) < 7:
        print("Usage: python sendraw.py -a IP -p PORT -l LISTEN_PORT")
        sys.exit(1)
    
    ip = None
    port = None
    listen_port = None

    for i in range(len(sys.argv)):
        if sys.argv[i] == '-a':
            ip = sys.argv[i + 1]
        elif sys.argv[i] == '-p':
            port = int(sys.argv[i + 1])
        elif sys.argv[i] == '-l':
            listen_port = int(sys.argv[i + 1])

    if ip is None or port is None or listen_port is None:
        print("Usage: python sendraw.py -a IP -p PORT -l LISTEN_PORT")
        sys.exit(1)

    client = RawClient(ip, port, listen_port)


    listener_thread = threading.Thread(target=client.listen_on_port)
    listener_thread.daemon = True
    listener_thread.start()


    client.send_raw_message()

if __name__ == "__main__":
    main()
