import socket

class ServidorCalculadora:
    def __init__(self, canal):
        self.canal = canal

    def executar(self):
        print("Servidor de Calculadora iniciado. Aguardando conexões...")

        while True:
            try:
                # Aceita conexões do canal
                dados, conn = self.canal.receber()
                print(f"Dados recebidos: {dados}")

                # Processa os dados
                operacao, valor1, valor2 = dados.split()
                valor1, valor2 = int(valor1), int(valor2)
                resultado = self.calcular(operacao, valor1, valor2)

                # Envia o resultado de volta ao cliente
                resposta = f"Resultado: {resultado}"
                conn.sendall(resposta.encode('utf-8'))
                print(f"Operação: {operacao}, Valores: {valor1}, {valor2}, Resultado: {resultado}")

            except ValueError as e:
                # Trata operações inválidas
                print(f"Erro na operação: {e}")
                try:
                    conn.sendall(f"Erro: {e}".encode('utf-8'))
                except Exception:
                    print("Não foi possível enviar a mensagem de erro ao cliente.")

            except (ConnectionResetError, OSError) as e:
                # Trata problemas de conexão
                print(f"Erro de conexão: {e}")

            finally:
                # Fecha a conexão de maneira segura
                if conn:
                    conn.close()

    def calcular(self, operacao, valor1, valor2):
        if operacao == '+':
            return valor1 + valor2
        elif operacao == '-':
            return valor1 - valor2
        elif operacao == '*':
            return valor1 * valor2
        elif operacao == '/':
            if valor2 == 0:
                raise ValueError("Divisão por zero não é permitida")
            return valor1 / valor2
        else:
            raise ValueError(f"Operação inválida: {operacao}")
