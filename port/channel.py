import socket

class Channel:
    def __init__(self, nome, port=12345):
        self.nome = nome
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', self.port))
        self.server_socket.listen(5)
        print(f"Canal {nome} iniciado na porta {self.port}")

    def receber(self):
        conn, addr = self.server_socket.accept()
        try:
            dados = conn.recv(1024).decode('utf-8')
            if not dados:
                raise ConnectionResetError("Conexão fechada pelo cliente.")
            return dados, conn
        except Exception as e:
            print(f"Erro ao receber dados: {e}")
            conn.close()
            raise

    def enviar(self, mensagem):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', self.port))
            s.sendall(mensagem.encode('utf-8'))
            resposta = s.recv(1024).decode('utf-8')
            return resposta
