from client.calculadora_client import ClienteCalculadora
from interpretador.analisador_lexico import AnalisadorLexico
from interpretador.analisador_sintatico import AnalisadorSintatico
from interpretador.analisador_semantico import AnalisadorSemantico
from interpretador.interpretador import Interpretador
import sys

from interpretador.tabela_simbolos import TabelaDeSimbolos
from port.channel import Channel
from port.server_calculadora import ServidorCalculadora

def executar_interpretador(codigo_fonte, range):
    codigo_fonte = codigo_fonte.replace("MAX", str(range))
    print("Executando Analisador Léxico...")
    analisador_lexico = AnalisadorLexico(codigo_fonte)
    tokens = analisador_lexico.analisar()
    print("Tokens gerados:", tokens)

    print("\nExecutando Analisador Sintático...")
    analisador_sintatico = AnalisadorSintatico(tokens)
    arvore_sintatica = analisador_sintatico.analisar()
    print("Árvore Sintática:", arvore_sintatica)

    print("\nExecutando Analisador Semântico...")
    tabela_de_simbolos = TabelaDeSimbolos()
    analisador_semantico = AnalisadorSemantico(arvore_sintatica)
    analisador_semantico.analisar()

    print("\nExecutando Interpretador...")
    interpretador = Interpretador(arvore_sintatica, tabela_de_simbolos)
    interpretador.executar()

def iniciar_servidor_calculadora():
    print("Iniciando Servidor de Calculadora...")
    canal_servidor = Channel("CalculadoraServidor", port=12345)
    servidor = ServidorCalculadora(canal_servidor)
    servidor.executar()

def executar_cliente_calculadora(operacao, valor1, valor2):
    print(f"Enviando operação: {operacao} {valor1} {valor2}")
    canal_cliente = Channel("CalculadoraCliente", port=12345)
    cliente = ClienteCalculadora(canal_cliente)
    resultado = cliente.enviar_operacao(operacao, valor1, valor2)
    print(f"Resultado recebido: {resultado}")

if __name__ == "__main__":
    codigo_fonte = """
        x = 0
        y = 1
        for i in 1 to MAX {
            z = x
            x = y
            y = z + y
            print(y)
        }
    """

    if len(sys.argv) > 1:
        if sys.argv[1] == "interpretador":
            executar_interpretador(codigo_fonte, sys.argv[2])
        elif sys.argv[1] == "servidor":
            iniciar_servidor_calculadora()
        elif sys.argv[1] == "cliente":
            if len(sys.argv) == 5:
                operacao = sys.argv[2]
                valor1 = int(sys.argv[3])
                valor2 = int(sys.argv[4])
                executar_cliente_calculadora(operacao, valor1, valor2)
            else:
                print("Uso: python main.py cliente <operacao> <valor1> <valor2>")
        else:
            print("Opção inválida. Use 'interpretador', 'servidor' ou 'cliente'.")
    else:
        print("Uso: python main.py <interpretador|servidor|cliente>")
