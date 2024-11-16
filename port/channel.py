import socket

class Channel:
    def __init__(self, nome, host='localhost', port=12345):
        self.nome = nome
        self.host = host
        self.port = port

    def enviar(self, mensagem):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            sock.sendall(mensagem.encode('utf-8'))
            resposta = sock.recv(1024).decode('utf-8')
            return resposta

    def receber(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))
            sock.listen()
            print(f"Servidor {self.nome} aguardando conexões em {self.host}:{self.port}...")
            conn, addr = sock.accept()
            with conn:
                print(f"Conectado por {addr}")
                dados = conn.recv(1024).decode('utf-8')
                return dados, conn
