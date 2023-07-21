import socket
import os
import threading

class Ponte(threading.Thread):
    def __init__(self, socket):
        super().__init__()
        self.socket = socket

    def run(self):
        try:
            self.handle_client()
        except Exception as e:
            print("Erro:", e)
        finally:
            self.socket.close()

    def handle_client(self):
        data = self.socket.recv(1024).decode()

        if data == "UPLOAD":
            file_name = self.socket.recv(1024).decode()
            file_size = int(self.socket.recv(1024).decode().strip())
            self.save_file(file_name, file_size)
        elif data == "DOWNLOAD":
            file_name = self.socket.recv(1024).decode()
            self.send_file(file_name)
        else:
            print("Comando inválido do cliente.")

    def save_file(self, file_name, file_size):
        with open(file_name, 'wb') as file:
            remaining_size = file_size
            buffer_size = 4 * 1024
            while remaining_size > 0:
                data = self.socket.recv(min(buffer_size, remaining_size))
                file.write(data)
                remaining_size -= len(data)

        print("Arquivo recebido:", file_name)

    def send_file(self, file_name):
        file_path = os.path.join("C:/Users/edson/OneDrive/Documentos/criptografia/", file_name)  # Substitua pelo caminho real do diretório no servidor

        if os.path.exists(file_path) and os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            self.socket.sendall(b"FILE_FOUND")
            self.socket.sendall(str(file_size).encode())

            with open(file_path, 'rb') as file:
                buffer_size = 4 * 1024
                while True:
                    data = file.read(buffer_size)
                    if not data:
                        break
                    self.socket.sendall(data)

            print("Arquivo enviado:", file_name)
        else:
            self.socket.sendall(b"FILE_NOT_FOUND")

def main():
    host = "192.168.0.6"  # Aceita conexões de qualquer endereço IP
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print("Servidor está ouvindo na porta", port)

    while True:
        client_socket, client_address = server_socket.accept()
        print("Cliente conectado:", client_address)
        client_handler = Ponte(client_socket)
        client_handler.start()

if __name__ == "__main__":
    main()
