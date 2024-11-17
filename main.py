import threading
import socket
import sys
from interpretador.analisador_lexico import AnalisadorLexico
from interpretador.analisador_sintatico import AnalisadorSintatico
from interpretador.analisador_semantico import AnalisadorSemantico
from interpretador.interpretador import Interpretador
from interpretador.tabela_simbolos import TabelaDeSimbolos


# Função para iniciar um servidor genérico
def iniciar_servidor(nome, porta, processar_funcao):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', porta))
    server_socket.listen(5)
    print(f"{nome} iniciado na porta {porta}")

    def tratar_conexao(conn, addr):
        print(f"Conexão recebida de {addr}")
        try:
            dados = conn.recv(4096).decode('utf-8')
            resposta = processar_funcao(dados)
            conn.sendall(resposta.encode('utf-8'))
        except Exception as e:
            print(f"Erro ao processar: {e}")
            conn.sendall(f"Erro: {e}".encode('utf-8'))
        finally:
            conn.close()

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=tratar_conexao, args=(conn, addr), name=f"Thread-{addr}")
        thread.start()

def processar_interpretador(dados):
    try:
        thread_name = threading.current_thread().name  # Nome da thread atual
        tipo, codigo_fonte, range_max = dados.split("|||")  # Extrai o tipo de cálculo
        codigo_fonte = codigo_fonte.replace("MAX", range_max)

        analisador_lexico = AnalisadorLexico(codigo_fonte)
        tokens = analisador_lexico.analisar()

        analisador_sintatico = AnalisadorSintatico(tokens)
        arvore_sintatica = analisador_sintatico.analisar()

        tabela_de_simbolos = TabelaDeSimbolos()
        analisador_semantico = AnalisadorSemantico(arvore_sintatica)
        analisador_semantico.analisar()

        interpretador = Interpretador(arvore_sintatica, tabela_de_simbolos)
        interpretador.executar()

        for resultado in interpretador.resultados:
            print(f"{resultado} - {tipo} - {thread_name}")

        return f"Tokens: {tokens}\nÁrvore Sintática: {arvore_sintatica}\nExecução concluída."
    except Exception as e:
        return f"Erro no interpretador: {e}"


# Função para enviar dados para um servidor
def enviar_para_servidor(nome, porta, mensagem):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', porta))
        s.sendall(mensagem.encode('utf-8'))
        resposta = s.recv(4096).decode('utf-8')
        return resposta


def executar_fatorial(maximo):
    codigo_fonte = "x = 1 for i in 1 to MAX { x = x * i print(x) }"
    mensagem = f"Fatorial|||{codigo_fonte}|||{maximo}"
    resposta = enviar_para_servidor("Cliente Interpretador", 12346, mensagem)
    print(f"Fatorial:\n{resposta}")


def executar_fibonacci(maximo):
    codigo_fonte = "x = 0 y = 1 for i in 1 to MAX { z = x x = y y = z + y print(y) }"
    mensagem = f"Fibonacci|||{codigo_fonte}|||{maximo}"
    resposta = enviar_para_servidor("Cliente Interpretador", 12346, mensagem)
    print(f"Fibonacci:\n{resposta}")


def executar_simultaneamente(maximo):
    thread_fatorial = threading.Thread(target=executar_fatorial, args=(maximo,), name="Thread-Fatorial")
    thread_fibonacci = threading.Thread(target=executar_fibonacci, args=(maximo,), name="Thread-Fibonacci")

    thread_fatorial.start()
    thread_fibonacci.start()

    thread_fatorial.join()
    thread_fibonacci.join()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "servidor_interpretador":
            iniciar_servidor("Servidor Interpretador", 12346, processar_interpretador)
        elif sys.argv[1] == "cliente_simultaneo":
            if len(sys.argv) == 3:
                maximo = int(sys.argv[2])
                executar_simultaneamente(maximo)
            else:
                print("Uso: python main.py cliente_simultaneo <maximo>")
        else:
            print("Opção inválida. Use 'servidor_interpretador' ou 'cliente_simultaneo'.")
    else:
        print("Uso: python main.py <servidor_interpretador|cliente_simultaneo>")
